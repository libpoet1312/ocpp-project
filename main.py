from datetime import datetime
from pathlib import Path

from fastapi import FastAPI, WebSocket, APIRouter, Depends
from ocpp.routing import on
from ocpp.v16 import call_result
from ocpp.v16.enums import Action, RegistrationStatus
from sqlalchemy.orm import Session

from central_system.centralsystem import on_connect
from helpers.websocketInterface import WebSocketInterface

from db import crud, database
from db.database import SessionLocal, engine

BASE_PATH = Path(__file__).resolve().parent

app = FastAPI(title='Central System rest API')

root_router = APIRouter()

database.Base.metadata.create_all(bind=engine)


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@root_router.get('/')
async def index(db: Session = Depends(get_db)):
    connections = crud.get_ChargePoints(db)
    return {
        'connections': connections
    }


@app.websocket("/ws/{cp_id}")
async def websocket_endpoint(websocket: WebSocket, db: Session = Depends(get_db)):
    interface = WebSocketInterface(websocket)

    await websocket.accept(subprotocol='ocpp1.6')
    try:
        await on_connect(interface, websocket.path_params['cp_id'], db)
        await websocket.close()
    except Exception as e:
        print(e)
        pass
    # else:
    #     try:
    #         await websocket.close()
    #     except RuntimeError:
    #         print(websocket.headers)
    #         print(websocket.path_params)
    #         pass


app.include_router(root_router)