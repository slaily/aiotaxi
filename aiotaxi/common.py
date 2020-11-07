# ***-------------***
# *** Synchronous ***
# ***-------------***

def display_connected_client(addr):
    print(f"Client {addr!r} - connected!")


def display_received_message(message, addr):
    print(f"Received {message!r} from {addr!r}")


def get_client_addr(writer):
    addr = writer.get_extra_info('peername')
    client_host, client_port = addr

    return ':'.join([client_host, str(client_port)])


# ***--------------***
# *** Asynchronous ***
# ***--------------***

async def read_message(reader):
    data = await reader.read(100)

    return data.decode()


async def write_message(writer, message):
    writer.write(message)
    await writer.drain()

    return writer


async def close_stream_writer(writer):
    writer.close()
    await writer.wait_closed()

    return None
