from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import StreamingResponse
import asyncio
import json

app = FastAPI(title="Urielsmooth Financial Backend")

ledger_state = {
    "account_id": "USFEX-CORE-01",
    "balance": 142500.00,
    "currency": "USD",
    "status": "SECURE_LOCKED"
}

async def event_generator():
    while True:
        yield f"data: {json.dumps(ledger_state)}\n\n"
        await asyncio.sleep(2)

@app.get("/api/financial/stream")
async def stream_ledger(request: Request):
    return StreamingResponse(event_generator(), media_type="text/event-stream")

@app.post("/api/financial/execute-transfer")
async def execute_transfer(payload: dict):
    amount = payload.get("amount", 0.0)
    if amount <= 0 or amount > ledger_state["balance"]:
        raise HTTPException(status_code=400, detail="Invalid transfer amount or insufficient funds.")
    ledger_state["balance"] -= amount
    return {"status": "SUCCESS", "new_balance": ledger_state["balance"]}
