# run.py
import sys
import logging
from src.config import AppConfig
from src.infrastructure.blockchain import Web3BscRepository
from src.infrastructure.alerts import CompositeAlertService
from src.services.tracker_engine import TrackingOrchestrator

# Config root logging level
logging.basicConfig(level=logging.INFO, format="[%(asctime)s] [%(levelname)s] %(message)s")

def bootstrap() -> None:
    try:
        # Load Settings Layer
        config = AppConfig()
        
        # Inject Dependencies into Implementations
        blockchain_repo = Web3BscRepository(rpc_url=config.bsc_rpc_url)
        alert_service = CompositeAlertService()
        
        # Start Engine
        orchestrator = TrackingOrchestrator(config=config, repo=blockchain_repo, notifier=alert_service)
        orchestrator.run()
        
    except KeyboardInterrupt:
        logging.info("\nGracefully shutting down engine pipelines. Safe status reached.")
        sys.exit(0)
    except Exception as e:
        logging.critical(f"Fatal crash on bootstrap routing: {e}")
        sys.exit(1)

if __name__ == "__main__":
    bootstrap()