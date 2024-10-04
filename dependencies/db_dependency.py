from database.database import sessionLocal
from sqlalchemy.orm import Session


def get_db():
    try:
        db = sessionLocal()
        yield db
    finally:
        db.close()
