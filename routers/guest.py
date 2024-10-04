from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import and_

from dependencies.db_dependency import get_db
from dependencies.auth_dependencies import get_current_user
from schemas.event import Guest, EventBase
from schemas.user import UserResponseModel
from models.event import Event
from models.user import User

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post('/events/{id}/guests')
def add_guest(id: int, payload: Guest, db: db_dependency, current_user: user_dependency):
    try:
        if not current_user:
            raise HTTPException(detail=f"could not validate user{current_user}", status_code=401)
        event_model = db.query(Event).filter(and_(Event.organiser_id == current_user.get('id'), Event.id == id)).first()
        if not event_model:
            return JSONResponse(content="Event not found")
        user_model = db.query(User).filter_by(name=payload.name).first()
        event_model.guests.append(user_model)
        db.commit()

    except HTTPException as he:
        db.rollback()
        return JSONResponse(content=str(he), status_code=401)
    except Exception as e:
        db.rollback()
        return JSONResponse(content=str(e), status_code=400)


@router.get('/events/{id}/guests', response_model=list[UserResponseModel])
def get_guest_list_by_id(id: int, db: db_dependency, current_user: user_dependency):
    try:
        if not current_user:
            raise HTTPException(detail=f"could not validate user{current_user}", status_code=401)
        event_model = db.query(Event).filter(and_(Event.organiser_id == current_user.get('id'), Event.id == id)).first()
        if not event_model:
            return JSONResponse(content="Event not found")

        if not event_model.guests:
            return JSONResponse(content='Event doesnt have guests')
        return event_model.guests

    except HTTPException as he:
        db.rollback()
        return JSONResponse(content=str(he), status_code=401)
    except Exception as e:
        db.rollback()
        return JSONResponse(content=str(e), status_code=400)


@router.delete('/events/{id}/guests/{guest_id}')
def delete_guest(id: int,guest_id:int, db: db_dependency, current_user: user_dependency):
    try:
        if not current_user:
            raise HTTPException(detail=f"could not validate user{current_user}", status_code=401)
        event = db.query(Event).filter(and_(Event.organiser_id == current_user.get('id'), Event.id == id)).first()
        if not event:
            return JSONResponse(content="event not found")

        user_model = db.query(User).filter_by(id=guest_id).first()
        event.guests.remove(user_model)
        db.commit()
    except HTTPException as he:
        db.rollback()
        return JSONResponse(content=str(he), status_code=401)
    except Exception as e:
        db.rollback()
        return JSONResponse(content=str(e), status_code=400)
