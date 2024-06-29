import uuid

from config import settings
from yookassa import Configuration, Payment



async def create_payment(value, description):

    Configuration.account_id = settings.yookassa_account_id
    Configuration.secret_key = settings.yookassa_api_key

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
    }, uuid.uuid4())

    return payment["confirmation"]["confirmation_url"]
