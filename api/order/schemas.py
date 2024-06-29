from pydantic import BaseModel
from typing import List, Optional
from api.order.models.orders import Items, OrderStatus


class OrderSchema(BaseModel):
    address: str
    city: str
    comment: str
    carts: Optional[List[Items]] = []


class StatusSchema(BaseModel):
    status: OrderStatus
