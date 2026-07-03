"""Strategy registry. The /backtest skill adds new strategies here."""
from .base import Strategy, run_vectorized
from .ma_crossover import MACrossover
from .cost_aware_momentum import CostAwareMomentum
from .lag1_reversal import Lag1Reversal
from .tsmom import TSMom
from .donchian_breakout import DonchianBreakout

REGISTRY = {cls.name: cls for cls in (MACrossover, CostAwareMomentum, Lag1Reversal, TSMom, DonchianBreakout)}


def get(name: str) -> type[Strategy]:
    if name not in REGISTRY:
        raise KeyError(f"unknown strategy '{name}'; have {sorted(REGISTRY)}")
    return REGISTRY[name]
