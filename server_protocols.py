import dnslib
import asyncio


class ProxyDatagramProtocol(asyncio.DatagramProtocol):

    def __init__(self, remote_address, blacklist, err_answer):
        self.remote_address = remote_address
        self.remotes = {}
        self.blacklist = blacklist
        self.err_answer = err_answer
        super().__init__()

    def get_qname(self, data):
        qname = str(dnslib.DNSRecord().parse(data).q.get_qname())
        qname = qname.strip()[:-1]
        return qname

    def is_valid(self, qname):
        return qname not in self.blacklist

    def connection_made(self, transport):
        self.transport = transport

    def send_data(self, data, addr):
        if addr in self.remotes:
            self.remotes[addr].transport.sendto(data)
        else:
            loop = asyncio.get_event_loop()
            self.remotes[addr] = RemoteDatagramProtocol(self, addr, data)
            coro = loop.create_datagram_endpoint(
                lambda: self.remotes[addr], remote_addr=self.remote_address)
            asyncio.ensure_future(coro)

    def datagram_received(self, data, addr):
        qname: str = self.get_qname(data)
        if self.is_valid(qname):
            self.send_data(data, addr)
        else:
            data = self.err_answer.encode()
            self.transport.sendto(data, addr)


class RemoteDatagramProtocol(asyncio.DatagramProtocol):

    def __init__(self, proxy, addr, data):
        self.proxy = proxy
        self.addr = addr
        self.data = data
        super().__init__()

    def connection_made(self, transport):
        self.transport = transport
        self.transport.sendto(self.data)

    def datagram_received(self, data, _):
        self.proxy.transport.sendto(data, self.addr)

    def connection_lost(self, exc):
        self.proxy.remotes.pop(self.attr)
