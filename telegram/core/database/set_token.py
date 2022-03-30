import asyncio

from .repositories.token import TokenRepository
from .create_table import SessionLocal

from .config import settings


async def set_token(token):
    session = SessionLocal()
    tr = TokenRepository(session)
    await tr.add({"token": token})
    await session.close()


if __name__ == "__main__":
    asyncio.run(set_token(settings.TOKEN))
