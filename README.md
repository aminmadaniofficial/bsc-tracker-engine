# BSC Tracker Engine (Real-Time ERC-20 Block Scanner)

A production-grade, highly decoupled blockchain monitoring solution built with Python and Web3.py. This engine implements **Onion/Clean Architecture** and strict data validation using **Pydantic V2** to track live ledger balance changes of specific ERC-20 tokens (default: USDT) on the Binance Smart Chain (BSC) network via direct JSON-RPC polling.

---

## 🛑 The Origin Story

This project was born out of a real-world security incident. On **June 21, 2026**, my main cryptocurrency wallet was compromised due to a leaked local KeyStore configuration backup. While the attacker gained control of the private keys, I needed a highly persistent, low-latency, and autonomous telemetry system to monitor the wallet's balance changes and catch outgoing transactions instantly without relying on centralized, delayed API block explorers (like BscScan APIs). 

Instead of deploying a quick, dirty script, I chose to engineer this enterprise-grade software to turn a critical security lesson into an open-source tool for decentralized finance (DeFi) forensics, monitoring, and wallet recovery asset tracking.

---

## 🏗️ Architecture Layout

The software strictly respects **S.O.L.I.D** principles, implementing complete **Separation of Concerns (SoC)** and **Dependency Injection**. The business logic is entirely decoupled from external frameworks, protocols, and notification infrastructures.

```text
bsctracker/
│
├── .env                        # Local env vars (Git ignored)
├── .gitignore                  # Git exclusion rules
├── requirements.txt            # Package dependencies
├── run.py                      # App bootstrap entrypoint
│
└── src/
    ├── __init__.py
    ├── config.py               # Pydantic schema validation
    │
    ├── core/                   # Enterprise Domain Layer
    │   ├── __init__.py
    │   ├── entities.py         # Data models & snapshots
    │   └── interfaces.py       # Abstract contracts
    │
    ├── infrastructure/         # External implementations
    │   ├── __init__.py
    │   ├── blockchain.py       # Web3 RPC Repository
    │   └── alerts.py           # Notification services
    │
    └── services/               # Orchestration Layer
        ├── __init__.py
        └── tracker_engine.py   # Core monitoring runtime loop

```

---

## ⚡ Key Technical Features

* **Strict Schema Validation:** Utilizes `pydantic-settings` to auto-parse, cast, and validate cryptographic addresses (`0x...` hex layouts) and safeguard polling intervals against invalid configurations before execution runtime.
* **Onion Architecture Mapping:** Pure Domain definitions (`src/core`) know absolutely nothing about `web3` or low-level JSON-RPC clients, allowing seamless protocol migrations (e.g., migrating to Ethereum or Solana infrastructure by swapping repositories).
* **Robust Persistence & Logging:** Implements thread-safe concurrent stream and persistent file logging (`tracker.log`) containing precise stack traces, operational lifecycles, and warning telemetries.
* **Zero Third-Party API Key Dependencies:** Interacts directly with public/private Web3 HTTP Provider RPC node gateways utilizing lightweight ERC-20 contract function ABI abstractions (`balanceOf` / `decimals`).

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository

```bash
git clone [https://github.com/yourusername/bsctracker.git](https://github.com/yourusername/bsctracker.git)
cd bsctracker

```

### 2. Configure Environment Context

Create an isolated Python virtual environment and pull structural dependencies:

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Setup Environment Configuration
The project utilizes a `.env` file to securely manage blockchain nodes and target wallets without exposing secrets to version control. Clone the provided repository template to create your local configurations:

```bash
cp .env.example .env
```

Now, open the newly created `.env` file and insert your dedicated tracking parameters:

```env
BSC_RPC_URL=https://bsc-dataseed.binance.org/
USDT_CONTRACT_ADDRESS=0x55d398326f99059ff775485246999027b3197955
TARGET_WALLET_ADDRESS=0xYourTargetWalletAddressHere
CHECK_INTERVAL_SECONDS=5

```

### 4. Fire Up the Engine

Execute the modular bootstrap component via python main path parsing:

```bash
python -m run

```

---

## 🛠️ Extensibility Pattern

To bind additional notification targets (e.g., Telegram Bots, Discord Webhooks, Twilio SMS), implement the core domain contract abstract definition found in `src/core/interfaces.py`:

```python
from src.core.interfaces import NotificationService
from src.core.entities import BalanceSnapshot

class TelegramNotificationService(NotificationService):
    def send_alert(self, previous: BalanceSnapshot, current: BalanceSnapshot) -> None:
        # Implement telegram bot dispatch logic here safely
        pass

```

Then inject your new implementation in the container wiring phase inside `run.py`.

---

## 📄 License

Distributed under the MIT License. See `LICENSE` for more information.

