"""
Django command to wait for the database to be available.
"""
import time

from django.db import connections
from psycopg2 import OperationalError as Psycopg2OpError

from django.db.utils import OperationalError

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """Django command to wait for database."""

    def handle(self, *args, **options):
        """Entry point for command"""

        self.stdout.write('waiting for database')
        db_conn = None
        while not db_conn:
            try:

                db_conn = connections['default']
                db_conn = True

            except (Psycopg2OpError, OperationalError):

                self.stdout.write('Database Unavailable, waiting 1 sec...')
                time.sleep(1)

        self.stdout.write(self.style.SUCCESS('Database Available!'))
