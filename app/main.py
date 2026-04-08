from pathlib import Path
from fastapi import FastAPI, Depends, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.config import settings
from app.db import Base, engine, get_db
from app.schemas import SyncRequest, HealthResponse
from app.demo_data import seed_demo_data
from app.mt5_service import initialize_mt5, shutdown_mt5, fetch_rates, get_terminal_info
from app.repository import (
    upsert_bars,
    add_sync_log,
    get_symbols,
    get_timeframes,
    get_high_low,
    get_latest_bar,
    get_daily_high_low,
    get_sync_logs,
)

BASE_DIR = Path(__file__).resolve().parent.parent
UI_PATH = BASE_DIR / "frontend" / "index.html"

app = FastAPI(title="Trading App V3")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)

@app.on_event("startup")
def startup():
    if settings.app_mode == "demo":
        from app.db import SessionLocal
        db = SessionLocal()
        try:
            seed_demo_data(db)
        finally:
            db.close()

@app.get("/", response_model=HealthResponse)
def root(db: Session = Depends(get_db)):
    db_ok = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False

    return HealthResponse(
        mode=settings.app_mode,
        mt5_enabled=settings.mt5_enabled,
        db_ok=db_ok,
    )

@app.get("/ui")
def ui():
    return FileResponse(UI_PATH)

@app.get("/api/health")
def health(db: Session = Depends(get_db)):
    db_ok = True
    try:
        db.execute(text("SELECT 1"))
    except Exception:
        db_ok = False

    terminal = None
    if settings.mt5_enabled and settings.app_mode == "live":
        try:
            initialize_mt5()
            terminal = get_terminal_info()
        except Exception as exc:
            terminal = {"error": str(exc)}
        finally:
            shutdown_mt5()

    return {
        "mode": settings.app_mode,
        "mt5_enabled": settings.mt5_enabled,
        "db_ok": db_ok,
        "terminal": terminal,
        "default_symbol": settings.default_symbol,
        "default_timeframe": settings.default_timeframe,
        "auto_refresh_seconds": settings.auto_refresh_seconds,
    }

@app.get("/api/symbols")
def symbols(db: Session = Depends(get_db)):
    values = get_symbols(db)
    return {"symbols": values}

@app.get("/api/timeframes")
def timeframes(db: Session = Depends(get_db)):
    values = get_timeframes(db)
    return {"timeframes": values}

@app.get("/api/high-low")
def high_low(
    symbol: str = Query(...),
    timeframe: str = Query(...),
    limit: int = Query(4, ge=1, le=30),
    db: Session = Depends(get_db),
):
    rows = get_high_low(db, symbol, timeframe, limit)
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "times": [row.bar_time.isoformat(sep=" ") for row in rows],
        "high": [row.high_price for row in rows],
        "low": [row.low_price for row in rows],
    }

@app.get("/api/latest-bar")
def latest_bar(
    symbol: str = Query(...),
    timeframe: str = Query(...),
    db: Session = Depends(get_db),
):
    row = get_latest_bar(db, symbol, timeframe)
    if not row:
        return {"message": "Aucune donnée"}

    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "bar_time": row.bar_time.isoformat(sep=" "),
        "open": row.open_price,
        "high": row.high_price,
        "low": row.low_price,
        "close": row.close_price,
    }

@app.get("/api/daily-high-low")
def daily_high_low(
    symbol: str = Query(...),
    timeframe: str = Query(...),
    db: Session = Depends(get_db),
):
    row = get_daily_high_low(db, symbol, timeframe)
    return {
        "symbol": symbol,
        "timeframe": timeframe,
        "daily_high": row["daily_high"],
        "daily_low": row["daily_low"],
    }

@app.get("/api/sync-logs")
def sync_logs(db: Session = Depends(get_db)):
    rows = get_sync_logs(db)
    return {
        "logs": [
            {
                "symbol": row.symbol,
                "timeframe": row.timeframe,
                "bars_requested": row.bars_requested,
                "bars_saved": row.bars_saved,
                "status": row.status,
                "message": row.message,
                "created_at": row.created_at.isoformat(sep=" "),
            }
            for row in rows
        ]
    }

@app.post("/api/sync")
def sync(payload: SyncRequest, db: Session = Depends(get_db)):
    if settings.app_mode != "live" or not settings.mt5_enabled:
        add_sync_log(
            db,
            payload.symbol,
            payload.timeframe,
            payload.bars,
            0,
            "INFO",
            "Mode demo actif. La synchronisation MT5 réelle n'est pas exécutée.",
        )
        return {
            "message": "Mode demo actif. Aucune synchronisation MT5 réelle n'a été exécutée.",
            "symbol": payload.symbol,
            "timeframe": payload.timeframe,
            "bars_saved": 0,
        }

    try:
        initialize_mt5()
        rows = fetch_rates(payload.symbol, payload.timeframe, payload.bars)
        saved = upsert_bars(db, payload.symbol, payload.timeframe, rows)
        add_sync_log(db, payload.symbol, payload.timeframe, payload.bars, saved, "SUCCESS", "Synchronisation MT5 OK")
        return {
            "message": "Synchronisation terminée",
            "symbol": payload.symbol,
            "timeframe": payload.timeframe,
            "bars_saved": saved,
        }
    except Exception as exc:
        add_sync_log(db, payload.symbol, payload.timeframe, payload.bars, 0, "ERROR", str(exc))
        raise HTTPException(status_code=500, detail=str(exc))
    finally:
        shutdown_mt5()
