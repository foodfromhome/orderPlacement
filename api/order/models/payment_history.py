from datetime import datetime

from pydantic import BaseModel


class PaymentHistory(BaseModel):
    payment_id: str
    payment_url: str
    payment_status: str
    payment_amount: int
    payment_currency: str
    payment_description: str
    created_at: datetime = datetime.utcnow()
