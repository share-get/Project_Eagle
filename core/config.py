"""
Project Eagle
Configuration

Author: Project Eagle
"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict


# ---------------------------------------------------------------------
# Project
# ---------------------------------------------------------------------

PROJECT_NAME = "Project Eagle"
VERSION = "0.1.0"


# ---------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------

ROOT_DIR = Path(__file__).resolve().parent.parent

CACHE_DIR = ROOT_DIR / "cache"
DATA_DIR = ROOT_DIR / "data"
RESULT_DIR = ROOT_DIR / "results"
LOG_DIR = ROOT_DIR / "logs"

for path in (
    CACHE_DIR,
    DATA_DIR,
    RESULT_DIR,
    LOG_DIR,
):
    path.mkdir(parents=True, exist_ok=True)


# ---------------------------------------------------------------------
# Market Assets
# ---------------------------------------------------------------------

ETF = {
    "VOO": "VOO",
    "QQQM": "QQQM",
    "SPY": "SPY",
    "QQQ": "QQQ",
}

MACRO = {
    "VIX": "^VIX",
    "TNX": "^TNX",
    "FVX": "^FVX",
    "IRX": "^IRX",
    "USD": "DX-Y.NYB",
}

FX = {
    "NZDUSD": "NZDUSD=X",
    "USDCNY": "USDCNY=X",
}


# ---------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------

START_DATE = "2000-01-01"

AUTO_CACHE = True

AUTO_ADJUST = False


# ---------------------------------------------------------------------
# Indicator Parameters
# ---------------------------------------------------------------------

MA_WINDOWS = [5, 10, 20, 50, 100, 200]

EMA_WINDOWS = [12, 26, 50]

RSI_PERIOD = 14

ATR_PERIOD = 14

MACD_FAST = 12
MACD_SLOW = 26
MACD_SIGNAL = 9

VOL_WINDOW = 20

ROLLING_HIGH = 252


# ---------------------------------------------------------------------
# Backtest
# ---------------------------------------------------------------------

INITIAL_CAPITAL = 100000.0

COMMISSION = 0.0005

SLIPPAGE = 0.0002


# ---------------------------------------------------------------------
# Runtime Config
# ---------------------------------------------------------------------

@dataclass(slots=True)
class RuntimeConfig:

    benchmark: str = "VOO"

    start_date: str = START_DATE

    auto_cache: bool = AUTO_CACHE

    initial_capital: float = INITIAL_CAPITAL

    indicators: Dict = field(
        default_factory=lambda: {
            "ma": MA_WINDOWS,
            "ema": EMA_WINDOWS,
            "rsi": RSI_PERIOD,
            "atr": ATR_PERIOD,
        }
    )
