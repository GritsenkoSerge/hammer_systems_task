"""SMS backend that writes messages to an API (1C for example)."""
import threading

import requests
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from sms.backends.base import BaseSmsBackend
from sms.message import SmsMessage


class SmsBackend(BaseSmsBackend):
    def __init__(
        self,
        *args,
        api_endpoint=None,
        api_auth_type=None,
        api_token=None,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.api_endpoint = api_endpoint
        if not self.api_endpoint:
            self.api_endpoint = getattr(settings, 'SMS_API_ENDPOINT', None)
        # Make sure self.api_endpoint is a string.
        if not isinstance(self.api_endpoint, str):
            raise ImproperlyConfigured(
                f'Endpoint for saving SMSs is not string: {self.file_path!r}',
            )
        # Make sure that self.file_path is a directory if it exists.
        if not self.api_endpoint:
            raise ImproperlyConfigured(
                'Endpoint for saving SMS messages is empty',
            )
        self.api_auth_type = api_auth_type
        if not self.api_auth_type:
            self.api_auth_type = getattr(settings, 'SMS_API_AUTH_TYPE', None)
        self.api_token = api_token
        if not self.api_token:
            self.api_token = getattr(settings, 'SMS_API_TOKEN', None)
        self._lock = threading.RLock()

    def send_message(self, sms_message: SmsMessage):
        if not sms_message:
            return
        response = None
        with self._lock:
            try:
                params = sms_message.kwargs.get('params', {})
                params['phone'] = sms_message.recipient()
                params['text'] = sms_message.message()
                headers = {}
                auth = self.api_auth_type
                token = self.api_token
                if auth and token:
                    headers['Authorization'] = f'{auth} {token}'
                response = requests.get(
                    self.api_endpoint,
                    headers=headers,
                    params=params,
                )
            except Exception:  # noqa: B902
                if not self.fail_silently:
                    raise
        return response
