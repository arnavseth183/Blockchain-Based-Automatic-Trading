import json
import os


class ContractLoader:

    def __init__(self, web3):

        self.w3 = web3

        # ------------------------------------------------
        # Get PROJECT ROOT
        # (two levels above web3_layer)
        # ------------------------------------------------

        project_root = os.path.abspath(
            os.path.join(os.path.dirname(__file__), "..", "..")
        )

        # ------------------------------------------------
        # Hardhat artifacts location
        # ------------------------------------------------

        self.artifacts_path = os.path.join(
            project_root,
            "artifacts",
            "contracts"
        )

        # ------------------------------------------------
        # addresses.json file
        # ------------------------------------------------

        self.address_file = os.path.join(
            project_root,
            "blockchain_protocol",
            "deployment",
            "addresses.json"
        )

    # ------------------------------------------------
    # Load artifact
    # ------------------------------------------------

    def load_artifact(self, contract_name):

        artifact_path = os.path.join(
            self.artifacts_path,
            f"{contract_name}.sol",
            f"{contract_name}.json"
        )

        print("Loading artifact:", artifact_path)

        if not os.path.exists(artifact_path):
            raise FileNotFoundError(
                f"Artifact not found: {artifact_path}"
            )

        with open(artifact_path) as f:
            artifact = json.load(f)

        bytecode = artifact["bytecode"]

        if isinstance(bytecode, dict):
            bytecode = bytecode["object"]

        return {
            "abi": artifact["abi"],
            "bytecode": bytecode
        }

    # ------------------------------------------------
    # Deploy contract
    # ------------------------------------------------

    def deploy_contract(self, contract_name, deployer, private_key):

        artifact = self.load_artifact(contract_name)

        contract = self.w3.eth.contract(
            abi=artifact["abi"],
            bytecode=artifact["bytecode"]
        )

        nonce = self.w3.eth.get_transaction_count(deployer)

        txn = contract.constructor().build_transaction({
            "from": deployer,
            "nonce": nonce,
            "gas": 5000000,
            "gasPrice": self.w3.to_wei("20", "gwei")
        })

        signed_txn = self.w3.eth.account.sign_transaction(
            txn,
            private_key
        )

        tx_hash = self.w3.eth.send_raw_transaction(
            signed_txn.raw_transaction
        )

        receipt = self.w3.eth.wait_for_transaction_receipt(tx_hash)

        return receipt.contractAddress

    # ------------------------------------------------
    # Save deployed address
    # ------------------------------------------------

    def save_address(self, contract_name, address):

        addresses = {}

        if os.path.exists(self.address_file):
            with open(self.address_file) as f:
                addresses = json.load(f)

        addresses[contract_name] = address

        with open(self.address_file, "w") as f:
            json.dump(addresses, f, indent=4)

    # ------------------------------------------------
    # Deploy + save
    # ------------------------------------------------

    def deploy_and_store(self, contract_name, deployer, private_key):

        address = self.deploy_contract(
            contract_name,
            deployer,
            private_key
        )

        self.save_address(contract_name, address)

        print(f"{contract_name} deployed at {address}")

        return address

    # ------------------------------------------------
    # Load addresses
    # ------------------------------------------------

    def load_addresses(self):

        if not os.path.exists(self.address_file):
            raise FileNotFoundError("Deploy contracts first")

        with open(self.address_file) as f:
            return json.load(f)

    # ------------------------------------------------
    # Load deployed contract
    # ------------------------------------------------

    def get_contract(self, contract_name):

        addresses = self.load_addresses()

        if contract_name not in addresses:
            raise Exception(f"{contract_name} not deployed")

        address = addresses[contract_name]

        artifact = self.load_artifact(contract_name)

        return self.w3.eth.contract(
            address=self.w3.to_checksum_address(address),
            abi=artifact["abi"]
        )