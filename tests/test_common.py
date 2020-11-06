import asyncio

from unittest import TestCase
from unittest.mock import AsyncMock

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
