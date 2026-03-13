from datetime import date, datetime, time, timedelta
from typing import Annotated

from fastapi import Query
from fastapi.routing import APIRouter
from sqlalchemy import select

from app.core.db import SessionDep
from app.models import Ticker
from app.schemas import Ticker as TickerSchema

router = APIRouter(prefix="/tickers", tags=["tickers"])


@router.get("/", response_model=list[TickerSchema])
async def get_all_prices(db: SessionDep, ticker: str):
    return await db.scalars(select(Ticker).where(Ticker.symbol == ticker))


@router.get("/last-price", response_model=TickerSchema | None)
async def get_last_price(db: SessionDep, ticker: str):
    return await db.scalar(
        select(Ticker)
        .where(Ticker.symbol == ticker)
        .order_by(Ticker.timestamp.desc())
        .limit(1)
    )


@router.get("/by-date", response_model=list[TickerSchema])
async def get_all_prices_by_date(
    db: SessionDep,
    ticker: str,
    date_from: Annotated[date, Query(example="2025-01-01")],
    date_to: Annotated[date, Query(example="2025-01-02")],
):
    date_from_ts = int(datetime.combine(date_from, time.min).timestamp())
    date_to_ts = int(
        datetime.combine(date_to + timedelta(days=1), time.min).timestamp()
    )

    stmt = select(Ticker).where(
        Ticker.symbol == ticker,
        Ticker.timestamp >= date_from_ts,
        Ticker.timestamp < date_to_ts,
    )

    return await db.scalars(stmt)
