from prisma import Prisma
from reviewturtl.settings import get_settings


settings = get_settings()


class TurtlPrismaClient:
    _instance = None

    async def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            await cls._instance._init_client()
        return cls._instance

    async def _init_client(self):
        self.client = Prisma()
        await self.client.connect()

    async def get_client(self):
        return self.client

    async def disconnect(self):
        await self.client.disconnect()


async def get_prisma_client():
    prisma_client = await TurtlPrismaClient()
    return await prisma_client.get_client()


# Usage example
# asyncio.run(get_prisma_client())
