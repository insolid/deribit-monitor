from fastapi import FastAPI

from app.api import tickers

app = FastAPI()

app.include_router(tickers.router)
