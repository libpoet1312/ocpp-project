"""
This file is used for CRUD and other database operations
"""
from sqlalchemy.orm import Session

from db.database import SessionLocal
from models.ChargePoint import ChargePoint


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_update_ChargePoint_db(cp):
    db = SessionLocal()
    if not db.query(ChargePoint).get(cp.cp_id):
        db.add(cp)
    db.commit()
    db.refresh(cp)


def get_ChargePoints(db: Session):
    return db.query(ChargePoint).all()


def create_ChargePoint(cp_id):
    pass
