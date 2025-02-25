import asyncio

from unittest import TestCase
from unittest.mock import (
    patch,
    AsyncMock
)

from aiotaxi import common


class CommonTestCase(TestCase):
    def test_write_message(self):
        amock = AsyncMock(spec=asyncio.StreamWriter)
        writer = asyncio.run(common.write_message(amock, b'tcase'))

        amock.drain.assert_awaited_once()

    def test_read_message(self):
        amock = AsyncMock(spec=asyncio.StreamReader)
        reader = asyncio.run(common.read_message(amock))

        amock.read.assert_called_with(100)

    def test_close_stream_writer(self):
        amock = AsyncMock(spec=asyncio.StreamWriter)
        writer = asyncio.run(common.close_stream_writer(amock))

        amock.wait_closed.assert_awaited_once()

    @patch('asyncio.start_server', new=AsyncMock())
    def test_create_server(self):
        args = (lambda x: x, '127.0.0.1', 2222)
        asyncio.run(common.create_server(*args))

        asyncio.start_server.assert_called_once_with(*args)
