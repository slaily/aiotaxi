import asyncio

from unittest import TestCase
from unittest.mock import patch

from aiotaxi import common


class CommonTestCase(TestCase):
    @patch('aiotaxi.common.write_message')
    def test_write_message(self, mock_writer):
        mock_writer.return_value = asyncio.StreamWriter
        writer = asyncio.run(common.write_message())

        self.assertIs(writer, asyncio.StreamWriter)

    @patch('aiotaxi.common.read_message')
    def test_read_message(self, mock_reader):
        mock_reader.return_value = asyncio.StreamReader
        reader = asyncio.run(common.read_message())

        self.assertIs(reader, asyncio.StreamReader)
