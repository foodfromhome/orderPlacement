from api.order.api import router
from fastapi import APIRouter

orders_router = APIRouter(
    prefix="/api/v1",
)

orders_router.include_router(router)
