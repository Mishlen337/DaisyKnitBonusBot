"""import sys, os

# initial directory
cwd = os.getcwd()
os.chdir(cwd + "/telegram")
print("Current directory is-", cwd + "/telegram")
"""
import asyncio

from repositories.user import UserRepository
from repositories.token import TokenRepository
from create_table import SessionLocal


async def test_insert(chat_id):
    session = SessionLocal()
    ur = UserRepository(session)
    await ur.add({"tg_chat_id": chat_id})
    assert (await ur.get_one(tg_chat_id=chat_id))["tg_chat_id"] == chat_id
    await session.close()


async def test_insert_email(chat_id, email):
    session = SessionLocal()
    ur = UserRepository(session)
    # us = ur.get_one(tg_chat_id=chat_id)
    await ur.update(tg_chat_id=chat_id, new_email=email)
    assert (await ur.get_one(tg_chat_id=chat_id))["email"] == email
    await session.close()


async def test_token(token):
    session = SessionLocal()
    tr = TokenRepository(session)
    await tr.add({"token": token})
    assert (await tr.get_one(token=token))["token"] == token
    await session.close()


async def test_deletion_user(chat_id):
    session = SessionLocal()
    ur = UserRepository(session)
    await ur.delete(tg_chat_id=chat_id)


async def test_deletion_token(token):
    session = SessionLocal()
    tr = TokenRepository(session)
    await tr.delete(token=token)


async def test_all():
    await test_insert(13145)
    await test_insert_email(13145, "jsdsd")
    await test_token("fdhsjass")
    await test_deletion_user(13145)
    await test_deletion_token("fdhsjass")

    print("TEST OK!")


if __name__ == "__main__":
    asyncio.run(test_all())
