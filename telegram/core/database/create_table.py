import asyncio

from sqlalchemy.ext.asyncio.engine import create_async_engine
from sqlalchemy.sql.sqltypes import String, Boolean, BigInteger, DateTime
from sqlalchemy.sql.schema import Column, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio.session import AsyncSession

from .config import settings


convention = {
    "all_column_names": lambda constraint, table: "_".join(
        [column.name for column in constraint.columns.values()]
    ),
    "ix": "ix__%(table_name)s__%(all_column_names)s",
    "uq": "uq__%(table_name)s__%(all_column_names)s",
    "ck": "ck__%(table_name)s__%(constraint_name)s",
    "fk": ("fk__%(table_name)s__%(all_column_names)s__" "%(referred_table_name)s"),
    "pk": "pk__%(table_name)s",
}

engine = create_async_engine(
    settings.DB_PATH,
    # connect_args={"check_same_thread": False},  # use this with SQLite
    # echo=True,
)

SessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine, expire_on_commit=False, class_=AsyncSession
)

meta = MetaData(naming_convention=convention)
Base = declarative_base(metadata=meta)


class User(Base):
    """Object in the user table in db.

    tg_chat_id – user's tg chat id
    email – unique id
    is_admin – parameter indicating the presence of admin rights
    """

    __tablename__ = "user"
    tg_chat_id = Column(BigInteger, primary_key=True)
    email = Column(String, nullable=True)
    is_admin = Column(Boolean, default=False, nullable=False)


class Token(Base):
    """Object in the token table in db.

    token – key to activate a person in the database
    vacant – parameter indicating the ability to activate the token

    """

    __tablename__ = "token"

    token = Column(String, primary_key=True)
    # uid = Column(
    #     String, ForeignKey(User.uid, onupdate="cascade", ondelete="cascade"), nullable=False
    # )
    vacant = Column(Boolean, default=True, nullable=False)


# create tables
async def update_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    print("DB - OK")
    return 0


if __name__ == "__main__":
    # uncomment to test all db functions
    asyncio.run(update_tables())
