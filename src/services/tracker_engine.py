# src/services/tracker_engine.py
import time
import logging
from src.core.interfaces import BlockchainRepository, NotificationService
from src.config import AppConfig

class TrackingOrchestrator:
    def __init__(self, config: AppConfig, repo: BlockchainRepository, notifier: NotificationService):
        self.config = config
        self.repo = repo
        self.notifier = notifier
        self.last_snapshot = None

    def run(self) -> None:
        logging.info(f"Engine fired up for target: {self.config.target_wallet_address}")
        
        while True:
            try:
                current_snapshot = self.repo.get_balance(
                    self.config.target_wallet_address, 
                    self.config.usdt_contract_address
                )
                
                if self.last_snapshot and self.last_snapshot.amount != current_snapshot.amount:
                    self.notifier.send_alert(self.last_snapshot, current_snapshot)
                else:
                    print(f"\r[{current_snapshot.timestamp.strftime('%H:%M:%S')}] Balance: ${current_snapshot.amount:,.2f} USDT | Standing by...", end="")
                
                self.last_snapshot = current_snapshot
            except Exception as e:
                logging.error(f"Execution handling error: {e}")
                
            time.sleep(self.config.check_interval_seconds)