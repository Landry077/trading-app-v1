from datetime import datetime, timezone
from typing import Any
from app.config import settings

try:
    import MetaTrader5 as mt5
except Exception:
    mt5 = None

TIMEFRAME_LOOKUP: dict[str, Any] = {}
if mt5 is not None:
    TIMEFRAME_LOOKUP = {
        "M1": mt5.TIMEFRAME_M1,
        "M5": mt5.TIMEFRAME_M5,
        "M15": mt5.TIMEFRAME_M15,
        "M30": mt5.TIMEFRAME_M30,
        "H1": mt5.TIMEFRAME_H1,
        "H4": mt5.TIMEFRAME_H4,
        "D1": mt5.TIMEFRAME_D1,
    }

def initialize_mt5():
    if mt5 is None:
        raise RuntimeError("Le module MetaTrader5 n'est pas disponible dans cet environnement.")

    kwargs = {
        "timeout": 60000
    }

    if settings.mt5_path:
        kwargs["path"] = settings.mt5_path

    if settings.mt5_login and settings.mt5_password and settings.mt5_server:
        kwargs["login"] = int(settings.mt5_login)
        kwargs["password"] = settings.mt5_password
        kwargs["server"] = settings.mt5_server

    ok = mt5.initialize(**kwargs)
    if not ok:
        raise RuntimeError(f"Échec initialize MT5: {mt5.last_error()}")

def shutdown_mt5():
    if mt5 is not None:
        mt5.shutdown()

def get_terminal_info():
    if mt5 is None:
        return None

    version = mt5.version()
    if version is None:
        return None

    account = mt5.account_info()

    result = {
        "version": version[0],
        "build": version[1],
        "release_date": version[2],
    }

    if account is not None:
        result["login"] = account.login
        result["server"] = account.server
        result["company"] = account.company

    return result

def normalize_symbol(symbol: str) -> str:
    if symbol.endswith("m"):
        return symbol
    return symbol + "m"

def fetch_rates(symbol: str, timeframe: str, count: int = 150):
    if mt5 is None:
        raise RuntimeError("Le module MetaTrader5 n'est pas disponible.")

    symbol = normalize_symbol(symbol)

    tf = TIMEFRAME_LOOKUP.get(timeframe)
    if tf is None:
        raise ValueError(f"Timeframe non supporté: {timeframe}")

    selected = mt5.symbol_select(symbol, True)
    if not selected:
        raise RuntimeError(f"Impossible d'activer le symbole {symbol} dans MT5.")

    rates = mt5.copy_rates_from_pos(symbol, tf, 0, count)
    if rates is None or len(rates) == 0:
        raise RuntimeError(f"Aucune donnée MT5 pour {symbol} {timeframe}. Détail: {mt5.last_error()}")

    result = []
    for row in rates:
        result.append({
            "bar_time": datetime.fromtimestamp(row["time"], tz=timezone.utc).replace(tzinfo=None),
            "open_price": float(row["open"]),
            "high_price": float(row["high"]),
            "low_price": float(row["low"]),
            "close_price": float(row["close"]),
            "tick_volume": int(row["tick_volume"]),
            "spread": int(row["spread"]),
            "real_volume": int(row["real_volume"]),
        })

    return result