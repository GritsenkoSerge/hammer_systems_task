class SmsMessage:
    """A container for SMS information."""

    def __init__(self, text: str, to: str, connection=None, **kwargs):
        """Initialize a single SMS message (which can be sent to multiple recipients)."""
        self.text = text or ''
        self.to = to or ''
        self.connection = connection
        self.kwargs = kwargs

    def get_connection(self, fail_silently=False):
        from sms import get_connection

        if not self.connection:
            self.connection = get_connection(fail_silently=fail_silently)
        return self.connection

    def message(self) -> str:
        return self.text

    def recipient(self) -> str:
        return self.to

    def send(self, fail_silently=False):
        """Send the SMS message."""
        if not self.to:
            return 0
        return self.get_connection(fail_silently).send_message(self)
