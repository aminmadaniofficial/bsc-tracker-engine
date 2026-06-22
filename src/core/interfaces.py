# src/core/interfaces.py
from abc import ABC, abstractmethod
from src.core.entities import BalanceSnapshot

class BlockchainRepository(ABC):
    @abstractmethod
    def get_balance(self, wallet_address: str, token_address: str) -> BalanceSnapshot:
        """Fetch normalized balance from the ledger."""
        pass

class NotificationService(ABC):
    @abstractmethod
    def send_alert(self, previous: BalanceSnapshot, current: BalanceSnapshot) -> None:
        """Dispatch balance change alerts to active channels."""
        pass