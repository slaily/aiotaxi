import asyncio

from aiotaxi import common
from aiotaxi.settings import (
    TRANSMITTER_HOST,
    TRANSMITTER_PORT
)

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
            elif decoded_message.lower().startswith('client'):
                is_transmitted, received_message = await utils.transmit_message_to_dispatcher(
                    addr, decoded_message
                )

                if not is_transmitted:
                    break

                asyncio.create_task(
                    common.write_message(writer, received_message)
                )
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
    await common.create_server(handle_client, TRANSMITTER_HOST, TRANSMITTER_PORT)


try:
    asyncio.run(main())
except KeyboardInterrupt:
    print('Server is shutting down...')
