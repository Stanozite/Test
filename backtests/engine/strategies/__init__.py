"""Strategy registry. The /backtest skill adds new strategies here."""
from .base import Strategy, run_vectorized
from .ma_crossover import MACrossover

REGISTRY = {cls.name: cls for cls in (MACrossover,)}


def get(name: str) -> type[Strategy]:
    if name not in REGISTRY:
        raise KeyError(f"unknown strategy '{name}'; have {sorted(REGISTRY)}")
    return REGISTRY[name]
