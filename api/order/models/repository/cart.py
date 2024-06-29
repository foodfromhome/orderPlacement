import requests


class CartService:
    def __init__(self, base_url: str):
        self.base_url = base_url

    async def get_cart(self, user_id: int) -> dict:
        response = requests.get(f"{self.base_url}/carts/{user_id}")
        response.raise_for_status()
        return response.json()

    async def update_cart(self, user_id: int, cart_data: dict) -> None:
        response = requests.patch(f"{self.base_url}/carts/{user_id}", json=cart_data)
        response.raise_for_status()


cart_repository = CartService(base_url="http://31.128.43.246:8000/api/v1")
