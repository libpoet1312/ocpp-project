import logging

from sqlalchemy.orm import Session

from db.crud import create_update_ChargePoint_db
from models.ChargePoint import ChargePoint

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


async def on_connect(websocket, cp_id, db: Session):
    """
    For every new charge point that connects,
    create a ChargePoint instance and start listening for messages.
    :param db:
    :param websocket:
    :param cp_id:
    :return:
    """
    try:
        requested_protocols = websocket._websocket.headers['Sec-WebSocket-Protocol']
    except KeyError:
        requested_protocols = None
        logging.info("Client hasn't requested any Subprotocol. "
                     "Closing Connection")
    if requested_protocols:
        logging.info("Protocols Matched: %s", requested_protocols)
    else:
        # In the websockets lib if no subprotocols are supported by the
        # client and the server, it proceeds without a subprotocol,
        # so we have to manually close the connection.
        logging.warning('Protocols Mismatched | Expected Subprotocols: %s,'
                        ' but client supports  %s | Closing connection',
                        websocket.available_subprotocols,
                        requested_protocols
                        )
        return await websocket.close()

    cp = ChargePoint(cp_id, websocket)

    db.add(cp)
    db.commit()
    db.refresh(cp)

    await cp.start()
