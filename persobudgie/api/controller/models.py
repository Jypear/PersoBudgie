from typing import Optional
from sqlalchemy import String, Numeric, Engine, ForeignKey
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import create_engine


class Base(DeclarativeBase):
    ...


class Incomes(Base):
    __tablename__ = "income_streams"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    income: Mapped[float] = mapped_column(Numeric(scale=2))
    outgoing: Mapped[Optional["Outgoings"]] = relationship(back_populates="ingoing")


class Outgoings(Base):
    __tablename__ = "outgoings"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String())
    income_id: Mapped[int] = mapped_column(ForeignKey("income_streams.id"))
    ingoing: Mapped[Optional["Incomes"]] = relationship(back_populates="outgoing")
    expenses: Mapped[Optional[str]] = mapped_column(String())


def create_db() -> Engine:
    engine = create_engine("sqlite:///data.db")
    Base.metadata.create_all(engine)
    return engine
