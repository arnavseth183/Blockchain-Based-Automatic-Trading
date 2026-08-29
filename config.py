import os
import json
from dotenv import load_dotenv

load_dotenv()


class AppConfig:

    # ------------------------------------------
    # GENERAL SETTINGS
    # ------------------------------------------

    APP_NAME = "Decentralized AI Blockchain Trading"
    DEBUG_MODE = True

    # ------------------------------------------
    # MARKET SETTINGS
    # ------------------------------------------

    SUPPORTED_STOCKS = [
        "RELIANCE.NS",
        "TCS.NS",
        "INFY.NS",
        "HDFCBANK.NS",
        "ICICIBANK.NS"
    ]

    DATA_INTERVAL = "1m"
    DATA_PERIOD = "5d"

    # ------------------------------------------
    # AI SETTINGS
    # ------------------------------------------

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    MODEL_PATH = os.path.join(BASE_DIR, "models", "trained", "trading_model.pkl")
    SCALER_PATH = os.path.join(BASE_DIR, "models", "scalers", "feature_scaler.pkl")

    CONFIDENCE_THRESHOLD = 0.65
    RETRAIN_INTERVAL_DAYS = 30

    # ------------------------------------------
    # BLOCKCHAIN SETTINGS
    # ------------------------------------------

    WEB3_PROVIDER_URI = os.getenv("WEB3_PROVIDER_URI")
    PRIVATE_KEY = os.getenv("PRIVATE_KEY")
    ACCOUNT_ADDRESS = os.getenv("ACCOUNT_ADDRESS")

    CONTRACT_ADDRESSES_FILE = os.path.join(
        BASE_DIR,
        "blockchain_protocol",
        "deployment",
        "addresses.json"
    )

    GAS_LIMIT = 3000000
    GAS_PRICE = None  # gwei

    # ------------------------------------------
    # SECURITY
    # ------------------------------------------

    ENCRYPTION_SECRET = os.getenv("ENCRYPTION_SECRET", "dev_secret_key")

    # ------------------------------------------
    # LOGGING
    # ------------------------------------------

    LOG_DIR = os.path.join(BASE_DIR, "logs")

    AI_LOG_FILE = os.path.join(LOG_DIR, "ai.log")
    BLOCKCHAIN_LOG_FILE = os.path.join(LOG_DIR, "blockchain.log")
    TRANSACTION_LOG_FILE = os.path.join(LOG_DIR, "transactions.log")

    # ------------------------------------------
    # COMPLIANCE
    # ------------------------------------------

    SIMULATION_MODE = False

    # ✅ FIX: THIS IS CRITICAL FOR YOUR PROJECT
    INITIAL_CAPITAL = 10000

    INITIAL_ETH_BALANCE = 10000

    # ------------------------------------------
    # EXECUTION SETTINGS (NEW - DO NOT REMOVE)
    # ------------------------------------------

    DEFAULT_EXECUTION_MODE = "manual"   # manual / auto
    AUTO_TRADER_INTERVAL = 10  # seconds

    # ------------------------------------------
    # INIT
    # ------------------------------------------

    def __init__(self):
        self._ensure_directories()
        self._ensure_blockchain_files()
        self.validate()

    # ------------------------------------------
    # DIRECTORY SETUP
    # ------------------------------------------

    def _ensure_directories(self):
        os.makedirs(self.LOG_DIR, exist_ok=True)
        os.makedirs(os.path.dirname(self.MODEL_PATH), exist_ok=True)
        os.makedirs(os.path.dirname(self.SCALER_PATH), exist_ok=True)

    # ------------------------------------------
    # BLOCKCHAIN FILE SETUP
    # ------------------------------------------

    def _ensure_blockchain_files(self):

        os.makedirs(os.path.dirname(self.CONTRACT_ADDRESSES_FILE), exist_ok=True)

        if not os.path.exists(self.CONTRACT_ADDRESSES_FILE):
            with open(self.CONTRACT_ADDRESSES_FILE, "w") as f:
                json.dump({}, f)

    # ------------------------------------------
    # VALIDATION
    # ------------------------------------------

    def validate(self):

        if not self.SIMULATION_MODE:

            if not self.WEB3_PROVIDER_URI:
                raise ValueError("WEB3_PROVIDER_URI not set in .env")

            if not self.PRIVATE_KEY:
                raise ValueError("PRIVATE_KEY not set in .env")

            if not self.ACCOUNT_ADDRESS:
                raise ValueError("ACCOUNT_ADDRESS not set in .env")

        if not os.path.exists(self.MODEL_PATH):
            print("Warning: Model file not found at", self.MODEL_PATH)

        if not os.path.exists(self.SCALER_PATH):
            print("Warning: Scaler file not found at", self.SCALER_PATH)

        if self.DEFAULT_EXECUTION_MODE not in ["manual", "auto"]:
            raise ValueError("DEFAULT_EXECUTION_MODE must be 'manual' or 'auto'")