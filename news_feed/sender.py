import os
from typing import Iterable

from twilio.rest import Client


def send_whatsapp_messages(messages: Iterable[str]) -> None:
    account_sid = required_env("TWILIO_ACCOUNT_SID")
    auth_token = required_env("TWILIO_AUTH_TOKEN")
    from_number = required_env("TWILIO_WHATSAPP_FROM")
    to_number = required_env("WHATSAPP_TO")

    client = Client(account_sid, auth_token)
    for message in messages:
        client.messages.create(body=message, from_=from_number, to=to_number)


def required_env(name: str) -> str:
    value = os.getenv(name)
    if not value:
        raise RuntimeError(f"Missing required environment variable: {name}")
    return value
