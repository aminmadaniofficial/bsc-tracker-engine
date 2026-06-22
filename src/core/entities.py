# src/core/entities.py
from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class BalanceSnapshot:
    wallet_address: str
    token_symbol: str
    amount: float
    timestamp: datetime