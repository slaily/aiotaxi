import asyncio

from json import dumps

from aiotaxi import common

from . import utils


async def handle_client(reader, writer):
    try:
        addr = common.get_client_addr(writer)
        common.display_connected_client(addr)
        unrecognized_message_counter = 0

        while message := await reader.readline():
            decoded_message = message.decode().strip('\n')
            common.display_received_message(decoded_message, addr)

            if decoded_message.lower().startswith('dispatcher'):
                dispatcher_reader, dispatcher_writer = await utils.establish_ext_serv_conn(
                    '127.0.0.1', 9999
                )

                if not dispatcher_writer:
                    continue

                msg_to_send_dict = {
                    'from_addr': addr,
                    'message': decoded_message
                }
                msg_to_send = dumps(msg_to_send_dict).encode('utf-8')
                asyncio.create_task(
                    common.write_message(dispatcher_writer, msg_to_send)
                )

                if not dispatcher_reader:
                    continue

                ext_message = await common.read_message(dispatcher_reader)
                dispatcher_addr = dispatcher_writer.get_extra_info('peername')
                common.display_received_message(ext_message, dispatcher_addr)
                asyncio.create_task(
                    common.close_stream_writer(dispatcher_writer)
                )
                asyncio.create_task(
                    common.write_message(writer, ext_message.encode('utf-8'))
                )
                break
            elif decoded_message.lower().startswith('close'):
                break
            else:
                if unrecognized_message_counter == 3:
                    break

                unrecognized_message_counter += 1
                asyncio.create_task(
                    common.write_message(
                        writer, b'Unrecognized message, do you need a taxi?\n'
                    )
                )

        print(f'Client {addr!r} - Leaving Connection.')
    except asyncio.CancelledError:
        for task in asyncio.all_tasks():
            task.cancel()

        print(f'Client {addr!r} connection dropped.')
    finally:
        asyncio.create_task(
            common.close_stream_writer(writer)
        )


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
