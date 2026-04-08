from pydantic import BaseModel
from typing import Optional

class SyncRequest(BaseModel):
    symbol: str
    timeframe: str
    bars: int = 150

class HealthResponse(BaseModel):
    mode: str
    mt5_enabled: bool
    db_ok: bool

class HighLowResponse(BaseModel):
    symbol: str
    timeframe: str
    times: list[str]
    high: list[float]
    low: list[float]

class DailyHighLowResponse(BaseModel):
    symbol: str
    timeframe: str
    daily_high: Optional[float] = None
    daily_low: Optional[float] = None
