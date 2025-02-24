#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
#=============================================================================
# FileName: fastapi_websocket_and_backgroup_task_test.py
# Author: alfons
# LastChange:  2020/6/29 下午4:55
#=============================================================================
"""
import uvicorn
from typing import Dict, List
from typing import Optional
from collections import defaultdict
from fastapi import Cookie, Depends, FastAPI, Query, WebSocket, status
from pydantic import BaseModel
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
        var ws = null;
            function connect(event) {
                var itemId = document.getElementById("itemId")
                var token = document.getElementById("token")
                ws = new WebSocket("ws://10.10.80.17:8000/items/" + itemId.value + "/ws?token=" + token.value);
                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages')
                    var message = document.createElement('li')
                    var content = document.createTextNode(event.data)
                    message.appendChild(content)
                    messages.appendChild(message)
                };
                event.preventDefault()
            }
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


class Item(BaseModel):
    name: str
    description: Optional[str]
    price: float
    tax: Optional[float]


@app.get("/nb/{t}", response_model=Item)
async def get(t: int) -> Item:
    return Item("fasfas", "hhhh", 12)


@app.get("/time")
def get():
    import time
    time.sleep(30)
    return f"{time.time()}"


async def get_cookie_or_token(websocket: WebSocket,
                              token: str,
                              session: str = None):
    if session is None and token is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
    return websocket


websocket_dict: Dict[str, List[WebSocket]] = defaultdict(list)


async def send_to_all(item_id: str, message: str):
    for websocket in websocket_dict[item_id]:
        await websocket.send_text(message)


@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
        item_id: str,
        webs: WebSocket = Depends(get_cookie_or_token),
):
    global websocket_dict

    await webs.accept()
    await webs.send_text("Begin")
    websocket_dict[item_id].append(webs)

    while True:
        data = await webs.receive_text()
        await send_to_all(item_id, f"Session cookie or query token value is: {item_id}")
        await send_to_all(item_id, f"Message text was: {data}, for item ID: {item_id}")


def main():
    uvicorn.run(app, host="0.0.0.0", port=8000)


if __name__ == '__main__':
    main()
