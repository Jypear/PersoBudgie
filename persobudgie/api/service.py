import json
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List, Dict

from .controller.handler import add_income, get_incomes, update_income, delete_income
from .controller.handler import (
    add_outgoing,
    get_outgoings,
    get_outgoing_income,
    update_outgoing,
    delete_outgoing,
)

api = FastAPI()


class ReturnIncomeStream(BaseModel):
    id: int
    name: str
    income: float


class ReturnOutgoings(BaseModel):
    id: int
    name: str
    expenses: Optional[dict]
    income_id: Optional[int]


class AddIncomeStream(BaseModel):
    name: str
    income: float


class AddOutgoing(BaseModel):
    name: str
    expenses: Optional[Dict[str, float]]
    income_id: Optional[int]


class UpdateIncomeStream(BaseModel):
    id: int
    name: Optional[str]
    income: Optional[float]


class UpdateOutgoing(BaseModel):
    id: int
    name: Optional[str]
    expenses: Optional[dict]
    income_id: Optional[int]


class DeleteIncomeStream(BaseModel):
    id: int


class DeleteOutgoing(BaseModel):
    id: int


class RemainingOutgoing(BaseModel):
    ingoing: float
    outgoing: float
    remaining: float


@api.post("/income")
async def add_income_stream(stream: AddIncomeStream) -> List[ReturnIncomeStream]:
    add_income(stream.name, stream.income)
    incomes = await get_income_streams()
    return incomes


@api.get("/income")
async def get_income_streams() -> List[ReturnIncomeStream]:
    incomes = get_incomes()
    returned_data = []
    for income in incomes:
        returned_data.append(
            {"id": income.id, "name": income.name, "income": income.income}
        )
    return returned_data


@api.put("/income")
async def update_income_stream(stream: UpdateIncomeStream) -> List[ReturnIncomeStream]:
    update_income(stream.id, stream.name, stream.income)
    incomes = await get_income_streams()
    return incomes


@api.delete("/income")
async def delete_income_stream(stream: DeleteIncomeStream) -> List[ReturnIncomeStream]:
    delete_income(stream.id)
    incomes = await get_income_streams()
    return incomes


@api.post("/outgoing")
async def add_outgoing_stream(outgoing: AddOutgoing) -> List[ReturnOutgoings]:
    add_outgoing(outgoing.name, outgoing.expenses, outgoing.income_id)
    outgoings = await get_outgoings_stream()
    return outgoings


@api.get("/outgoing")
async def get_outgoings_stream() -> List[ReturnOutgoings]:
    outgoings = get_outgoings()
    returned_data = []
    for outgoing in outgoings:
        expenses = {}
        if outgoing.expenses:
            expenses = json.loads(outgoing.expenses)
        returned_data.append(
            {
                "id": outgoing.id,
                "name": outgoing.name,
                "expenses": expenses,
                "income_id": outgoing.income_id,
            }
        )
    return returned_data


@api.put("/outgoing")
async def update_outgoings_stream(outgoing: UpdateOutgoing) -> List[ReturnOutgoings]:
    update_outgoing(outgoing.id, outgoing.name, outgoing.expenses, outgoing.income_id)
    outgoings = await get_outgoings_stream()
    return outgoings


@api.delete("/outgoing")
async def delete_outgoing_stream(
    outgoing: DeleteOutgoing,
) -> List[ReturnOutgoings]:
    delete_outgoing(outgoing.id)
    outgoings = await get_outgoings_stream()
    return outgoings


@api.get("/outgoing/remaining")
def calculate_remianing(id: int) -> RemainingOutgoing:
    total_income = 0
    total_outgoing = 0
    outgoings = get_outgoings()
    for outgoing in outgoings:
        if outgoing.id == id:
            if outgoing.income_id:
                income = get_outgoing_income(outgoing)
                total_income += income.income
            expenses = json.loads(outgoing.expenses)
            for expense in expenses.values():
                total_outgoing += expense
            break

    return {
        "ingoing": total_income,
        "outgoing": total_outgoing,
        "remaining": total_income - total_outgoing,
    }
