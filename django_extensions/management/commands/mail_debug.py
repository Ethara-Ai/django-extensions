import asyncio
import sys

try:
    from aiosmtpd.controller import Controller
except ImportError:
    raise ImportError("Please install 'aiosmtpd' library to use mail_debug command.")

from logging import getLogger
from typing import List

from django.core.management.base import BaseCommand, CommandError

from django_extensions.management.utils import setup_logger, signalcommand

logger = getLogger(__name__)


class CustomHandler:
    async def handle_DATA(self, server, session, envelope):
        """Output will be sent to the module logger at INFO level."""
        pass


class Command(BaseCommand):
    help = "Starts a test mail server for development."
    args = "[optional port number or ippaddr:port]"

    requires_system_checks: List[str] = []

    def add_arguments(self, parser):
        pass

    @signalcommand
    def handle(self, addrport="", *args, **options):
        pass
