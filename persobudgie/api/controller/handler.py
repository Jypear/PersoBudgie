from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import select
from .models import create_db, Incomes


engine = create_db()


def add_income(name: str, income: float) -> Incomes:
    with Session(engine) as session:
        new_income = Incomes(name=name, income=income)
        session.add(new_income)
        session.commit()
    return new_income


def get_incomes() -> List[Incomes]:
    search = select(Incomes)
    incomes = []
    with Session(engine) as session:
        for result in session.scalars(search):
            incomes.append(result)
    return incomes


def update_income(id: int, name: str, income: float) -> Optional[Incomes]:
    search = select(Incomes).where(Incomes.id == id)
    with Session(engine) as session:
        income_obj = session.scalars(search).one_or_none()
        if not income_obj:
            return None
        if name:
            income_obj.name = name
        if income:
            income_obj.income = income
        session.commit()
    return income


def delete_income(id: int) -> Optional[Incomes]:
    with Session(engine) as session:
        income = session.get(Incomes, id)
        if income:
            session.delete(income)
        session.commit()
    return income
