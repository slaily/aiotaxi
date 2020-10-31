import asyncio


from aiotaxi import common


async def handle_client(reader, writer):
    addr = writer.get_extra_info('peername')
    common.display_connected_client(addr)
    message = await common.read_message(reader)
    common.display_received_message(message, addr)

    if message.lower().startswith('dispatcher'):
        pass

    await common.close_stream_writer(writer)
    print(f'Client {addr!r} - connection closed.')


async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 9999)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
