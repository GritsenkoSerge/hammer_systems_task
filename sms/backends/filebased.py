"""SMS backend that writes messages to a file."""

import datetime
import os

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from sms.backends.console import SmsBackend as ConsoleSmsBackend
from sms.message import SmsMessage


class SmsBackend(ConsoleSmsBackend):
    def __init__(self, *args, file_path=None, **kwargs):
        self._fname = None
        if file_path is not None:
            self.file_path = file_path
        else:
            self.file_path = getattr(settings, 'SMS_FILE_PATH', None)
        # Make sure self.file_path is a string.
        if not isinstance(self.file_path, str):
            raise ImproperlyConfigured(
                f'Path for saving SMSs is invalid: {self.file_path!r}',
            )
        self.file_path = os.path.abspath(self.file_path)
        # Make sure that self.file_path is a directory if it exists.
        if os.path.exists(self.file_path) and not os.path.isdir(self.file_path):
            raise ImproperlyConfigured(
                'Path for saving SMS messages exists, '
                f'but is not a directory: {self.file_path}',
            )
        # Try to create it, if it not exists.
        elif not os.path.exists(self.file_path):
            try:
                os.makedirs(self.file_path)
            except OSError as err:
                raise ImproperlyConfigured(
                    'Could not create directory for saving '
                    f'SMS messages: {self.file_path} ({err})',
                )
        # Make sure that self.file_path is writable.
        if not os.access(self.file_path, os.W_OK):
            raise ImproperlyConfigured(f'Could not write to directory: {self.file_path}')
        # Finally, call super().
        # Since we're using the console-based backend as a base,
        # force the stream to be None, so we don't default to stdout
        kwargs['stream'] = None
        super().__init__(*args, **kwargs)

    def write_message(self, message: SmsMessage):
        self.stream.write(
            '{0}\n{1} {2}\n{3}\n'.format(
                message.message(),
                message.recipient(),
                message.kwargs,
                '-' * 79,
            ).encode(),
        )

    def open_connection(self):
        if self.stream is None:
            self.stream = open(self._get_filename(), 'ab')
            return True
        return False

    def close_connection(self):
        try:
            if self.stream is not None:
                self.stream.close()
        finally:
            self.stream = None

    def _get_filename(self):
        """Return a unique file name."""
        if self._fname is None:
            timestamp = datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
            fname = f'{timestamp}-{abs(id(self))}.log'
            self._fname = os.path.join(self.file_path, fname)
        return self._fname
