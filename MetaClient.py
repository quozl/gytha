import socket, select

class MetaClient:
    """ Netrek UDP MetaClient
        for connection to metaservers to obtain list of games in play
        References: server/ntserv/solicit.c server/tools/players.c
        metaserver/*.c client/parsemeta.c
    """
    def __init__(self):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.spout = None
        self.servers = {}

    def uncork(self, spout):
        self.spout = spout

    def query(self, metaserver):
        metaservers = ("127.0.0.1", "224.0.0.1", metaserver)
        # FIXME: merge duplicate replies from 127.0.0.1 and the
        # interface used by 224.0.0.1
        for hostname in metaservers:
            addresses = socket.getaddrinfo(
                    hostname, 3521, socket.AF_INET, socket.SOCK_STREAM)
            for family, socktype, proto, canonname, sockaddr in addresses:
                try:
                    self.socket.sendto('?', sockaddr)
                except socket.error:
                    print sockaddr, "bad"
    
    def recv(self):
        if not self.spout:
            return
        while 1:
            is_readable = [self.socket]
            is_writable = []
            is_error = []
            r, w, e = select.select(is_readable, is_writable, is_error, 0.1)
            if not r: return
            try:
                (text, address) = self.socket.recvfrom(2048)
                break
            except:
                return
        if text[0] == 's': self.version_s(text, address)
        elif text[0] == 'r': self.version_r(text)

    def version_s(self, text, address):
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
        self.update(server)

    def version_r(self, text):
        lines = text.split('\n')
        (version, n) = lines[0].split(',')
        for x in range(int(n)):
            server = {}
            (server['name'], port, server['status'], age, players, queue, server['type']) = lines[x+1].split(',')
            server['port'] = int(port)
            server['age'] = int(age)
            server['players'] = int(players)
            server['queue'] = int(queue)
            server['comment'] = ''
            self.update(server)

    def update(self, server):
        # FIXME: client currently lacks necessary hockey support
        if server['type'] == 'H':
            return

        # FIXME: client currently lacks necessary sturgeon support
        if server['type'] == 'S':
            return

        name = server['name']
        if not name in self.servers:
            self.servers[name] = server
        else:
            self.servers[name]['players'] = server['players']
            self.servers[name]['queue'] = server['queue']
            
        if self.spout:
            self.spout(name)
