const hre = require("hardhat");

async function main() {
  const TradingProtocol = await hre.ethers.getContractFactory("TradingProtocol");
  const tradingProtocol = await TradingProtocol.deploy();
  await tradingProtocol.waitForDeployment();

  console.log("TradingProtocol deployed to:", await tradingProtocol.getAddress());

  const RiskManager = await hre.ethers.getContractFactory("RiskManager");
  const riskManager = await RiskManager.deploy();
  await riskManager.waitForDeployment();

  console.log("RiskManager deployed to:", await riskManager.getAddress());
}

main().catch((error) => {
  console.error(error);
  process.exitCode = 1;
});