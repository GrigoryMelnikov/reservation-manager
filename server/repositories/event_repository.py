import logging
from typing import List

from models.models import Event
from sqlalchemy import select, insert, update, delete
from sqlalchemy.sql import func
from sqlalchemy.orm import Session

from sqlalchemy.exc import IntegrityError

logger = logging.getLogger(__name__)

class EventRepository:
    @staticmethod
    async def get_all_events(db: Session):
        statement = select(Event)
        try:
            return db.execute(statement)
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e
        
    @staticmethod
    async def get_users_events(user_id, db: Session):
        statement = select(Event).filter(Event.owner_id == user_id)
        try:
            return db.execute(statement).all()
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e 

    @staticmethod
    async def get_users_active_events(user_id, db: Session):
        statement = select(Event).filter(Event.owner_id == user_id).filter(Event.t_event > func.now())
        try:
            return db.execute(statement).all()
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e 

    @staticmethod
    async def get_event_by_id(id, db: Session):
        statement = select(Event).filter(Event.id == id)
        try:
            event = db.execute(statement).first()
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e 
        if not event:
            logger.error('Event={id} not found', exc_info=True)
            raise Exception()
        return event
    

    @staticmethod
    async def create(event: Event, db: Session) -> None:
        try:
            # Verbose option of ```db.execute(insert(Event), user)```
            transaction_output = db.scalar(
                insert(Event).returning(Event),
                event
            ) 
            logger.info('New event added: {transaction_output}')
        except IntegrityError as e:
            logger.error(e, exc_info=True)
            raise e
        except Exception as e:
            logger.error(e, exc_info=True)
            raise e
        
    @staticmethod
    async def delete(id, db: Session) -> None:
        try:
            db.execute(delete(Event).where(Event.id == id))
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