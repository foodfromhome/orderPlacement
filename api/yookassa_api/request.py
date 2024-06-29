import asyncio
import json
import uuid

from config import settings
from yookassa import Configuration, Payment



async def create_payment(value, description):

    Configuration.account_id = settings.yookassa_account_id
    Configuration.secret_key = settings.yookassa_api_key

    payment_id = uuid.uuid4()

    payment = Payment.create({
        "amount": {
            "value": value,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": "https://www.example.com/return_url"
        },
        "capture": True,
        "description": description
    }, payment_id)

    return payment["confirmation"]["confirmation_url"], payment['id']


async def check_payment(payment_id):

    Configuration.account_id = settings.yookassa_account_id
    Configuration.secret_key = settings.yookassa_api_key

    payment = json.loads((Payment.find_one(payment_id)).json())

    return payment['status']
