#!/usr/bin/python3


import json
from dnslib import RR, A
from dnslib.proxy import ProxyResolver
from dnslib.server import DNSServer


class SubProxy(ProxyResolver):
    def __init__(self, address, port, timeout, b_list, answer, host):
        ProxyResolver.__init__(self, address, port, timeout)
        self.blacklist = b_list
        self.answer = answer
        self.host = host

    def resolve(self, request, handler):
        if request.q.qname in self.blacklist:
            answer = RR(rdata=A(self.host))
            answer.set_rname(self.answer)
            reply = request.reply()
            reply.add_answer(answer)
            return reply
        else:
            return ProxyResolver.resolve(self, request, handler)


if __name__ == '__main__':
    import time

    with open('config.json', 'r') as conf_file:
        conf = json.load(conf_file)

    resolver = SubProxy(address=conf['upper_dns'],
                        port=conf['port'],
                        timeout=conf['socket_timeout'],
                        b_list=conf['blacklist'],
                        answer=conf['answer'],
                        host=conf['host'])

    server = DNSServer(resolver,
                       port=conf['port'],
                       address=conf['host'])

    server.start_thread()

    while server.isAlive():
        time.sleep(1)
