from pydantic import BaseModel
from dotenv import load_dotenv
import os

load_dotenv()

class Settings(BaseModel):
    app_mode: str = os.getenv("APP_MODE", "demo").strip().lower()
    db_url: str = os.getenv("DB_URL", "sqlite:///./trading_app.db")
    mt5_enabled: bool = os.getenv("MT5_ENABLED", "false").strip().lower() == "true"
    mt5_login: str | None = os.getenv("MT5_LOGIN") or None
    mt5_password: str | None = os.getenv("MT5_PASSWORD") or None
    mt5_server: str | None = os.getenv("MT5_SERVER") or None
    mt5_path: str | None = os.getenv("MT5_PATH") or None
    default_symbol: str = os.getenv("DEFAULT_SYMBOL", "EURUSD")
    default_timeframe: str = os.getenv("DEFAULT_TIMEFRAME", "M15")
    auto_refresh_seconds: int = int(os.getenv("AUTO_REFRESH_SECONDS", "20"))

settings = Settings()

SUPPORTED_TIMEFRAMES = {
    "M1": 1,
    "M5": 5,
    "M15": 15,
    "M30": 30,
    "H1": 60,
    "H4": 240,
    "D1": 1440,
}
