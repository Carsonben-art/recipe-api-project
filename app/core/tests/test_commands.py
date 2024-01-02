from unittest.mock import patch
from django.core.management import call_command
from django.test import SimpleTestCase
from django.db.utils import OperationalError
from psycopg2 import OperationalError as Psycopg2OpError  # noqa: F401
import time  # noqa: F401


class CommandTests(SimpleTestCase):
    """Test commands here."""

    @patch('core.management.commands.wait_for_db.connections')
    def test_wait_for_db_ready(self, mocked_connections):
        """Test waiting for database if ready."""
        mocked_connections.__getitem__.return_value = {}
        mocked_connections['default'] = True

        call_command('wait_for_db')

        mocked_connections.__getitem__.assert_called_once_with('default')

    @patch('core.management.commands.wait_for_db.connections')
    @patch('time.sleep')
    def test_wait_for_db_delay(self, patched_sleep, mocked_connections):
        """Test waiting for database when getting OperationalError"""
        side_effect = [OperationalError, OperationalError, True]
        mocked_connections.__getitem__.side_effect = side_effect

        call_command('wait_for_db')

        self.assertEqual(mocked_connections.__getitem__.call_count, 3)
        mocked_connections.__getitem__.assert_called_with('default')
