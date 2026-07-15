"""
Project Eagle v0.1

Configuration Module

负责：
- 项目路径管理
- 市场资产配置
- 数据下载配置
- 指标参数配置
- 回测参数配置
- 运行环境配置

所有核心模块通过 RuntimeConfig 获取配置。

"""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List


# ============================================================
# Project Information
# ============================================================

PROJECT_NAME = "Project Eagle"

PROJECT_VERSION = "0.1.0"


# ============================================================
# Directory Configuration
# ============================================================

ROOT_DIR = Path(__file__).resolve().parent.parent


CACHE_DIR = ROOT_DIR / "cache"

DATA_DIR = ROOT_DIR / "data"

RESULT_DIR = ROOT_DIR / "results"

LOG_DIR = ROOT_DIR / "logs"


DEFAULT_DIRECTORIES = [
    CACHE_DIR,
    DATA_DIR,
    RESULT_DIR,
    LOG_DIR,
]


def initialize_directories() -> None:
    """
    创建项目运行所需目录。

    在系统启动时调用。
    """

    for directory in DEFAULT_DIRECTORIES:
        directory.mkdir(
            parents=True,
            exist_ok=True
        )


# ============================================================
# Data Configuration
# ============================================================

START_DATE = "2000-01-01"


END_DATE = None


AUTO_CACHE = True


CACHE_FORMAT = "csv"


AUTO_ADJUST_PRICE = False


# ============================================================
# Market Assets
# ============================================================

ETF_UNIVERSE: Dict[str, str] = {

    "VOO": "VOO",

    "QQQM": "QQQM",

    # Benchmark
    "SPY": "SPY",

    "QQQ": "QQQ",
}


MACRO_UNIVERSE: Dict[str, str] = {

    # Volatility Index
    "VIX": "^VIX",

    # US Treasury Yield
    "US10Y": "^TNX",

    "US5Y": "^FVX",

    "US3M": "^IRX",

    # Dollar Index
    "DXY": "DX-Y.NYB",
}


FX_UNIVERSE: Dict[str, str] = {

    "NZDUSD": "NZDUSD=X",

    "USDCNY": "USDCNY=X",
}


# ============================================================
# Indicator Configuration
# ============================================================

@dataclass(frozen=True)
class IndicatorConfig:
    """
    技术指标参数配置。
    """

    ma_windows: List[int] = field(
        default_factory=lambda: [
            5,
            10,
            20,
            50,
            100,
            200,
        ]
    )


    ema_windows: List[int] = field(
        default_factory=lambda: [
            12,
            26,
            50,
        ]
    )


    rsi_period: int = 14


    atr_period: int = 14


    macd_fast: int = 12


    macd_slow: int = 26


    macd_signal: int = 9


    volatility_window: int = 20


    rolling_high_window: int = 252



# ============================================================
# Backtest Configuration
# ============================================================

@dataclass(frozen=True)
class BacktestConfig:
    """
    回测环境参数。
    """

    initial_capital: float = 100000.0


    commission: float = 0.0005


    slippage: float = 0.0002


    benchmark: str = "VOO"



# ============================================================
# Runtime Configuration
# ============================================================

@dataclass
class RuntimeConfig:
    """
    Project Eagle运行时总配置。

    所有核心模块推荐接收该对象。
    """

    start_date: str = START_DATE


    end_date: str | None = END_DATE


    cache_enabled: bool = AUTO_CACHE


    cache_dir: Path = CACHE_DIR


    data_dir: Path = DATA_DIR


    result_dir: Path = RESULT_DIR


    log_dir: Path = LOG_DIR


    indicators: IndicatorConfig = field(
        default_factory=IndicatorConfig
    )


    backtest: BacktestConfig = field(
        default_factory=BacktestConfig
    )


# ============================================================
# Helper Functions
# ============================================================

def get_default_config() -> RuntimeConfig:
    """
    返回默认运行配置。

    Returns
    -------
    RuntimeConfig
        默认项目配置
    """

    initialize_directories()

    return RuntimeConfig()
