import sys, socket, select, errno, time, struct, array, threading
from .constants import *

MSG_PEEK = socket.MSG_PEEK
try:
    MSG_DONTWAIT = socket.MSG_DONTWAIT
except AttributeError:
    # on some platforms socket.MSG_DONTWAIT is not defined
    MSG_DONTWAIT = 0

class Error(Exception):
    pass

class ServerDisconnectedError(Error):
    pass


class NetworkThread(threading.Thread):
    """Background thread: blocks on network sockets, dispatches packet
    handlers, then posts a pygame event so the main thread wakes up."""

    def __init__(self, client, event_type):
        super().__init__(daemon=True, name='network-io')
        self.client = client
        self.event_type = event_type
        self._stop = threading.Event()

    def run(self):
        import pygame
        while not self._stop.is_set():
            try:
                data = self.client.recv(timeout=0.5)
            except ServerDisconnectedError:
                self._stop.set()
                try:
                    pygame.event.post(pygame.event.Event(self.event_type))
                except Exception:
                    pass
                break
            except Exception:
                self._stop.set()
                break
            if data:
                try:
                    pygame.event.post(pygame.event.Event(self.event_type))
                except Exception:
                    pass

    def stop(self):
        self._stop.set()


class Client:
    """ Netrek TCP & UDP Client
        for connection to a server to play or observe the game.
    """
    def __init__(self, sp):
        self.sp = sp
        self.bufsiz = 1024 * 8
        self.buffer = array.array('B', bytes(self.bufsiz))
        self.time = time.time()
        self.mode_requested = COMM_UDP
        self.mode = None
        self.udp_rx_path_proven = False
        self.udp_tx_path_proven = False
        self.has_quit = False
        self.tcp = self.udp = -1
        self.ct = self.cu = 0
        self._net_thread = None

    def connect(self, host, port):
        """ connect via TCP to a game server, and prepare the UDP
        socket, returns True on success """

        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.bufsiz)

        # iterate through the addresses of the server host until one connects
        addresses = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
        for family, socktype, proto, canonname, sockaddr in addresses:
            try:
                self.sockaddr = sockaddr
                self.tcp.connect(sockaddr)
                self.mode = COMM_TCP
                break
            except OSError as _e:
                reason, explanation = _e.args
                if reason == errno.ECONNREFUSED:
                    print(host, sockaddr, "is not listening")
                else:
                    print(host, sockaddr, reason, explanation)
                continue

        if self.mode is None:
            return False

        # test that the socket is connected
        self.tcp_peername = self.tcp.getpeername()
        (self.tcp_peerhost, self.tcp_peerport) = self.tcp_peername
        self.tcp_sockname = self.tcp.getsockname()

        # try binding the UDP socket to the same port number
        # (rationale: ease of packet trace analysis)
        try:
            self.udp.bind(self.tcp_sockname)
        except socket.error:
            # otherwise use any free port number
            (udp_host, udp_port) = self.sockaddr
            self.udp.bind((udp_host, 0))

        self.udp_sockname = self.udp.getsockname()
        (self.udp_sockhost, self.udp_sockport) = self.udp_sockname

        # our UDP connection will eventually be to the same host as the TCP
        self.udp_peerhost = self.tcp_peerhost
        self.udp_peerport = None
        self.ct = self.cu = 0
        self.has_quit = False
        return True

    def start_network_thread(self, event_type):
        """Start the background network I/O thread."""
        self._net_thread = NetworkThread(self, event_type)
        self._net_thread.start()

    def stop_network_thread(self):
        """Signal and join the background network I/O thread."""
        if self._net_thread is not None:
            self._net_thread.stop()
            self._net_thread.join(timeout=2.0)
            self._net_thread = None

    def tcp_send(self, data):
        self.tcp.send(data)

    def udp_send(self, data):
        self.udp.send(data)

    def send(self, data):
        if self.mode == COMM_UDP:
            self.udp.send(data)
        else:
            self.tcp.send(data)

    def recv(self, timeout=0.02):
        """ check for and process data arriving from the server,
        returns true if data was processed, false if not """
        fds = [s for s in [self.tcp, self.udp] if s != -1]
        if not fds:
            return False
        try:
            r, _, _ = select.select(fds, [], [], timeout)
        except (OSError, ValueError):
            return False
        self.time = time.time()
        data = False
        if self.udp in r:
            self.udp_readable()
            data = True
        if self.tcp in r:
            self.tcp_readable()
            data = True
        return data

    def udp_readable(self):
        """ process UDP data, socket file descriptor is readable, and
        so we will read the UDP packet from the socket, then break it
        down into game packets, one by one, and pass each to the
        respective handler. """

        try:
            length = self.udp.recv_into(self.buffer, self.bufsiz)
        except OSError as _e:
            reason, explanation = _e.args
            if reason == errno.EINTR: return
            print("udp recv", reason, explanation)
            self.udp_failure()
            return

        self.udp_rx_path_proven = True

        # break UDP packet into game packets using type codes and handle
        offset = 0
        while offset < length:
            p_type = struct.unpack_from('b', self.buffer, offset)[0]
            (size, instance) = self.sp.find(p_type)
            if size != 1:
                # FIXME: detect truncated packets
                instance.handler(self.buffer[offset:offset+size].tobytes())
                self.cu += 1
                offset = offset + size
                continue
            print("bad udp drop type=%d bytes=%d" % (p_type, length-offset))
            return

    def tcp_readable(self):
        """ process TCP data, socket file descriptor is readable, and
        presumed to be positioned at the first byte of a game packet,
        so we shall look to see how many bytes are ahead in the
        stream, and if there is a potential for segmentation use the
        byte by byte method ... this generally occurs during the
        initial login data burst because of the MOTD and torp arrays. """

        # find out how much is available right now
        try:
            pbytes = self.tcp.recv_into(self.buffer, self.bufsiz,
                                        MSG_PEEK + MSG_DONTWAIT)
        except OSError as _e:
            reason, explanation = _e.args
            print("tcp recv", reason, explanation)
            self.shutdown()
            raise ServerDisconnectedError

        if pbytes > 1024:
            return self.tcp_readable_stream()

        # FIXME: at this point, on a server where queue has no slot,
        # server emits ntserv/main.c: Quitting: No slot available on
        # queue 0 and client experiences socket.error: (104,
        # 'Connection reset by peer')

        # read all the data available right now
        try:
            length = self.tcp.recv_into(self.buffer, pbytes)
        except OSError as _e:
            reason, explanation = _e.args
            if reason == errno.EINTR: return
            print("tcp recv", reason, explanation)
            sys.exit(1)
        if length == 0:
            print("server disconnection")
            self.shutdown()
            raise ServerDisconnectedError

        # break TCP packet into game packets using type codes and handle
        offset = 0
        while offset < length:
            p_type = struct.unpack_from('b', self.buffer, offset)[0]
            (size, instance) = self.sp.find(p_type)
            if size != 1:
                # if we have not got the complete packet, read some more
                if (offset + size) > length:
                    have = length - offset
                    need = size - have
                    length += self.tcp.recv_into(
                        memoryview(self.buffer)[length:], need)
                instance.handler(self.buffer[offset:offset+size].tobytes())
                self.ct += 1
                offset = offset + size
                continue
            print("bad tcp drop type=%d bytes=%d" % (p_type, length-offset))
            return

    def tcp_readable_stream(self):
        """ process TCP data, socket file descriptor is readable, and
        presumed to be positioned at the first byte of a game packet,
        but we shall read the stream in a bytewise fashion instead of
        hoping for a game packet ... and return after we have read
        only one game packet ... the performance impact is acceptable
        only during login. """

        try:
            byte = self.tcp.recv(1)
            if len(byte) == 1:
                self.tcp_read_more(byte, self.tcp)
                return
            # recv returned zero, indicating connection closure
            print("server disconnection")
            self.shutdown()
            raise ServerDisconnectedError
        except OSError as _e:
            reason, explanation = _e.args
            if reason == errno.EINTR: return
            print("tcp recv", reason, explanation)
            sys.exit(1)

    def tcp_read_more(self, byte, sock):
        """ process more TCP data, socket file descriptor is
        positioned after the first byte of a game packet, from which
        we may deduce the length, so we read in only the remaining
        bytes of the game packet, and then process it, leaving any
        further game packets to be detected on next select. """

        # recognise the packet type byte; byte is a bytes object of length 1
        p_type = struct.unpack('b', byte)[0]
        (size, instance) = self.sp.find(p_type)
        if size == 1:
            raise RuntimeError(
                "Unknown packet type %d, a packet was received from the server "
                "that is not known to this program, and since packet lengths are "
                "determined by packet types there is no reasonable way to "
                "continue operation" % (p_type,))

        # read the remaining bytes of the packet from the socket
        rest = b''
        while len(rest) < (size - 1):
            new = sock.recv((size - 1) - len(rest))
            if not new:
                break  # eof
            rest += new
        if len(rest) != (size - 1):
            print("### asked for %d and got %d bytes" % ((size - 1), len(rest)))

        # reconstruct the packet and pass it to a handler
        instance.handler(byte + rest)
        self.ct += 1

    def sp_pickok(self):
        """ ship has entered game, switch to udp mode """
        if self.mode_requested != COMM_UDP:
            return
        if self.mode != COMM_UDP:
            self.tcp.send(self.cp_udp_req.data(COMM_UDP, CONNMODE_PORT, self.udp_sockport))
            self.udp_rx_path_proven = False
            self.udp_tx_path_proven = False
            # FIXME: detect failure of either rx or tx path
            # FIXME: tx path requires netrek protocol level interpretation

    def sp_udp_reply(self, reply, port):
        """ server acknowledged CP_UDP_REQ switch to udp mode """
        if reply == SWITCH_UDP_OK:
            self.udp_peerport = port
            self.udp.connect((self.udp_peerhost, self.udp_peerport))
            self.udp.send(self.cp_udp_req.data(COMM_VERIFY, 0, 0))
            self.mode = COMM_UDP
        if reply == SWITCH_TCP_OK:
            self.mode = COMM_TCP

    def udp_failure(self):
        self.mode = COMM_TCP
        self.tcp.send(self.cp_udp_req.data(COMM_TCP, 0, 0))

    def statistics(self):
        print('network statistics: tcp game packets = %d, udp game packets = %d' % (self.ct, self.cu))

    def shutdown(self):
        self.stop_network_thread()
        try:
            self.tcp.shutdown(socket.SHUT_RDWR)
        except Exception:
            pass
        self.tcp.close()
        self.udp.close()
        self.tcp = self.udp = -1
        self.mode = None
        self.statistics()

    def diagnostics(self):
        (self.tcp_sockhost, self.tcp_sockport) = self.tcp_sockname
        return "TCP: %s:%s -> %s:%s, UDP: %s -> %s" % (
            self.tcp_sockhost, self.tcp_sockport,
            self.tcp_peerhost, self.tcp_peerport,
            self.udp_sockport, self.udp_peerport)
