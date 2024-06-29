from config import settings
import motor.motor_asyncio


# DATABASE_URL = (f"mongodb://{settings.mongo_username}:{settings.mongo_password}@"
#                 f"{settings.mongo_host}:{settings.mongo_port}")

DATABASE_URL = f"mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(
    DATABASE_URL, uuidRepresentation="standard"
)


db = client[f'{settings.mongo_db}']
