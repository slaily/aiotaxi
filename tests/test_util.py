import asyncio

from unittest import TestCase
from unittest.mock import patch

from aiotaxi import util


class UtilTestCase(TestCase):
    @patch('aiotaxi.util.write_message')
    def test_write_message(self, mock_writer):
        mock_writer.return_value = asyncio.StreamWriter
        writer = asyncio.run(util.write_message())

        self.assertIs(writer, asyncio.StreamWriter)

    @patch('aiotaxi.util.read_message')
    def test_read_message(self, mock_reader):
        mock_reader.return_value = asyncio.StreamReader
        reader = asyncio.run(util.read_message())

        self.assertIs(reader, asyncio.StreamReader)
