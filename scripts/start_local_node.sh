#!/bin/bash

# ============================================================
# start_local_node.sh
# Starts local Ethereum blockchain node for protocol testing
# ============================================================

echo "=============================================="
echo "Starting Local Blockchain Node"
echo "=============================================="

NETWORK_NAME="tradechain_local"
DATA_DIR="./blockchain_protocol/local_node_data"
PORT=8545
CHAIN_ID=1337

# Create data directory if not exists
if [ ! -d "$DATA_DIR" ]; then
  echo "Creating local blockchain data directory..."
  mkdir -p $DATA_DIR
fi

# Check if Ganache is installed
if ! command -v ganache-cli &> /dev/null
then
    echo "Ganache CLI not found. Installing globally..."
    npm install -g ganache-cli
fi

echo "Launching Ganache Local Blockchain..."

ganache-cli \
  --port $PORT \
  --networkId $CHAIN_ID \
  --chainId $CHAIN_ID \
  --accounts 10 \
  --defaultBalanceEther 1000 \
  --gasLimit 12000000 \
  --mnemonic "tradechain blockchain deterministic mnemonic phrase" \
  --db $DATA_DIR

echo "Local blockchain running at http://127.0.0.1:$PORT"

echo "=============================================="
echo "Node Started Successfully"
echo "=============================================="