from datetime import datetime, date, time
from sqlalchemy import select, func, desc
from sqlalchemy.orm import Session
from app.models import MarketBar, SyncLog

def upsert_bars(db: Session, symbol: str, timeframe: str, rows: list[dict]) -> int:
    saved = 0
    for row in rows:
        existing = db.execute(
            select(MarketBar).where(
                MarketBar.symbol == symbol,
                MarketBar.timeframe == timeframe,
                MarketBar.bar_time == row["bar_time"],
            )
        ).scalar_one_or_none()

        if existing:
            existing.open_price = row["open_price"]
            existing.high_price = row["high_price"]
            existing.low_price = row["low_price"]
            existing.close_price = row["close_price"]
            existing.tick_volume = row["tick_volume"]
            existing.spread = row["spread"]
            existing.real_volume = row["real_volume"]
        else:
            db.add(MarketBar(
                symbol=symbol,
                timeframe=timeframe,
                bar_time=row["bar_time"],
                open_price=row["open_price"],
                high_price=row["high_price"],
                low_price=row["low_price"],
                close_price=row["close_price"],
                tick_volume=row["tick_volume"],
                spread=row["spread"],
                real_volume=row["real_volume"],
            ))
        saved += 1

    db.commit()
    return saved

def add_sync_log(db: Session, symbol: str, timeframe: str, bars_requested: int, bars_saved: int, status: str, message: str | None = None):
    db.add(SyncLog(
        symbol=symbol,
        timeframe=timeframe,
        bars_requested=bars_requested,
        bars_saved=bars_saved,
        status=status,
        message=message,
    ))
    db.commit()

def get_symbols(db: Session) -> list[str]:
    stmt = select(MarketBar.symbol).distinct().order_by(MarketBar.symbol.asc())
    return [row[0] for row in db.execute(stmt).all()]

def get_timeframes(db: Session) -> list[str]:
    stmt = select(MarketBar.timeframe).distinct().order_by(MarketBar.timeframe.asc())
    return [row[0] for row in db.execute(stmt).all()]

def get_high_low(db: Session, symbol: str, timeframe: str, limit: int):
    stmt = (
        select(MarketBar)
        .where(MarketBar.symbol == symbol, MarketBar.timeframe == timeframe)
        .order_by(desc(MarketBar.bar_time))
        .limit(limit)
    )
    rows = list(db.execute(stmt).scalars().all())
    rows.reverse()
    return rows

def get_latest_bar(db: Session, symbol: str, timeframe: str):
    stmt = (
        select(MarketBar)
        .where(MarketBar.symbol == symbol, MarketBar.timeframe == timeframe)
        .order_by(desc(MarketBar.bar_time))
        .limit(1)
    )
    return db.execute(stmt).scalar_one_or_none()

def get_daily_high_low(db: Session, symbol: str, timeframe: str):
    start_of_day = datetime.combine(date.today(), time.min)
    end_of_day = datetime.combine(date.today(), time.max)

    stmt = select(
        func.max(MarketBar.high_price),
        func.min(MarketBar.low_price),
    ).where(
        MarketBar.symbol == symbol,
        MarketBar.timeframe == timeframe,
        MarketBar.bar_time >= start_of_day,
        MarketBar.bar_time <= end_of_day,
    )
    row = db.execute(stmt).one()
    return {
        "daily_high": row[0],
        "daily_low": row[1],
    }

def get_sync_logs(db: Session, limit: int = 20):
    stmt = select(SyncLog).order_by(desc(SyncLog.created_at)).limit(limit)
    return list(db.execute(stmt).scalars().all())
