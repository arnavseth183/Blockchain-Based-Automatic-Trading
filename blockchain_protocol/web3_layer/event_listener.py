"""
web3_layer/event_listener.py

Listens to smart contract events in real-time
"""

import time


class EventListener:

    def __init__(self, contract):
        self.contract = contract

    def listen_to_event(self, event_name):
        event = getattr(self.contract.events, event_name)
        event_filter = event.create_filter(fromBlock="latest")

        print(f"Listening to {event_name}...")

        while True:
            for entry in event_filter.get_new_entries():
                print("Event received:", entry)

            time.sleep(2)