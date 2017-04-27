import usocket as socket

class MetaSocket:
    def __init__(self, url):
        _, _, self.host, _ = url.split('/', 3)
        self.s = socket.socket()

    def get(self, url): # returns socket
        _, _, _, path = url.split('/', 3)
        self.addr = socket.getaddrinfo(self.host, 80)[0][-1]
        self.s.connect(self.addr)
        self.s.send(bytes('GET /{} HTTP/1.0\r\nHost: {}\r\n\r\n'.format(path, self.host), 'utf8'))
