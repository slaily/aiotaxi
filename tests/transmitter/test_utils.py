import asyncio

from unittest import TestCase

from aiotaxi.transmitter import utils


class UtilsTestCase(TestCase):
    def test_format_message_to_send(self):
        addr, message = '127.0.0.1:50127', 'tcase'
        message_to_send = utils.format_message_to_send(addr, message)

        self.assertIsInstance(message_to_send, bytes)
