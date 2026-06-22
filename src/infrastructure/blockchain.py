# src/infrastructure/blockchain.py
from datetime import datetime
from web3 import Web3
from src.core.interfaces import BlockchainRepository
from src.core.entities import BalanceSnapshot

class Web3BscRepository(BlockchainRepository):
    def __init__(self, rpc_url: str):
        self.web3 = Web3(Web3.HTTPProvider(rpc_url))
        if not self.web3.is_connected():
            raise ConnectionError("RPC Node unavailable.")
        
        self.erc20_abi = [
            {"constant": True, "inputs": [{"name": "_owner", "type": "address"}], "name": "balanceOf", "outputs": [{"name": "balance", "type": "uint256"}], "type": "function"},
            {"constant": True, "inputs": [], "name": "decimals", "outputs": [{"name": "", "type": "uint8"}], "type": "function"}
        ]

    def get_balance(self, wallet_address: str, token_address: str) -> BalanceSnapshot:
        contract = self.web3.eth.contract(address=Web3.to_checksum_address(token_address), abi=self.erc20_abi)
        decimals = contract.functions.decimals().call()
        raw_balance = contract.functions.balanceOf(Web3.to_checksum_address(wallet_address)).call()
        
        return BalanceSnapshot(
            wallet_address=wallet_address,
            token_symbol="USDT",
            amount=raw_balance / (10 ** decimals),
            timestamp=datetime.now()
        )