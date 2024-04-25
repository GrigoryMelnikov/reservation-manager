from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from pydantic_settings import BaseSettings
from dotenv import find_dotenv, load_dotenv, get_key
from pydantic import ValidationError

class DbBaseSettings(BaseSettings):
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_name: str
    pgadmin_default_email: str
    pgadmin_default_password: str

class DbSettings(DbBaseSettings):
    class Config:
        env_file = ".env.database"

def get_setting() -> DbSettings:
    """
    First try to get env values from .env file.
    Pydantic will only check the current working directory and won't check any parent directories for the .env.database file.
    If pydantic does not find the file dotenv library will search the file in parent directories,
    If it finds the file the values will be loaded and then set with os.getenv method.
    """
    try:
        return DbSettings()
    except ValidationError:
        db_env_file_path = find_dotenv(".env.database", True)
        load_dotenv(db_env_file_path)
        return DbBaseSettings(
            postgres_host=get_key(key_to_get="POSTGRES_HOST", dotenv_path=db_env_file_path),
            postgres_port=get_key(key_to_get="POSTGRES_PORT", dotenv_path=db_env_file_path),
            postgres_user=get_key(key_to_get="POSTGRES_USER"), dotenv_path=db_env_file_path,
            postgres_password=get_key(key_to_get="POSTGRES_PASSWORD", dotenv_path=db_env_file_path),
            postgres_name=get_key(key_to_get="POSTGRES_NAME", dotenv_path=db_env_file_path),
            pgadmin_default_email=get_key(key_to_get="PGADMIN_DEFAULT_EMAIL", dotenv_path=db_env_file_path),
            pgadmin_default_password=get_key(key_to_get="PGADMIN_DEFAULT_PASSWORD", dotenv_path=db_env_file_path)
        )

# Get DB credentials from .env.database file
DB_CREDENTIALS: DbSettings = get_setting()

SQLALCHEMY_DATABASE_URL = "postgresql://%s:%s@%s:%s/%s" % (
    DB_CREDENTIALS.postgres_user,
    DB_CREDENTIALS.postgres_password,
    DB_CREDENTIALS.postgres_host,
    DB_CREDENTIALS.postgres_port,
    DB_CREDENTIALS.postgres_name
)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=10,
    max_overflow=20
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_engine():
    return engine