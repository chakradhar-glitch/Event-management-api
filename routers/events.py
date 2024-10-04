from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import and_

from dependencies.db_dependency import get_db
from dependencies.auth_dependencies import get_current_user
from models.event import Event
from schemas.event import EventBase, EventResponseModel

router = APIRouter()
db_dependency = Annotated[Session, Depends(get_db)]
user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post('/events')
def create_event(event: EventBase, db: db_dependency, current_user: user_dependency):
    try:
        print(current_user)
        if not current_user:
            raise HTTPException(detail=f"could not validate user{current_user}", status_code=401)
        event_model = Event(title=event.title, date=event.date, location=event.location)
        event_model.organiser_id = current_user.get("id")
        db.add(event_model)
        db.commit()

        res = db.query(Event).filter_by(title=event.title).first()
        return JSONResponse(content=f"id:{res.id}", status_code=201)
    except HTTPException as he:
        db.rollback()
        return JSONResponse(content=str(he), status_code=401)
    except Exception as e:
        db.rollback()
        return JSONResponse(content=str(e), status_code=400)


@router.get('/events', response_model=list[EventResponseModel])
def get_all_events(current_user: user_dependency, db: db_dependency):
    try:
        if not current_user:
            raise HTTPException(detail=f"could not validate user{current_user}", status_code=401)
        events = db.query(Event).filter_by(organiser_id=current_user.get('id')).all()
        if not events:
            raise HTTPException(detail=f"events not found for user{current_user.get('id')}")

        return events

    except HTTPException as he:
        db.rollback()
        return JSONResponse(content=str(he), status_code=401)
    except Exception as e:
        db.rollback()
        return JSONResponse(content=str(e), status_code=400)


@router.get('/events/{id}', response_model=EventResponseModel, status_code=200)
def get_event_by_id(id: int, current_user: user_dependency, db: db_dependency):
    try:

        if not current_user:
            raise HTTPException(detail=f"could not validate user{current_user}", status_code=401)
        event_model = db.query(Event).filter(and_(Event.organiser_id == current_user.get('id'), Event.id == id)).first()
        if not event_model:
            return JSONResponse(content='Event not found', status_code=400)
        return event_model
    except HTTPException as he:
        db.rollback()
        return JSONResponse(content=str(he), status_code=401)
    except Exception as e:
        db.rollback()
        return JSONResponse(content=str(e), status_code=400)


@router.put('/events/{id}', response_model=EventResponseModel)
def update_event_by_id(id: int, event: EventBase, current_user: user_dependency, db: db_dependency):
    try:
        if not current_user:
            raise HTTPException(detail=f"could not validate user{current_user}", status_code=401)
        event_model = db.query(Event).filter(Event.id == id).first()
        if not event_model:
            return JSONResponse(content='Event not found', status_code=400)
        if event_model.organiser_id != current_user.get('id'):
            return JSONResponse(content='Only organiser can update event', status_code=400)
        event_model.title = event.title
        event_model.date = event.date
        event_model.location = event.location
        event_model.is_cancelled = event.is_cancelled
        db.commit()
        return event_model

    except HTTPException as he:
        db.rollback()
        return JSONResponse(content=str(he), status_code=401)
    except Exception as e:
        db.rollback()
        return JSONResponse(content=str(e), status_code=400)


@router.delete("/events/{id}")
def delete_event(id: int, current_user: user_dependency, db: db_dependency):
    try:
        if not current_user:
            raise HTTPException(detail=f"could not validate user{current_user}", status_code=401)

        event = db.query(Event).filter_by(id=id).first()
        if event.organiser_id != current_user.get('id'):
            return JSONResponse(content='Only organiser can delete event', status_code=400)
        if not event.is_cancelled:
            event.is_cancelled = True
        db.commit()
        return JSONResponse(content="Event cancelled successfully", status_code=200)

    except HTTPException as he:
        db.rollback()
        return JSONResponse(content=str(he), status_code=401)
    except Exception as e:
        db.rollback()
        return JSONResponse(content=str(e), status_code=400)
