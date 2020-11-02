import asyncio

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
                _, received_message = await utils.transmit_message_to_dispatcher(
                    addr, decoded_message
                )
                asyncio.create_task(
                    common.write_message(writer, received_message)
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
