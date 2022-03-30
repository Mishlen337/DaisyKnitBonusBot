from sqlalchemy.ext.asyncio.session import AsyncSession
from sqlalchemy.sql.expression import select, delete
from typing import Optional, List, Union

from ..create_table import User


class UserRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(
        self,
        tg_chat_id: Optional[int] = "",
        email: Optional[str] = "",
        is_admin: Optional[bool] = "",
    ) -> List[Optional[dict]]:
        """The function of getting all users from the User table.

        :param email: users email
        :type email: str | None

        :param phone: user's phone number
        :type phone: str

        :param is_admin: parameter indicating the presence of admin rights (replace None with False)
        :type is_admin: bool | None

        :param tg_chat_id: user's tg chat id
        :type tg_chat_id: int | None

        :return: list of dictionaries - json format of the requested object
        :rtype: List[dict | None]

        """

        query = select(User)

        if email != "" and email is not None:
            query = query.where(User.email == email)

        if is_admin != "" and is_admin is not None:
            query = query.where(User.is_admin == is_admin)

        if tg_chat_id != "":
            query = query.where(User.tg_chat_id == tg_chat_id)

        users = [
            {
                "email": user.email,
                "is_admin": user.is_admin,
                "tg_chat_id": user.tg_chat_id,
            }
            for user in (await self.session.execute(query)).scalars()
        ]

        return users

    async def get_one(
        self,
        email: Optional[str] = "",
        is_admin: Optional[bool] = "",
        tg_chat_id: Optional[int] = "",
    ) -> Optional[dict]:
        """The function of getting one user from the User table.

        :param email: users email
        :type email: str | None

        :param is_admin: parameter indicating the presence of admin rights (replace None with False)
        :type is_admin: bool | None

        :param tg_chat_id: user's tg chat id
        :type tg_chat_id: int | None

        :return: dictionary - json format of the requested object; or nothing
        :rtype: dict | None

        """

        users = await self.get_all(email=email, is_admin=is_admin, tg_chat_id=tg_chat_id)

        if users and users[0]:
            return users[0]
        return None

    async def delete(
        self,
        email="",
        is_admin: Optional[bool] = "",
        tg_chat_id: Optional[int] = "",
    ) -> None:
        """The function of deleting users from the User table.

        :param email: users email
        :type email: str

        :param is_admin: parameter indicating the presence of admin rights (replace None with False)
        :type is_admin: bool | None

        :param tg_chat_id: user's tg chat id
        :type tg_chat_id: int | None

        :return: nothing
        :rtype: None

        """

        query = delete(User)

        if email != "":
            query = query.where(User.email == email)

        if is_admin != "":
            if is_admin is None:
                is_admin = False
            query = query.where(User.is_admin == is_admin)

        if tg_chat_id != "":
            query = query.where(User.tg_chat_id == tg_chat_id)

        await self.session.execute(query)
        await self.session.commit()

        return None

    async def add(self, users: Union[dict, List[dict]]) -> Union[dict, List[dict]]:
        """The function of adding users to the User table.

        :param users: dictionary or list of dictionaries - json format of the received objects
        :type users: dict | List[dict]

        :return: dictionary or list of dictionaries - json format of the received objects
        :rtype: dict | List[dict]

        """

        query = select(User).distinct()
        tg_chat_ids = {user.tg_chat_id for user in (await self.session.execute(query)).scalars()}

        if type(users) == dict:
            users = [users]

        return_users = []

        for user in users:
            params = {}

            if "email" in user.keys():
                params["email"] = user["email"]
            else:
                params["email"] = None

            if "is_admin" in user.keys():
                params["is_admin"] = user["is_admin"]
            else:
                params["is_admin"] = False

            if "tg_chat_id" in user.keys():
                if user["tg_chat_id"] not in tg_chat_ids or user["tg_chat_id"] is None:
                    params["tg_chat_id"] = user["tg_chat_id"]
                    tg_chat_ids.add(user["tg_chat_id"])
                else:
                    raise ValueError(
                        f"Unable to add new user with parameter "
                        f'tg_chat_id="{user["tg_chat_id"]}" '
                        f"because this tg_chat_id already exists."
                    )
            else:
                raise ValueError(
                    f"Unable to add new user " f'because a parameter "tg_chat_id" does not exist.'
                )

            self.session.add(User(**params))
            tg_chat_ids.add(params["tg_chat_id"])

            await self.session.commit()
            return_users.append(params)

        if len(return_users) == 1:
            return_users = return_users[0]

        return return_users

    async def update(
        self,
        email="",
        is_admin: Optional[bool] = "",
        tg_chat_id: Optional[int] = "",
        new_email="",
        new_is_admin: Optional[bool] = "",
        new_tg_chat_id: Optional[int] = "",
    ) -> None:
        """The function of updating users in the User table.

        :param email: users email
        :type email: str

        :param is_admin: parameter indicating the presence of admin rights (replace None with False)
        :type is_admin: bool | None

        :param tg_chat_id: user's tg chat id
        :type tg_chat_id: int | None

        :param new_email: users email
        :type new_email: str

        :param new_is_admin: new parameter indicating the presence of admin rights
                             (replace None with False)
        :type new_is_admin: bool | None

        :param new_tg_chat_id: user's new tg chat id
        :type new_tg_chat_id: int | None

        :return: nothing
        :rtype: None

        """

        params = dict()
        query = select(User)

        if email != "":
            params["email"] = email
            query = query.where(User.email == email)

        if is_admin != "":
            if is_admin is None:
                is_admin = False
            params["is_admin"] = is_admin
            query = query.where(User.is_admin == is_admin)

        if tg_chat_id != "":
            params["tg_chat_id"] = tg_chat_id
            query = query.where(User.tg_chat_id == tg_chat_id)

        if not params:
            return

        users = (await self.session.execute(query)).scalars()

        query = select(User).distinct()
        tg_chat_ids = {user.tg_chat_id for user in (await self.session.execute(query)).scalars()}

        for user in users:

            if new_email != "":
                user.email = new_email

            if new_is_admin != "":
                user.is_admin = new_is_admin

            if new_tg_chat_id != "":
                if new_tg_chat_id == None or new_tg_chat_id not in tg_chat_ids:
                    tg_chat_ids.remove(user.tg_chat_id)
                    user.tg_chat_id = new_tg_chat_id
                    tg_chat_ids.add(new_tg_chat_id)
                else:
                    ValueError(
                        f"Unable to update the value in user "
                        f"because user with this "
                        f'tg_chat_id="{new_tg_chat_id}" already exists.'
                    )

            await self.session.commit()
