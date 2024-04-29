from typing import List
from uuid import uuid4

from faker import Faker
from sqlalchemy.orm import Session

from models.models import User
from repositories.user_repository import UserRepository


class UserFactory:
    '''Generates Users in the DB'''

    def __init__(self) -> None:
        self.users: List[User] = list()

    async def _create_user(self, db: Session):
        f = Faker()
        new_user = User(
            email=f.ascii_email(),
            mispar_telefon=f.phone_number(),
            first_name=f.first_name_nonbinary(),
            last_name=f.phone_number(),
            ind_contact_me=f.boolean(),
        )
        # await UserRepository.create(new_user, db)
        self.users.append(new_user)

    async def bulk_create(self, db: Session, num: int) -> List[User]:
        '''Creates `int` objects of class `User` in DB'''
        for i in range(num):
            await self._create_user(db)
        await UserRepository.create_bulk(self.users, db)
        return self.users
