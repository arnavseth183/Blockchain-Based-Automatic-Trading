# blockchain_protocol/execution_engine/execution_state.py

from datetime import datetime


class ExecutionState:
    """
    SINGLE SOURCE OF TRUTH
    - Stores all trades (blockchain explorer)
    - Stores portfolio (cash + positions)
    - Updates state after every trade
    """

    def __init__(self):
        # -----------------------------
        # TRADE LEDGER (BLOCKCHAIN)
        # -----------------------------
        self.trades = []

        # -----------------------------
        # PORTFOLIO STATE
        # -----------------------------
        self.portfolio = {
            "cash": 10000.0,   # initial simulated balance
            "positions": {}    # { "RELIANCE": 10 }
        }

    # =========================================================
    # TRADE STORAGE (BLOCKCHAIN EXPLORER FEED)
    # =========================================================
    def add_trade(self, trade: dict):
        trade_record = {
            "tx_hash": trade.get("tx_hash"),
            "symbol": trade.get("symbol"),
            "action": trade.get("action"),
            "quantity": int(trade.get("quantity", 0)),
            "price": float(trade.get("price", 0)),
            "status": trade.get("status", "SUCCESS"),
            "timestamp": datetime.utcnow().isoformat()
        }

        self.trades.append(trade_record)

    def get_trades(self):
        return self.trades

    # =========================================================
    # PORTFOLIO UPDATE LOGIC
    # =========================================================
    def update_portfolio(self, symbol: str, action: str, qty: int, price: float):

        if symbol not in self.portfolio["positions"]:
            self.portfolio["positions"][symbol] = 0

        if action == "BUY":
            self.portfolio["positions"][symbol] += qty
            self.portfolio["cash"] -= qty * price

        elif action == "SELL":
            self.portfolio["positions"][symbol] -= qty
            self.portfolio["cash"] += qty * price

    def get_portfolio(self):
        return self.portfolio

    # =========================================================
    # RESET (OPTIONAL DEBUG)
    # =========================================================
    def reset(self):
        self.trades = []
        self.portfolio = {
            "cash": 10000.0,
            "positions": {}
        }