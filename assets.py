"""
Trading assets watched by this strategy.
"""
from dataclasses import dataclass
import math


@dataclass
class AssetSpec:
    name: str
    mode: str                  # "price" or "pip"
    contract_size: float
    pip_size: float | None = None
    min_lot: float = 0.01
    lot_step: float = 0.01
    max_lot: float | None = None

ASSETS = {
    "GBPUSD": AssetSpec(
        name="GBPUSD",
        mode="pip",
        contract_size=100000,   # verify on your platform
        pip_size=0.0001,
    ),
    "EURUSD": AssetSpec(
        name="EURUSD",
        mode="pip",
        contract_size=100000,   # verify on your platform
        pip_size=0.0001,
    ),
    "NZDCAD": AssetSpec(
        name="NZDCAD",
        mode="pip",
        contract_size=100000,    # ENTER current USD pip value
        pip_size=0.0001,
    ),
    "BTCUSDT": AssetSpec(
        name="BTCUSDT",
        mode="price",
        contract_size=1,    # ENTER platform-specific value
        pip_size=None,
    ),
    "EURCAD": AssetSpec(
        name="EURCAD",
        mode="pip",
        contract_size=100000,    # ENTER current USD pip value
        pip_size=0.0001,
    ),
}
