"""
execution_engine/protocol_controller.py
"""

from typing import Optional, Dict, Any, List
from datetime import datetime
from blockchain_protocol.storage.user_wallet_registry import UserWalletRegistry


class ProtocolController:

    def __init__(self, config, web3: Optional[object] = None, executor: Optional[object] = None):

        self.config = config
        self.web3 = web3

        # attach executor safely
        self.executor = executor

        self.simulation_mode = getattr(config, "SIMULATION_MODE", True)

        print(
            "✅ Protocol running in SIMULATION mode"
            if self.simulation_mode
            else "🚀 Protocol running in LIVE blockchain mode"
        )

        self.INITIAL_CAPITAL = float(
            getattr(config, "INITIAL_CAPITAL", 10000)
        )

        self.portfolio_state = {
            "cash": self.INITIAL_CAPITAL,
            "positions": {}
        }

        self.transaction_history: List[Dict[str, Any]] = []
        self.registry = UserWalletRegistry()

    # ==================================================
    # SAFE NORMALIZER
    # ==================================================
    def _normalize(self, data):
        if data is None:
            return {"quantity": 0.0, "price": 0.0}

        if isinstance(data, (int, float)):
            return {"quantity": float(data), "price": 0.0}

        if isinstance(data, dict):
            return {
                "quantity": float(data.get("quantity", 0) or 0),
                "price": float(data.get("price", 0) or 0)
            }

        return {"quantity": 0.0, "price": 0.0}

    # ==================================================
    # TRADE EXECUTION ENGINE
    # ==================================================
    def execute_trade(self, signal_data: Dict[str, Any]) -> Dict[str, Any]:

        stock = signal_data.get("stock")
        signal = signal_data.get("signal")

        price = signal_data.get("price")
        if price is None or price == 0:
            return {
                "status": "FAILED",
                "error": "Price missing",
                "details": signal_data
            }

        price = float(price)
        quantity = int(signal_data.get("quantity", 1))
        user = signal_data.get("user")

        # ==================================================
        # SIMULATION MODE
        # ==================================================
        if self.simulation_mode:

            print("📊 Simulated trade executed:", signal_data)

            return self._execute_simulation(stock, signal, price, quantity, user)

        # ==================================================
        # LIVE MODE (SAFE GUARD)
        # ==================================================
        if self.executor is None:
            # 🔥 IMPORTANT: fallback instead of crash
            print("⚠️ Executor missing → switching to SIMULATION mode")

            return self._execute_simulation(stock, signal, price, quantity, user)

        try:
            tx = self.executor.execute(signal_data)
            self.transaction_history.append(tx)
            return tx

        except Exception as e:
            return {
                "status": "FAILED",
                "error": str(e),
                "details": signal_data
            }

    # ==================================================
    # SIMULATION ENGINE (CLEAN SEPARATION)
    # ==================================================
    def _execute_simulation(self, stock, signal, price, quantity, user):

        if signal == "BUY":

            cost = price * quantity

            if self.portfolio_state["cash"] < cost:
                return {
                    "status": "FAILED",
                    "error": "Insufficient cash balance"
                }

            self.portfolio_state["cash"] -= cost

            existing = self._normalize(
                self.portfolio_state["positions"].get(stock)
            )

            old_qty = existing["quantity"]
            old_price = existing["price"]

            new_qty = old_qty + quantity

            avg_price = (
                (old_qty * old_price) + (quantity * price)
            ) / new_qty if new_qty > 0 else 0.0

            self.portfolio_state["positions"][stock] = {
                "quantity": new_qty,
                "price": avg_price
            }

            if user:
                self.registry.update_balance(user, -cost)
                self.registry.update_portfolio(user, stock, quantity)

        elif signal == "SELL":

            existing = self._normalize(
                self.portfolio_state["positions"].get(stock)
            )

            held_qty = existing["quantity"]

            if held_qty <= 0:
                return {
                    "status": "FAILED",
                    "error": "No holdings to sell"
                }

            sell_qty = min(quantity, held_qty)

            self.portfolio_state["cash"] += price * sell_qty

            new_qty = held_qty - sell_qty

            if new_qty == 0:
                self.portfolio_state["positions"].pop(stock, None)
            else:
                self.portfolio_state["positions"][stock] = {
                    "quantity": new_qty,
                    "price": existing["price"]
                }

            if user:
                self.registry.update_balance(user, price * sell_qty)
                self.registry.update_portfolio(user, stock, -sell_qty)

        else:
            return {
                "status": "FAILED",
                "error": "Only BUY/SELL allowed"
            }

        tx = {
            "tx_hash": f"0xSIM_{len(self.transaction_history)+1}",
            "symbol": stock,
            "action": signal,
            "quantity": quantity,
            "price": price,
            "status": "SIMULATED",
            "timestamp": datetime.now().isoformat()
        }

        self.transaction_history.append(tx)
        return tx

    # ==================================================
    # PORTFOLIO STATE
    # ==================================================
    def get_portfolio_state(self):

        clean_positions = {}

        for symbol, data in self.portfolio_state["positions"].items():
            clean_positions[symbol] = self._normalize(data)

        return {
            "cash": float(self.portfolio_state["cash"]),
            "positions": clean_positions
        }

    # ==================================================
    # HISTORY
    # ==================================================
    def get_transaction_history(self):
        return self.transaction_history

    def get_dashboard_state(self):
        return {
            "portfolio": self.get_portfolio_state(),
            "transactions": self.get_transaction_history()
        }

    def get_protocol_parameters(self):
        return {
            "max_position_size": 100,
            "leverage": 2,
            "risk_limit": 0.7
        }

    def propose_change(self, param, value):
        return f"0xproposal_{param}_{value}"