import json
import os
import time
from dataclasses import dataclass, asdict
from typing import Dict, List, Optional, Tuple

STORE_DIR = os.path.join(os.path.dirname(__file__), "data")
BALANCES_FILE = os.path.join(STORE_DIR, "balances.json")
ORDERS_FILE = os.path.join(STORE_DIR, "orders.json")
USERS_FILE = os.path.join(STORE_DIR, "users.json")

SUPPORTED_TOKENS = ["GCR", "OGLEC"]  # Gravity Credits and OGLE Coins


def ensure_store():
    os.makedirs(STORE_DIR, exist_ok=True)
    for path, default in [
        (BALANCES_FILE, {}),
        (ORDERS_FILE, {"bids": [], "asks": []}),
        (USERS_FILE, {"users": []}),
    ]:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                json.dump(default, f)


class JsonStore:
    def __init__(self, path: str):
        self.path = path
        ensure_store()

    def read(self):
        with open(self.path, "r", encoding="utf-8") as f:
            return json.load(f)

    def write(self, data):
        tmp = self.path + ".tmp"
        with open(tmp, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        os.replace(tmp, self.path)


class BalanceLedger:
    def __init__(self):
        self.store = JsonStore(BALANCES_FILE)

    def _get_balances(self) -> Dict[str, Dict[str, float]]:
        return self.store.read()

    def _set_balances(self, data: Dict[str, Dict[str, float]]):
        self.store.write(data)

    def ensure_user(self, username: str):
        data = self._get_balances()
        if username not in data:
            data[username] = {t: 0.0 for t in SUPPORTED_TOKENS}
            self._set_balances(data)

    def get_balances(self, username: str) -> Dict[str, float]:
        data = self._get_balances()
        return data.get(username, {t: 0.0 for t in SUPPORTED_TOKENS})

    def credit(self, username: str, token: str, amount: float):
        if token not in SUPPORTED_TOKENS:
            raise ValueError("Unsupported token")
        data = self._get_balances()
        self.ensure_user(username)
        data = self._get_balances()
        data[username][token] += float(amount)
        self._set_balances(data)

    def debit(self, username: str, token: str, amount: float):
        data = self._get_balances()
        self.ensure_user(username)
        data = self._get_balances()
        if data[username][token] < amount:
            raise ValueError("Insufficient balance")
        data[username][token] -= float(amount)
        self._set_balances(data)


@dataclass
class Order:
    id: str
    username: str
    side: str  # "buy" or "sell" (buy GCR for OGLEC; sell GCR for OGLEC)
    price: float  # price in OGLEC per 1 GCR
    amount: float  # amount of GCR
    ts: float


class OrderBook:
    def __init__(self):
        self.store = JsonStore(ORDERS_FILE)

    def _read(self):
        return self.store.read()

    def _write(self, data):
        self.store.write(data)

    def list_books(self) -> Dict[str, List[Dict]]:
        return self._read()

    def place(self, order: Order):
        data = self._read()
        book_key = "bids" if order.side == "buy" else "asks"
        data[book_key].append(asdict(order))
        # sort bids desc by price, asks asc by price
        data["bids"] = sorted(data["bids"], key=lambda x: (-x["price"], x["ts"]))
        data["asks"] = sorted(data["asks"], key=lambda x: (x["price"], x["ts"]))
        self._write(data)

    def match(self) -> List[Dict]:
        """Simple price-time priority matching. Returns list of trades."""
        data = self._read()
        bids = data["bids"]
        asks = data["asks"]
        trades: List[Dict] = []
        i = 0
        while bids and asks and bids[0]["price"] >= asks[0]["price"]:
            bid = bids[0]
            ask = asks[0]
            trade_price = (bid["price"] + ask["price"]) / 2.0
            trade_amount = min(bid["amount"], ask["amount"])
            trades.append({
                "price": trade_price,
                "amount": trade_amount,
                "buy_user": bid["username"],
                "sell_user": ask["username"],
                "ts": time.time(),
            })
            bid["amount"] -= trade_amount
            ask["amount"] -= trade_amount
            if bid["amount"] <= 1e-9:
                bids.pop(0)
            if ask["amount"] <= 1e-9:
                asks.pop(0)
            # re-sort not needed as top elements only reduced
        data["bids"] = bids
        data["asks"] = asks
        self._write(data)
        return trades


class Users:
    def __init__(self):
        self.store = JsonStore(USERS_FILE)

    def register(self, username: str) -> bool:
        data = self.store.read()
        if username in data.get("users", []):
            return False
        data.setdefault("users", []).append(username)
        self.store.write(data)
        return True

    def exists(self, username: str) -> bool:
        data = self.store.read()
        return username in data.get("users", [])


class Market:
    def __init__(self):
        ensure_store()
        self.ledger = BalanceLedger()
        self.orderbook = OrderBook()
        self.users = Users()

    def register(self, username: str) -> Dict:
        created = self.users.register(username)
        self.ledger.ensure_user(username)
        return {"created": created, "username": username}

    def mint_gcr(self, username: str, amount: float) -> Dict:
        self.ledger.credit(username, "GCR", amount)
        return {"ok": True, "username": username, "delta": amount, "balance": self.ledger.get_balances(username)}

    def place_order(self, username: str, side: str, price: float, amount: float) -> Dict:
        if side not in ("buy", "sell"):
            raise ValueError("side must be 'buy' or 'sell'")
        # Reserve funds
        if side == "buy":
            cost = price * amount
            self.ledger.debit(username, "OGLEC", cost)
        else:
            self.ledger.debit(username, "GCR", amount)
        order = Order(
            id=f"ord_{int(time.time()*1000)}",
            username=username,
            side=side,
            price=float(price),
            amount=float(amount),
            ts=time.time(),
        )
        self.orderbook.place(order)
        trades = self.orderbook.match()
        # Settle trades
        for t in trades:
            amt = t["amount"]
            price = t["price"]
            # Buyer pays OGLEC, receives GCR
            self.ledger.credit(t["buy_user"], "GCR", amt)
            # Seller receives OGLEC
            self.ledger.credit(t["sell_user"], "OGLEC", amt * price)
        return {"ok": True, "order": asdict(order), "trades": trades}

    def balances(self, username: str) -> Dict[str, float]:
        return self.ledger.get_balances(username)

    def orderbook_snapshot(self) -> Dict:
        return self.orderbook.list_books()
