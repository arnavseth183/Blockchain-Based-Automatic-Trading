"""
execution_engine/simulation_rules/settlement_logic.py

Handles T+1 settlement simulation
"""

import datetime


class SettlementLogic:

    def __init__(self):
        self.settlement_records = {}

    def record_trade(self, trade_id):
        settlement_date = datetime.datetime.now() + datetime.timedelta(days=1)
        self.settlement_records[trade_id] = settlement_date

    def check_settlement(self, trade_id):
        if trade_id not in self.settlement_records:
            return "Not found"

        if datetime.datetime.now() >= self.settlement_records[trade_id]:
            return "Settled"

        return "Pending"