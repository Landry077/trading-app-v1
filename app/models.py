from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime
from app.db import Base

class MarketBar(Base):
    __tablename__ = "market_bars"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), index=True, nullable=False)
    timeframe = Column(String(10), index=True, nullable=False)
    bar_time = Column(DateTime, index=True, nullable=False)
    open_price = Column(Float, nullable=False)
    high_price = Column(Float, nullable=False)
    low_price = Column(Float, nullable=False)
    close_price = Column(Float, nullable=False)
    tick_volume = Column(Integer, nullable=True)
    spread = Column(Integer, nullable=True)
    real_volume = Column(Integer, nullable=True)

class SyncLog(Base):
    __tablename__ = "sync_logs"

    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String(20), nullable=False)
    timeframe = Column(String(10), nullable=False)
    bars_requested = Column(Integer, nullable=False)
    bars_saved = Column(Integer, nullable=False)
    status = Column(String(20), nullable=False)
    message = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
