import json
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy import select
from .models import create_db, Incomes, Outgoings


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


def add_outgoing(
    name: str, expenses: dict, income_id: Optional[int] = None
) -> Outgoings:
    chosen_income = None
    if income_id:
        for income in get_incomes():
            if income.id == income_id:
                chosen_income = income
                break

    with Session(engine) as session:
        new_outgoing = Outgoings(
            name=name, expenses=json.dumps(expenses), ingoing=chosen_income
        )
        print(new_outgoing.name, new_outgoing.expenses, new_outgoing.ingoing)
        session.add(new_outgoing)
        session.commit()
    return new_outgoing


def get_outgoings() -> List[Outgoings]:
    search = select(Outgoings)
    outgoings = []
    with Session(engine) as session:
        for result in session.scalars(search):
            outgoings.append(result)
    return outgoings


def get_outgoing_income(outgoing: Outgoings) -> Incomes:
    income = None
    with Session(engine) as session:
        if outgoing.income_id:
            outgoing = session.get(Outgoings, outgoing.id)
            income = outgoing.ingoing
    return income


def update_outgoing(
    id: int, name: str, expenses: dict, income_id: Optional[int] = None
) -> Optional[dict]:
    chosen_income = None
    if income_id:
        for income in get_incomes():
            if income.id == income_id:
                chosen_income = income
                break
    search = select(Outgoings).where(Outgoings.id == id)
    with Session(engine) as session:
        outgoing_obj = session.scalars(search).one_or_none()
        if not outgoing_obj:
            return None
        if name:
            outgoing_obj.name = name
        if expenses:
            outgoing_obj.expenses = json.dumps(expenses)
        if chosen_income:
            outgoing_obj.ingoing = chosen_income
        session.commit()
    return expenses


def delete_outgoing(id: int) -> Optional[Outgoings]:
    with Session(engine) as session:
        outgoing = session.get(Outgoings, id)
        if outgoing:
            session.delete(outgoing)
        session.commit()
    return outgoing
