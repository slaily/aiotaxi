import asyncio

from json import dumps

from aiotaxi import common
from aiotaxi import settings


async def establish_ext_serv_conn(host, port):
    reader = None
    writer = None

    try:
        connection_task = asyncio.create_task(
            asyncio.open_connection(host, port)
        )
        reader, writer = await connection_task
    except ConnectionRefusedError as exc:
        print(str(exc))

    return reader, writer


def format_message_to_send(*args):
    addr, message = args
    msg_to_send_dict = {
        'from_addr': addr,
        'message': message
    }

    return dumps(msg_to_send_dict).encode()


async def transmit_message_to_dispatcher(from_addr, message):
    reader, writer = await establish_ext_serv_conn(
        settings.DISPATCHER_HOST, settings.DISPATCHER_PORT
    )

    if not writer:
        return False, b"Sorry, your request cannot be processed at this time!\n"

    message_to_send =format_message_to_send(from_addr, message)
    asyncio.create_task(
        common.write_message(writer, message_to_send)
    )

    if not reader:
        return False, b"Sorry, your request cannot be processed at this time!\n"

    received_message = await common.read_message(reader)
    dispatcher_addr = common.get_client_addr(writer)
    common.display_received_message(received_message, dispatcher_addr)
    asyncio.create_task(common.close_stream_writer(writer))

    return True, received_message.encode()
