from sqlalchemy.orm import DeclarativeBase
from decimal import Decimal

from sqlalchemy import DECIMAL, BigInteger
from sqlalchemy.orm import Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class Ticker(Base):
    __tablename__ = "ticker"

    id: Mapped[int] = mapped_column(autoincrement=True, primary_key=True)
    symbol: Mapped[str] = mapped_column()
    price: Mapped[Decimal] = mapped_column(DECIMAL)
    timestamp: Mapped[int] = mapped_column(BigInteger)
