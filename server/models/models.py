from sqlalchemy import Column, PrimaryKeyConstraint
from sqlalchemy.schema import ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import BOOLEAN, VARCHAR, INTEGER, TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, relationship

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = 'users'
    # id  = Column(INTEGER, primary_key=True, unique=True, autoincrement=True)
    email = Column(VARCHAR, nullable=False, unique=True)
    mispar_telefon = Column(VARCHAR, primary_key=True)
    first_name = Column(VARCHAR, nullable=False)
    last_name = Column(VARCHAR, nullable=False)
    # role_id = Column(INTEGER, ForeignKey("roles.id"))
    ind_contact_me = Column(BOOLEAN, nullable=False)
    t_created = Column(TIMESTAMP, nullable=False, server_default=func.now())

    user_guests = relationship('Guest', backref='users', lazy=True, cascade="all")
    user_events = relationship('Event', backref='users', lazy=True, cascade="all")
    user_tguser = relationship('TgUsers', backref='user', lazy=True, cascade="all")


class Event(Base):
    __tablename__ = 'events'
    id = Column(INTEGER, primary_key=True, unique=True, autoincrement=True)
    user_telefon = Column(VARCHAR, ForeignKey("users.mispar_telefon"))
    mispar_ishur = Column(VARCHAR, nullable=False)
    type_id = Column(INTEGER, ForeignKey("event_type.id"))
    size_id = Column(INTEGER, ForeignKey("event_size.id"))
    tg_token = Column(VARCHAR, nullable=False, unique=True)
    t_event = Column(TIMESTAMP, nullable=False)

    event_guest = relationship('Guest', backref='events', lazy=True, cascade="all")
    event_tg_user = relationship('TgUsers', backref='events', lazy=True, cascade="all")


class TgUsers(Base):
    __tablename__ = 'tg_users'
    __table_args__ = (
        PrimaryKeyConstraint('id', 'token'),
    )
    id = Column(INTEGER, nullable=False)
    mispar_telefon = Column(VARCHAR, ForeignKey("users.mispar_telefon"))
    token = Column(VARCHAR, ForeignKey('events.tg_token'))


class Guest(Base):
    __tablename__ = 'guests'
    __table_args__ = (
        PrimaryKeyConstraint('event_id', 'mispar_telefon'),
    )
    name = Column(VARCHAR, nullable=False)
    event_id = Column(INTEGER, ForeignKey('events.id'))
    added_by = Column(VARCHAR, ForeignKey('users.mispar_telefon'))
    mispar_telefon = Column(VARCHAR, nullable=False)
    ind_arriving = Column(BOOLEAN, nullable=False)
    arriving_with = Column(INTEGER, server_default='0')

class EventType(Base):
    __tablename__ = 'event_type'
    id = Column(INTEGER, primary_key=True, unique=True, autoincrement=True)
    type_name = Column(VARCHAR)
    ind_active = Column(BOOLEAN, nullable=False)

class EventSize(Base):
    __tablename__ = 'event_size'
    id = Column(INTEGER, primary_key=True, unique=True, autoincrement=True)
    size = Column(INTEGER, nullable=False)
    price = Column(INTEGER, nullable=False)
    ind_active = Column(BOOLEAN, nullable=False)
