"""Base SMS backend class."""


from sms.message import SmsMessage


class BaseSmsBackend:
    """
    Base class for SMS backend implementations.

    Subclasses must at least overwrite send_message().

    open() and close() can be called indirectly by using a backend object as a
    context manager:

       with backend as connection:
           # do something with connection
           pass
    """

    def __init__(self, fail_silently=False, **kwargs):
        self.fail_silently = fail_silently

    def __enter__(self):
        try:
            self.open_connection()
        except Exception:  # noqa: B902
            self.close_connection()
            raise
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.close_connection()

    def send_message(self, sms_message: SmsMessage):
        """Send one SmsMessage objects and return 1 if sms message sent."""
        raise NotImplementedError(
            'subclasses of BaseSmsBackend must ' 'override send_message() method',
        )

    def open_connection(self):
        """
        Open a network connection.

        This method can be overwritten by backend implementations to
        open a network connection.

        It's up to the backend implementation to track the status of
        a network connection if it's needed by the backend.

        This method can be called by applications to force a single
        network connection to be used when sending SMS.

        The default implementation does nothing.
        """
        ...

    def close_connection(self):
        """Close a network connection."""
        ...
