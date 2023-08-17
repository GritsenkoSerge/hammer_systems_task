from typing import Optional

from django.conf import settings
from django.utils.module_loading import import_string

from sms.backends.base import BaseSmsBackend
from sms.message import SmsMessage


def get_connection(backend=None, fail_silently=False, **kwargs):
    """Load an SMS backend and return an instance of it.

    If backend is None (default), use settings.SMS_BACKEND.

    Both fail_silently and other keyword arguments are used in the
    constructor of the backend.
    """
    klass = import_string(backend or settings.SMS_BACKEND)
    return klass(fail_silently=fail_silently, **kwargs)


def send_sms(
    message: str,
    recipient: str,
    connection: Optional[BaseSmsBackend] = None,
    **kwargs,
):
    """Easy wrapper for sending a single message to a recipient."""
    connection = connection or get_connection(
        fail_silently=kwargs.get('fail_silently'),
    )
    sms = SmsMessage(message, recipient, connection=connection, **kwargs)

    return sms.send()
