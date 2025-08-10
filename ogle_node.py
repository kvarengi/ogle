#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import uvicorn
from ogle_market import Market

app = FastAPI(title="OGLE NODE", version="0.1.0")
market = Market()

class RegisterReq(BaseModel):
    username: str

class MintReq(BaseModel):
    username: str
    amount: float

class OrderReq(BaseModel):
    username: str
    side: str
    price: float
    amount: float

@app.post("/register")
def register(req: RegisterReq):
    return market.register(req.username)

@app.get("/balances/{username}")
def balances(username: str):
    return market.balances(username)

@app.post("/mint_gcr")
def mint_gcr(req: MintReq):
    return market.mint_gcr(req.username, req.amount)

@app.post("/order")
def place_order(req: OrderReq):
    try:
        return market.place_order(req.username, req.side, req.price, req.amount)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.get("/orderbook")
def orderbook():
    return market.orderbook_snapshot()

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
