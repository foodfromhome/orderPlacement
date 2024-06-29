from fastapi import APIRouter, HTTPException
from starlette import status
from starlette.responses import JSONResponse

from api.order.models.orders import OrdersUser, Order
from api.order.schemas import OrderSchema, StatusSchema
from beanie import PydanticObjectId
from api.yookassa_api.request import create_payment

from typing import List

router = APIRouter()


@router.post("/{user_id}/orders", status_code=status.HTTP_201_CREATED, summary="Создание заказа",
             response_model=Order)
async def create_order(user_id: int, request: OrderSchema):
    try:
        user_orders = await OrdersUser.find_one({"user_id": user_id})
        if user_orders is None:
            user_orders = OrdersUser(user_id=user_id, orders=[])


        order = Order(
            address=request.address,
            city=request.city,
            items=request.carts,
            total_price=sum(item.price * item.quantity for item in request.carts)
        )

        user_orders.orders.append(order)

        await user_orders.save()

        return order
    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))


@router.get("/{user_id}/orders", response_model=OrdersUser, summary="Возвращает все Orders по пользователю",
            status_code=status.HTTP_200_OK)
async def get_orders_from_user(user_id: int):
    try:

        user_orders = await OrdersUser.find_one({"user_id": user_id})

        if user_orders is None:

            user_orders = OrdersUser(user_id=user_id, orders=[])
            return user_orders

        return user_orders

    except HTTPException as e:

        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))


@router.get("/orders/{order_id}", response_model=Order, summary="Возвращает Order по ID",
            status_code=status.HTTP_200_OK)
async def get_order_id(order_id: PydanticObjectId):
    try:
        user_order = await OrdersUser.find_one({"orders.id": order_id})

        if user_order is None:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        for order in user_order.orders:

            if order.id == order_id:

                return order

    except HTTPException as e:

        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))


@router.delete("/orders/{order_id}", summary="Удаление Order по ID", status_code=status.HTTP_204_NO_CONTENT)
async def delete_order(order_id: PydanticObjectId):
    try:
        user_order = await OrdersUser.find_one({"orders.id": order_id})

        if user_order is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        for order in user_order.orders:
            if order.id == order_id:

                user_order.orders.remove(order)

                await user_order.save()


    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))


@router.put("/orders/{order_id}", summary="Обновление статуса orders", status_code=status.HTTP_200_OK,
            response_model=Order)
async def update_status_order_id(order_id: PydanticObjectId, request: StatusSchema):
    try:

        user_orders = await OrdersUser.find_one({"orders.id": order_id})

        if user_orders is None:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")


        for order in user_orders.orders:

            if order.id == order_id:

                order.status = request.status

                await user_orders.save()

                return order

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))


@router.post("/orders/{order_id}/confirm", summary="Форирование ссылки на оплату",
             status_code=status.HTTP_201_CREATED)
async def confirm_order(order_id: PydanticObjectId):
    try:

        user_orders = await OrdersUser.find_one({"orders.id": order_id})

        if user_orders is None:

            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Order not found")

        for order in user_orders.orders:

            if order.id == order_id:

                url_payment = await create_payment(order.total_price, f"{order.id}\n\n")

                return JSONResponse(status_code=status.HTTP_200_OK,
                                    content={"url": url_payment})

    except HTTPException as e:
        return JSONResponse(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, content=str(e))

