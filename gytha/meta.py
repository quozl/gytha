import socket, select

class MetaClient:
    """ Netrek UDP MetaClient
        for connection to metaservers to obtain list of games in play
        References: server/ntserv/solicit.c server/tools/players.c
        metaserver/*.c client/parsemeta.c
    """
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        self.spout = None
        self.servers = {}
        # non-blocking poll; called at ~100 Hz from the USEREVENT handler
        self.timeout = 0
        self.last_s = None

    def uncork(self, spout):
        self.spout = spout

    def query(self, metaserver):
        self.last_s = None
        metaservers = ("127.0.0.1", "224.0.0.1", metaserver)
        for hostname in metaservers:
            try:
                addresses = socket.getaddrinfo(
                        hostname, 3521, socket.AF_INET, socket.SOCK_STREAM)
                for family, socktype, proto, canonname, sockaddr in addresses:
                    (ip, port) = sockaddr
                    if ip == '65.193.17.240':
                        continue
                    try:
                        self.socket.sendto(b'?version=gytha', sockaddr)
                        print("queried", hostname, "aka", ip)
                    except socket.error:
                        print("unable to query %s, proceeding" % str(sockaddr))
            except socket.gaierror:
                print("unable to resolve %s, proceeding" % hostname)

    def recv(self):
        r, w, e = select.select([self.socket], [], [], self.timeout)
        if self.socket in r:
            if not self.spout:
                print("suboptimal, mc recv spout unready")
                return
            try:
                # netrek-metaserver/disp_udp.c display_udp() specifies
                # no maximum size of the response
                (data, address) = self.socket.recvfrom(8192)
            except Exception:
                return
            # decode bytes to str for parsing
            try:
                text = data.decode('ascii', errors='replace')
            except Exception:
                return
            if text[0] == 's':
                self.version_s(text, address)
            elif text[0] == 'r':
                self.version_r(text)

    def version_s(self, text, address):
        """ single server reply from a server via multicast """

        # ignore duplicate responses from localhost
        if text == self.last_s: return
        self.last_s = text

        unpack = text.split(',')
        server = {}
        server['name'] = address[0]
        server['type'] = unpack[1]
        server['comment'] = unpack[2]
        server['port'] = int(unpack[4])
        server['players'] = int(unpack[5])
        server['queue'] = int(unpack[6].strip())
        server['status'] = 2
        if server['type'] == 'unknown': server['status'] = 3
        server['age'] = 0
        server['source'] = 's'
        self.update(server)

    def version_r(self, text):
        """ multi-server reply from a metaserver via UDP query """
        lines = text.split('\n')
        (version, n) = lines[0].split(',')
        for x in range(int(n)):
            server = {}
            (server['name'], port, server['status'], age, players, queue,
             server['type']) = lines[x+1].split(',')
            server['port'] = int(port)
            server['age'] = int(age)
            server['players'] = int(players)
            server['queue'] = int(queue)
            server['comment'] = ''
            server['source'] = 'r'
            self.update(server)

    def update(self, server):
        # FIXME: client currently lacks necessary hockey support
        if server['type'] == 'H':
            return
        # FIXME: client currently lacks necessary sturgeon support
        if server['type'] == 'S':
            return
        # FIXME: client currently lacks necessary paradise support
        if server['type'] == 'P':
            return

        name = server['name']
        if name not in self.servers:
            self.servers[name] = server
        else:
            self.servers[name]['players'] = server['players']
            self.servers[name]['queue'] = server['queue']

        if self.spout:
            self.spout(name)
