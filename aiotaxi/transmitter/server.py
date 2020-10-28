import asyncio

from aiotaxi import common

from . import utils


async def handle_client(reader, writer):
    try:
        addr = writer.get_extra_info('peername')
        common.display_connected_client(addr)

        while message := await reader.readline():
            decoded_message = message.decode()
            common.display_received_message(decoded_message, addr)

            if decoded_message.lower().startswith('close'):
                break

        print(f'Client {addr!r} - Leaving Connection.')
    except asyncio.CancelledError:
        for task in asyncio.all_tasks():
            task.cancel()

        print('Connection dropped!')
    finally:
        writer.close()


async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 8888)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


try:
    asyncio.run(main(), debug=True)
except KeyboardInterrupt:
    print('Server is shutting down...')
