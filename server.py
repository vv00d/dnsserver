import asyncio
from server_protocols import ProxyDatagramProtocol


async def start(config: dict):
    print("Starting UDP server")
    addr = config['host']
    port = config['port']
    dns_addr = config['dns']
    dns_port = config['dns_port']
    blacklist = config['blacklist']
    err_answer = config['answer']

    loop = asyncio.get_event_loop()
    protocol = ProxyDatagramProtocol((dns_addr, dns_port), blacklist, err_answer)
    return await loop.create_datagram_endpoint(
        lambda: protocol, local_addr=(addr, port))
