import asyncio

from json import dumps


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
