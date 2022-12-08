from starlette.websockets import WebSocket, WebSocketDisconnect


class WebSocketInterface:
    def __init__(self, websocket: WebSocket):
        self._websocket = websocket

    async def recv(self):
        try:
            receive_msg = await self._websocket.receive_text()
        except WebSocketDisconnect:
            # close skata
            return 'disconnected'
        else:
            return receive_msg

    async def send(self, text_message):
        await self._websocket.send_text(text_message)

    @property
    def websocket(self):
        return self._websocket