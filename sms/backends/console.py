"""SMS backend that writes messages to console instead of sending them."""
import sys
import threading

from sms.backends.base import BaseSmsBackend
from sms.message import SmsMessage


class SmsBackend(BaseSmsBackend):
    def __init__(self, *args, **kwargs):
        self.stream = kwargs.pop('stream', sys.stdout)
        self._lock = threading.RLock()
        super().__init__(*args, **kwargs)

    def write_message(self, message: SmsMessage):
        self.stream.write(
            '{0}\n{1}\n{2} {3}\n{4}\n'.format(
                '-' * 79,
                message.message(),
                message.recipient(),
                message.kwargs,
                '-' * 79,
            ),
        )

    def send_message(self, sms_message: SmsMessage):
        """Write all messages to the stream in a thread-safe way."""
        if not sms_message:
            return
        msg_count = 0
        with self._lock:
            try:
                stream_created = self.open_connection()
                self.write_message(sms_message)
                self.stream.flush()  # flush after each message
                msg_count += 1
                if stream_created:
                    self.close_connection()
            except Exception:  # noqa: B902
                if not self.fail_silently:
                    raise
        return msg_count
