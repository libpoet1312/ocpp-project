import asyncio
import uuid
from datetime import datetime

from fastapi import Depends
from ocpp.charge_point import LOGGER
from ocpp.routing import on
from ocpp.v16 import ChargePoint as Base_ChargePoint
from ocpp.v16 import call_result
from ocpp.v16.enums import Action, RegistrationStatus

from db.database import Base, SessionLocal
from sqlalchemy import Boolean, Column, Text, String, DateTime, func

from helpers.websocketInterface import WebSocketInterface


class ChargePoint(Base_ChargePoint, Base):
    __tablename__ = "chargepoints"
    id = Column(Text, primary_key=True, index=True)
    cp_id = Column(String)
    host = Column(String)
    user_agent = Column(String)
    is_online = Column(Boolean, default=True)
    is_connected = Column(Boolean, default=False)

    created_at = Column(DateTime, default=func.now())
    updated_at = Column(DateTime, onupdate=func.utc_timestamp())

    def __init__(self, charger_id: str, connection: WebSocketInterface, response_timeout=30):
        """
        Args:

            charger_id (str): ID of the charger.
            connection: Connection to CP.
            response_timeout (int): When no response on a request is received
                within this interval, an asyncio.TimeoutError is raised.

        """
        super().__init__(charger_id, connection, response_timeout)
        self.cp_id = str(charger_id)
        self.host = connection.websocket.headers['host']
        self.user_agent = connection.websocket.headers['user-agent']

    async def start(self):
        while True:
            try:
                message = await self._connection.recv()
                if 'disconnected' in message:
                    LOGGER.info('Charger %s: disconnected', self.id)
                    return

                LOGGER.info('%s: receive message %s', self.id, message)
                await self.route_message(message)
            except Exception as e:
                print(e)
                await self._connection.close()

    @on(Action.BootNotification)
    def on_boot_notification(self, charge_point_vendor: str, charge_point_model: str, **kwargs):
        print(charge_point_vendor)
        print(charge_point_model)
        print(kwargs)

        t = datetime.utcnow().isoformat()
        return call_result.BootNotificationPayload(
            current_time=t + 'Z',
            interval=10,
            status=RegistrationStatus.accepted
        )