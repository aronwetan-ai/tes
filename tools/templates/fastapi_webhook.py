#!/usr/bin/env python3
"""
FastAPI Webhook Receiver Template — Runnable

Usage:
    pip install fastapi uvicorn
    uvicorn tools.templates.fastapi_webhook:app --host 0.0.0.0 --port 8000

For production:
    pm2 start "uvicorn tools.templates.fastapi_webhook:app --host 0.0.0.0 --port 8000" \
        --name webhook-receiver

Test:
    curl -X POST http://localhost:8000/trigger \
      -H "Content-Type: application/json" \
      -d '{"type": "input.received", "payload": {"hello": "world"}}'

Source: Adapted from SUPERAGENT v2 m4.md
"""

import os
import logging
from datetime import datetime
from typing import Optional

from fastapi import FastAPI, Request, HTTPException, Header
from fastapi.responses import JSONResponse

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
)
logger = logging.getLogger(__name__)

app = FastAPI(title="Webhook Receiver", version="1.0")

# Optional: shared-secret signature verification
WEBHOOK_SECRET = os.getenv("WEBHOOK_SECRET")


# === Event handlers ===

async def on_exchange_complete(data: dict):
    """Handle 'exchange.complete' events (e.g., payment confirmed)."""
    logger.info(f"Exchange complete: {data.get('payload')}")
    # ADD YOUR LOGIC HERE


async def on_input_received(data: dict):
    """Handle 'input.received' events (generic input trigger)."""
    logger.info(f"Input received: {data.get('payload')}")
    # ADD YOUR LOGIC HERE


async def on_unknown(data: dict):
    """Fallback for unmapped event types."""
    logger.warning(f"Unknown event type: {data.get('type')}")


# Event router
EVENT_HANDLERS = {
    "exchange.complete": on_exchange_complete,
    "input.received": on_input_received,
}


# === Endpoints ===

@app.get("/")
async def root():
    return {"status": "ok", "service": "webhook-receiver", "ts": datetime.utcnow().isoformat()}


@app.get("/health")
async def health():
    return {"healthy": True, "ts": datetime.utcnow().isoformat()}


@app.post("/trigger")
async def trigger(
    request: Request,
    x_webhook_secret: Optional[str] = Header(None),
):
    """Main webhook receiver. Routes by event 'type' field."""

    # Optional secret verification
    if WEBHOOK_SECRET and x_webhook_secret != WEBHOOK_SECRET:
        logger.warning("Webhook called with invalid secret")
        raise HTTPException(status_code=401, detail="Invalid signature")

    try:
        data = await request.json()
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON: {e}")

    event_type = data.get("type")
    if not event_type:
        raise HTTPException(status_code=400, detail="Missing 'type' field")

    handler = EVENT_HANDLERS.get(event_type, on_unknown)
    try:
        await handler(data)
    except Exception as e:
        logger.exception(f"Handler error for {event_type}")
        raise HTTPException(status_code=500, detail=f"Handler error: {e}")

    return JSONResponse({"ack": True, "type": event_type, "ts": datetime.utcnow().isoformat()})


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
