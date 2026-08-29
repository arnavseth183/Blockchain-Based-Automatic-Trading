from web3 import Web3
from blockchain_protocol.web3_layer.contract_loader import ContractLoader

RPC = "http://127.0.0.1:8545"

PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
ACCOUNT = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"

w3 = Web3(Web3.HTTPProvider(RPC))

if not w3.is_connected():
    raise Exception("Web3 connection failed")

print("Connected to blockchain")

loader = ContractLoader(w3)

contracts = [
    "TradingProtocol",
    "PortfolioManager",
    "RiskManager",
    "GasSimulator",
    "Governance"
]

for c in contracts:

    print("Deploying", c)

    loader.deploy_and_store(
        c,
        ACCOUNT,
        PRIVATE_KEY
    )

print("All contracts deployed")