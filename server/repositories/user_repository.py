import logging
from typing import List

from models.models import User
from sqlalchemy import select, insert, update, delete
from sqlalchemy.orm import Session

from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

class UserRepository:
    @staticmethod
    async def get_all_users(db: Session) -> List[User]:
        statement = select(User)
        try:
            return db.execute(statement).all()
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e
    
    @staticmethod
    async def get_user_by_id(user_id, db: Session) -> User:
        statement = select(User).filter(User.id == user_id)
        try:
            user = db.execute(statement).first()
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e 
        if not user: 
            logger.error('User={mispar_telefon} not found', exc_info=True)
            raise Exception()
        return user
    
    @staticmethod
    async def create(user: User, db: Session) -> None:
        try:
            # Verbose option of ```db.execute(insert(User), user)```
            transaction_output = db.scalar(
                insert(User).returning(User),
                user
            ) 
            logger.info('New user added: {transaction_output}')
        except IntegrityError as e:
            logger.error(e, exc_info=True)
            raise e
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e
    
    @staticmethod
    async def delete(user_id, db: Session) -> None:
        try:
            db.execute(delete(User).where(User.id == user_id))
        except IntegrityError as e:
            logger.error(e, exc_info=True)
            raise e
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e
        
    @staticmethod
    async def update(user_id, db: Session) -> None:
        # TODO
        pass
        # try:
        #     db.execute(delete(User).where(User.id == user_id))
        # except IntegrityError as e:
        #     logger.error(e, exc_info=True)
        #     raise e
        # except Exception as e:
        #     logger.error(e, exc_info=True)
        #     raise e