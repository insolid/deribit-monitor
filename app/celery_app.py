import requests
from celery import Celery
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.core.config import settings
from app.models import Ticker

app = Celery("celery_app", broker=settings.redis_url)

sync_engine = create_engine(settings.postgres_url.replace("asyncpg", "psycopg2"))
sync_session = sessionmaker(sync_engine, expire_on_commit=False, autoflush=False)

BASE_URL = "https://www.deribit.com/api/v2/public/ticker?instrument_name="


@app.task
def save_deribit_tickers(base_url: str, *tickers: str):
    ticker_objs = []

    for t in tickers:
        try:
            res = requests.get(base_url + t)
            if res.status_code != 200:
                continue
            result = res.json()["result"]
            price, timestamp = result["index_price"], result["timestamp"] / 1000
            ticker_objs.append(Ticker(symbol=t, price=price, timestamp=timestamp))
        except Exception as e:
            print(e)

    with sync_session() as db:
        db.add_all(ticker_objs)
        db.commit()


app.conf.beat_schedule = {
    "save-deribit-tickers-every-1-minute": {
        "task": "app.celery_app.save_deribit_tickers",
        "schedule": 60,
        "args": (BASE_URL, "BTC_USDT", "ETH_USDT"),
    },
}
