from fastapi import FastAPI, WebSocket, WebSocketDisconnect, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from typing import Dict, List
import asyncio
import json
from myfirstproject import db

app = FastAPI()

# Mount a directory called `static/` at the URL path `/static` so the browser
# can request `app.js` and `style.css` directly. FastAPI serves files from
# the filesystem through this mount.
app.mount("/static", StaticFiles(directory="static"), name="static")

# Simple in-memory key->value store. This is intentionally minimal so you can
# concentrate on the request flow and real-time updates. In production you'd
# replace this with a database.
items: Dict[str, str] = {}

# Keep track of connected websocket clients so we can push updates to them.
connections: List[WebSocket] = []


def broadcast(message: str) -> None:
    """Send a text message to all connected websocket clients.

    We schedule send operations with `asyncio.create_task` because `broadcast`
    is called from synchronous FastAPI endpoints (POST/PUT/DELETE). Scheduling
    tasks lets the event loop handle sends without blocking the HTTP response.
    """
    for ws in connections:
        asyncio.create_task(ws.send_text(message))


@app.get("/", response_class=HTMLResponse)
async def index():
    # Serve the static HTML page. In a small app this is a simple file read.
    # In larger apps you'd use templating (Jinja) and pass context variables.
    with open("templates/index.html", "r", encoding="utf-8") as f:
        return HTMLResponse(f.read())


@app.get("/items")
async def list_items():
    # Return items from the database as key->value JSON.
    rows = db.list_items()
    return {r.key: r.value for r in rows}


@app.post("/items")
async def create_item(request: Request):
    # Accept either form/query params or a JSON body for flexibility. This
    # lets the browser send application/json from the frontend and
    # still support form-encoded clients.
    if request.headers.get("content-type", "").startswith("application/json"):
        payload = await request.json()
        key = payload.get("key")
        value = payload.get("value")
    else:
        form = await request.form()
        key = form.get("key")
        value = form.get("value")

    item = db.upsert_item(key, value)
    msg = json.dumps({"action": "created", "key": item.key, "value": item.value})
    broadcast(msg)
    return {"ok": True}


@app.put("/items/{key}")
async def update_item(key: str, request: Request):
    existing = db.get_item_by_key(key)
    if not existing:
        return {"error": "not found"}

    if request.headers.get("content-type", "").startswith("application/json"):
        payload = await request.json()
        value = payload.get("value")
    else:
        form = await request.form()
        value = form.get("value")

    item = db.upsert_item(key, value)
    msg = json.dumps({"action": "updated", "key": item.key, "value": item.value})
    broadcast(msg)
    return {"ok": True}


@app.delete("/items/{key}")
async def delete_item(key: str):
    db.delete_item_by_key(key)
    msg = json.dumps({"action": "deleted", "key": key})
    broadcast(msg)
    return {"ok": True}


@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    # Each client must `accept()` the websocket connection. We then add the
    # connection to our `connections` list so future broadcasts reach it.
    await websocket.accept()
    connections.append(websocket)
    try:
        while True:
            # Keep the connection open and echo back any incoming messages.
            # In this simple app the client doesn't need to send data, but
            # echoing makes it easy to debug the socket.
            data = await websocket.receive_text()
            await websocket.send_text(f"echo: {data}")
    except WebSocketDisconnect:
        # Clean up the connection list when the client disconnects.
        connections.remove(websocket)


if __name__ == "__main__":
    import uvicorn

    # Initialize the database file and tables on startup in dev mode.
    db.init_db()
    uvicorn.run("myfirstproject.app:app", host="127.0.0.1", port=8000, reload=True)
