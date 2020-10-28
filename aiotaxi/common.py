async def read_message(reader):
    data = await reader.read(100)

    return data.decode()


async def write_message(writer, message):
    writer.write(message)
    await writer.drain()
    writer.close()

    return writer


def display_connected_client(addr):
    print(f"Client {addr!r} - connected!")


def display_received_message(message, addr):
    print(f"Received {message!r} from {addr!r}")
