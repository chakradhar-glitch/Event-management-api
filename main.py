from fastapi import FastAPI, HTTPException
from routers.auth import router as auth_router
from routers.events import router as event_router
from routers.guest import router as guest_router
from database.database import Base, engine
from dotenv import load_dotenv

app = FastAPI(title='EventManagement', description='An App to serve your event management needs')

app.include_router(auth_router)
app.include_router(event_router)
app.include_router(guest_router)

Base.metadata.create_all(bind=engine)
load_dotenv()


@app.get('/')
def root():
    return {"detail": "Nothing to serve at root"}
