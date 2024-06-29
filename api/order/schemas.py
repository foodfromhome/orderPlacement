from pydantic import BaseModel
from typing import List, Optional
from api.order.models.orders import Items


class OrderSchema(BaseModel):
    address: str
    city: str
    comment: str
    carts: Optional[List[Items]] = []
