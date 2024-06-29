from pydantic import BaseModel
from typing import List, Optional
from api.order.models.orders import Items, OrderStatus


class OrderSchema(BaseModel):
    address: str
    city: str
    comment: str



class StatusSchema(BaseModel):
    status: OrderStatus
