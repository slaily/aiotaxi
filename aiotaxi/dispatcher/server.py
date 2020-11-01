import asyncio

from json import loads

from aiotaxi import common

from . import utils


async def handle_client(reader, writer):
    addr = common.get_client_addr(writer)
    common.display_connected_client(addr)
    received_message = await common.read_message(reader)
    common.display_received_message(received_message, addr)
    received_message_dict = loads(received_message)

    if received_message_dict['message'].lower().startswith('dispatcher'):
        dispatcher_id = utils.assign_dispatcher('Available')
        message_to_send = dispatcher_id.encode('utf-8')
        await common.write_message(writer, message_to_send)

    await common.close_stream_writer(writer)
    print(f'Client {addr} - connection closed.')


async def main():
    server = await asyncio.start_server(
        handle_client, '127.0.0.1', 9999)

    addr = server.sockets[0].getsockname()
    print(f'Serving on {addr}')

    async with server:
        await server.serve_forever()


asyncio.run(main())
