import asyncio

from unittest import TestCase
from unittest.mock import patch

import util


class UtilTestCase(TestCase):
    @patch('util.write_message')
    def test_write_message(self, mock_writer):
        mock_writer.return_value = asyncio.StreamWriter
        writer = asyncio.run(util.write_message())

        self.assertIs(writer, asyncio.StreamWriter)
