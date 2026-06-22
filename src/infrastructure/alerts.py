# src/infrastructure/alerts.py
import logging
import sys
from src.core.interfaces import NotificationService
from src.core.entities import BalanceSnapshot

class CompositeAlertService(NotificationService):
    def __init__(self):
        self.logger = logging.getLogger("TrackerEngine")

    def send_alert(self, previous: BalanceSnapshot, current: BalanceSnapshot) -> None:
        delta = current.amount - previous.amount
        msg = (
            f"\n🚨 [BALANCE ALERT]\n"
            f"Wallet: {current.wallet_address}\n"
            f"Previous: ${previous.amount:,.2f} | Current: ${current.amount:,.2f}\n"
            f"Net Delta: {delta:+,.2f} USDT\n"
            f"========================================="
        )
        self.logger.warning(msg)
        sys.stdout.write('\a')
        sys.stdout.flush()