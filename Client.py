import socket, select, errno, time, struct
from Constants import *

class Client:
    """ Netrek TCP & UDP Client
        for connection to a server to play or observe the game.
    """
    # FIXME: add UDP client
    def __init__(self, sp):
        self.sp = sp
        self.bufsiz = 1024
        self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcp.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1)
        self.udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udp.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.bufsiz)
        self.time = time.time()
        self.tcp_connected = 0
        self.mode_requested = COMM_UDP
        self.mode = None

    def connect(self, host, port):
        """ connect via TCP to a game server, and prepare the UDP
        socket, returns True on success """

        # iterate through the addresses of the server host until one connects
        addresses = socket.getaddrinfo(host, port, socket.AF_INET, socket.SOCK_STREAM)
        for family, socktype, proto, canonname, sockaddr in addresses:
            try:
                self.sockaddr = sockaddr
                self.tcp.connect(sockaddr)
                self.tcp_connected = 1
                break
            except socket.error, (reason, explanation):
                if reason == errno.ECONNREFUSED:
                    print host, sockaddr, "is not listening"
                else:
                    print host, sockaddr, reason, explanation
                continue

        if not self.tcp_connected:
            return False

        self.mode = COMM_TCP
        
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
        return True

    def tcp_send(self, data):
        self.tcp.send(data)

    def udp_send(self, data):
        self.udp.send(data)

    def send(self, data):
        if self.mode == COMM_UDP:
            self.udp.send(data)
        else:
            self.tcp.send(data)

    def recv(self):
        """ check for and process data arriving from the server """
        # FIXME: a network update may cost more local time in
        # processing than the time between updates from the server,
        # which results in a pause to display updates since this
        # function does not return until the network queue is empty
        # ... this could be detected and CP_UPDATES negotiation made
        # to reduce the update rate.
        while 1:
            is_readable = [self.tcp, self.udp]
            is_writable = []
            is_error = []
            r, w, e = select.select(is_readable, is_writable, is_error, 0.04)
            if not r: return
            if self.udp in r:
                self.udp_readable()
            if self.tcp in r:
                self.tcp_readable()

    def tcp_readable(self):
        """ process TCP data, socket file descriptor is readable, and
        presumed to be positioned at the first byte of a game
        packet. """

        try:
            byte = self.tcp.recv(1)
            if len(byte) == 1:
                self.tcp_read_more(byte, self.tcp)
                return
            # recv returned zero, indicating connection closure
            # FIXME: when server closes connection, offer to reconnect
            print "server disconnection"
            sys.exit(1)
        except socket.error, (reason, explanation):
            if reason == errno.EINTR: return
            print "tcp recv", reason, explanation
            sys.exit(1)
                    
    def tcp_read_more(self, byte, sock):
        """ process more TCP data, socket file descriptor is
        positioned after the first byte of a game packet, from which
        we may deduce the length, so we read in only the remaining
        bytes of the game packet, and then process it, leaving any
        further game packets to be detected on next select. """

        # recognise the packet type byte
        p_type = struct.unpack('b', byte[0])[0]
        (size, instance) = self.sp.find(p_type)
        if size == 1:
            raise "Unknown packet type %d, a packet was received from the server that is not known to this program, and since packet lengths are determined by packet types there is no reasonable way to continue operation" % (p_type)
            return

        # read the remaining bytes of the packet from the socket
        rest = ''
        while len(rest) < (size-1):
            new = sock.recv((size-1) - len(rest))
            if new == '':
                break # eof
            rest += new
        if len(rest) != (size-1):
            print "### asked for %d and got %d bytes" % ((size-1), len(rest))

        # set the timestamp
        self.time = time.time()

        # reconstruct the packet and pass it to a handler
        instance.handler(byte + rest)

    def udp_readable(self):
        """ process UDP data, socket file descriptor is readable, and
        so we will read the UDP packet from the socket, then break it
        down into game packets, one by one, and pass each to the
        respective handler. """

        try:
            packet = self.udp.recv(self.bufsiz)
        except socket.error, (reason, explanation):
            if reason == errno.EINTR: return
            print "udp recv", reason, explanation
            self.udp_failure()
            return

        # set the timestamp
        self.time = time.time()

        # break UDP packet into game packets using type codes and handle
        offset = 0
        length = len(packet)
        while offset < length:
            p_type = struct.unpack_from('b', packet, offset)[0]
            (size, instance) = self.sp.find(p_type)
            if size != 1:
                # FIXME: detect truncated packets
                instance.handler(packet[offset:offset+size])
                offset = offset + size
                continue
            print "bad udp drop type=%d bytes=%d" % (p_type, length-offset)
            return
                    
    def sp_pickok(self):
    	""" ship has entered game, switch to udp mode """
        if self.mode_requested != COMM_UDP:
            return
        if self.mode != COMM_UDP:
            self.tcp.send(cp_udp_req.data(COMM_UDP, CONNMODE_PORT, self.udp_sockport))
        
    def sp_udp_reply(self, reply, port):
        """ server acknowledged CP_UDP_REQ switch to udp mode """
        if reply == SWITCH_UDP_OK:
            self.udp_peerport = port
            self.udp.connect((self.udp_peerhost, self.udp_peerport))
            self.udp.send(cp_udp_req.data(COMM_VERIFY, 0, 0))
            self.mode = COMM_UDP
        if reply == SWITCH_TCP_OK:
            self.mode = COMM_TCP

    def udp_failure(self):
        # FIXME: test, when UDP connection severed, reset to TCP
        self.mode = COMM_TCP
        self.tcp.send(cp_udp_req.data(COMM_TCP, 0, 0))
    
    def shutdown(self):
        self.tcp.shutdown(socket.SHUT_RDWR)

