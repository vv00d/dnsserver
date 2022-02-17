from conf import get_config
from server import start
import asyncio


if __name__ == '__main__':
    config:dict = get_config()
    loop = asyncio.get_event_loop()
    print("Starting datagram proxy...")
    coro = start(config)
    transport, _ = loop.run_until_complete(coro)
    print("Datagram proxy is running...")
    try:
        loop.run_forever()
    except KeyboardInterrupt:
        pass
    print("Closing transport...")
    transport.close()
    loop.close()
