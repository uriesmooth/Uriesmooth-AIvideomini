import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import stripe

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("uriesmoothai-videomini-settlements")

app = FastAPI(title="UriesmoothAI-videomini Settlement Engine", version="2.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = os.getenv("STRIPE_API_KEY", "sk_test_mockkey")

class PaymentRequest(BaseModel):
    customer_id: str
    amount_cents: int
    currency: str = "usd"
    payment_method_id: str

@app.post("/api/v1/settle-payment")
async def create_payment_settlement(payload: PaymentRequest):
    try:
        logger.info(f"Processing payment settlement for customer: {payload.customer_id}")
        intent = stripe.PaymentIntent.create(
            amount=payload.amount_cents,
            currency=payload.currency,
            payment_method=payload.payment_method_id,
            confirm=True,
            automatic_payment_methods={"enabled": True, "allow_redirects": "never"}
        )
        
        return {
            "status": "success",
            "transaction_id": intent.id,
            "charged_amount": payload.amount_cents / 100.0,
            "currency": payload.currency
        }
    except Exception as e:
        logger.error(f"Payment settlement failed: {str(e)}")
        raise HTTPException(status_code=400, detail=str(e))
