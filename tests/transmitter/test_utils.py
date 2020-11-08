import asyncio

from unittest import TestCase
from unittest.mock import (
    patch,
    AsyncMock
)

from aiotaxi.transmitter import utils


class UtilsTestCase(TestCase):
    def test_format_message_to_send(self):
        addr, message = '127.0.0.1:50127', 'tcase'
        message_to_send = utils.format_message_to_send(addr, message)

        self.assertIsInstance(message_to_send, bytes)

    @patch('asyncio.open_connection', new=AsyncMock)
    @patch('asyncio.create_task', new_callable=AsyncMock)
    def test_establish_ext_serv_conn(self, amock_create_task):
        amock_create_task.return_value = None, None
        asyncio.run(utils.establish_ext_serv_conn('127.0.0.1', 1111))

        amock_create_task.assert_awaited()
