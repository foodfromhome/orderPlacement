from beanie import Document, PydanticObjectId
from typing import Optional, List
from pydantic import Field, BaseModel
from enum import Enum

from api.order.models.payment_history import PaymentHistory


class OrderStatus(str, Enum):
    PAYMENT = 'Ожидание оплаты'
    NEW = "Новый заказ"
    CONFIRMED = "Заказ подтвержден"
    PREPARING = "Заказ готовится"
    READY_FOR_PICKUP = "Заказ готов к выдаче"
    OUT_FOR_DELIVERY = "Заказ в пути к клиенту"
    DELIVERED = "Заказ доставлен"
    CANCELLED = "Заказ отменен"
    FAILED = "Заказ не может быть выполнен (например, ресторан закрылся)"



class Items(BaseModel):
    meals_id: PydanticObjectId = Field(default_factory=PydanticObjectId)
    quantity: int = Field(..., gt=1)
    price: float = Field(..., gt=0)


class Order(BaseModel):
    id: Optional[PydanticObjectId] = Field(default_factory=PydanticObjectId)
    address: str = Field(...)
    city: str = Field(...)
    items: Optional[List[Items]] = []
    total_price: Optional[float] = 0
    status: OrderStatus = OrderStatus.PAYMENT
    payment_history: Optional[PaymentHistory] = None


class OrdersUser(Document):
    id: PydanticObjectId = Field(default_factory=PydanticObjectId, alias='_id')
    user_id: int = Field(alias='user_id')
    orders: List[Order] = []
