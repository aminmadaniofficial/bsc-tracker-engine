# src/config.py
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from web3 import Web3

class AppConfig(BaseSettings):
    """
    Robust Environment Configuration Model.
    Automatically parses, type-casts, and validates schema integrity from runtime environment or .env file.
    """
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    bsc_rpc_url: str = Field(..., alias="BSC_RPC_URL")
    usdt_contract_address: str = Field(..., alias="USDT_CONTRACT_ADDRESS")
    target_wallet_address: str = Field(..., alias="TARGET_WALLET_ADDRESS")
    check_interval_seconds: int = Field(5, alias="CHECK_INTERVAL_SECONDS")

    @field_validator("usdt_contract_address", "target_wallet_address")
    @classmethod
    def validate_evm_addresses(cls, value: str) -> str:
        """Ensures incoming addresses strictly match basic EVM layout requirements."""
        if not value.startswith("0x") or len(value) != 42:
            raise ValueError(f"Invalid cryptographic address format identified: '{value}'")
        return Web3.to_checksum_address(value)

    @field_validator("check_interval_seconds")
    @classmethod
    def validate_polling_interval(cls, value: int) -> int:
        """Prevents setting dangerous zero or negative evaluation rates."""
        if value < 1:
            raise ValueError("Telemetry pooling interval must evaluate to a positive integer (min 1s).")
        return value