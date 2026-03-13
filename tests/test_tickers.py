from datetime import datetime
from decimal import Decimal

import pytest
from fastapi import FastAPI
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Ticker
from app.schemas import Ticker as TickerSchema

pytestmark = pytest.mark.asyncio


async def test_get_all_prices(
    app: FastAPI,
    client: AsyncClient,
    db: AsyncSession,
):
    db.add_all(
        [
            Ticker(
                symbol="BTC_USDT",
                price=Decimal(i),
                timestamp=int(datetime.now().timestamp()),
            )
            for i in range(5)
        ]
    )
    await db.commit()

    res = await client.get(
        app.url_path_for("get_all_prices"), params={"ticker": "BTC_USDT"}
    )
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 5


async def test_get_last_price(
    app: FastAPI,
    client: AsyncClient,
    db: AsyncSession,
):
    db.add_all(
        [
            Ticker(
                symbol="BTC_USDT",
                price=Decimal(1 * i),
                timestamp=int(datetime.now().timestamp()),
            )
            for i in range(3)
        ]
    )
    await db.commit()

    res = await client.get(
        app.url_path_for("get_last_price"), params={"ticker": "BTC_USDT"}
    )
    assert res.status_code == 200
    ticker = TickerSchema.model_validate(res.json())
    assert ticker.id == 3


async def test_get_prices_by_date(
    app: FastAPI,
    client: AsyncClient,
    db: AsyncSession,
):
    ticker_1 = Ticker(
        symbol="BTC_USDT",
        price=10,
        timestamp=datetime(2026, 3, 1).timestamp(),
    )
    ticker_2 = Ticker(
        symbol="BTC_USDT",
        price=50,
        timestamp=datetime(2026, 3, 30).timestamp(),
    )

    db.add_all([ticker_1, ticker_2])
    await db.commit()

    res = await client.get(
        app.url_path_for("get_price_by_date"),
        params={
            "ticker": "BTC_USDT",
            "date_from": "2026-03-20",
            "date_to": "2026-03-30",
        },
    )
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["id"] == ticker_2.id
