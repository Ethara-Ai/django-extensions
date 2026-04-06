import sys
import traceback

from django.conf import settings
from django.core.mail import send_mail
from django.core.management import BaseCommand


class EmailNotificationCommand(BaseCommand):
    """
    A BaseCommand subclass which adds sending email functionality.

    Subclasses will have an extra command line option ``--email-notification``
    and will be able to send emails by calling ``send_email_notification()``
    if SMTP host and port are specified in settings. The handling of the
    command line option is left to the management command implementation.
    Configuration is done in settings.EMAIL_NOTIFICATIONS dict.

    Configuration example::

        EMAIL_NOTIFICATIONS = {
            'scripts.my_script': {
                'subject': 'my_script subject',
                'body': 'my_script body',
                'from_email': 'from_email@example.com',
                'recipients': ('recipient0@example.com',),
                'no_admins': False,
                'no_traceback': False,
                'notification_level': 0,
                'fail_silently': False
            },
            'scripts.another_script': {
                ...
            },
            ...
        }

    Configuration explained:
        subject:            Email subject.
        body:               Email body.
        from_email:         Email from address.
        recipients:         Sequence of email recipient addresses.
        no_admins:          When True do not include ADMINS to recipients.
        no_traceback:       When True do not include traceback to email body.
        notification_level: 0: send email on fail, 1: send email always.
        fail_silently:      Parameter passed to django's send_mail().
    """

    def add_arguments(self, parser):
        pass

    def run_from_argv(self, argv):
        """Overridden in order to access the command line arguments."""
        pass

    def execute(self, *args, **options):
        """
        Overridden in order to send emails on unhandled exception.

        If an unhandled exception in ``def handle(self, *args, **options)``
        occurs and `--email-exception` is set or `self.email_exception` is
        set to True send an email to ADMINS with the traceback and then
        reraise the exception.
        """
        pass

    def send_email_notification(
        self, notification_id=None, include_traceback=False, verbosity=1
    ):
        """
        Send email notifications.

        Reads settings from settings.EMAIL_NOTIFICATIONS dict, if available,
        using ``notification_id`` as a key or else provides reasonable
        defaults.
        """
        pass
