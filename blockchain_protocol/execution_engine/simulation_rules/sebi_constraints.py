"""
execution_engine/simulation_rules/sebi_constraints.py

Implements SEBI-like constraints for academic simulation
"""


class SEBIConstraints:

    MAX_POSITION_PER_STOCK = 10000
    MAX_TOTAL_EXPOSURE = 5000000

    def validate_position_limits(self, user_id, symbol, quantity):
        """
        Enforces:
        - Max position size
        - Max exposure limit
        """

        if quantity > self.MAX_POSITION_PER_STOCK:
            return {
                "approved": False,
                "reason": "Position exceeds SEBI limit"
            }

        # Simulated exposure logic
        exposure = quantity * 1000  # placeholder pricing

        if exposure > self.MAX_TOTAL_EXPOSURE:
            return {
                "approved": False,
                "reason": "Exposure exceeds regulatory cap"
            }

        return {"approved": True}