from sqlalchemy.engine import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

# it creates db called users and fetched automaticaly, connect args here is specific to sqllite
SQLALCHEMY_DB_URL = "sqlite:///./users.db"

engine = create_engine(SQLALCHEMY_DB_URL, connect_args={"check_same_thread": False})

sessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
