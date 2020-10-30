import asyncio


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
