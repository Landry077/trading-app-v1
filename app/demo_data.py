from datetime import datetime, timedelta
from random import uniform, randint
from sqlalchemy.orm import Session
from app.models import MarketBar

DEMO_SYMBOLS = ["EURUSD", "GBPUSD", "XAUUSD", "USDJPY", "BTCUSD"]
DEMO_TIMEFRAMES = ["M5", "M15", "H1"]

BASE_PRICES = {
    "EURUSD": 1.0850,
    "GBPUSD": 1.2710,
    "XAUUSD": 3025.0,
    "USDJPY": 151.20,
    "BTCUSD": 81250.0,
}

MINUTES = {
    "M5": 5,
    "M15": 15,
    "H1": 60,
}

def seed_demo_data(db: Session):
    existing = db.query(MarketBar).first()
    if existing:
        return

    now = datetime.utcnow().replace(second=0, microsecond=0)

    for symbol in DEMO_SYMBOLS:
        for timeframe in DEMO_TIMEFRAMES:
            step = MINUTES[timeframe]
            base = BASE_PRICES[symbol]
            price = base

            for i in range(220, 0, -1):
                bar_time = now - timedelta(minutes=i * step)

                drift = uniform(-0.003, 0.003) if symbol != "XAUUSD" and symbol != "BTCUSD" else uniform(-8, 8)
                open_price = price
                high_price = open_price + abs(drift) + abs(uniform(0.0002, 0.002 if symbol != "XAUUSD" and symbol != "BTCUSD" else 3))
                low_price = open_price - abs(uniform(0.0002, 0.002 if symbol != "XAUUSD" and symbol != "BTCUSD" else 3))
                close_price = open_price + drift

                if symbol in ("XAUUSD", "BTCUSD"):
                    high_price = round(high_price, 2)
                    low_price = round(low_price, 2)
                    open_price = round(open_price, 2)
                    close_price = round(close_price, 2)
                elif symbol == "USDJPY":
                    high_price = round(high_price, 3)
                    low_price = round(low_price, 3)
                    open_price = round(open_price, 3)
                    close_price = round(close_price, 3)
                else:
                    high_price = round(high_price, 5)
                    low_price = round(low_price, 5)
                    open_price = round(open_price, 5)
                    close_price = round(close_price, 5)

                if low_price > high_price:
                    low_price, high_price = high_price, low_price

                db.add(MarketBar(
                    symbol=symbol,
                    timeframe=timeframe,
                    bar_time=bar_time,
                    open_price=open_price,
                    high_price=high_price,
                    low_price=low_price,
                    close_price=close_price,
                    tick_volume=randint(100, 3000),
                    spread=randint(1, 40),
                    real_volume=randint(100, 3000),
                ))
                price = close_price

    db.commit()
