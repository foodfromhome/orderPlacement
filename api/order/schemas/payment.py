from datetime import datetime

from beanie import PydanticObjectId
from pydantic import BaseModel


class PaymentHistorySchema(BaseModel):
    order_id: PydanticObjectId
    payment_id: str
    payment_status: str
    payment_amount: int
    payment_currency: str
    payment_description: str
    created_at: datetime

    class Config:
        orm_mode = True
