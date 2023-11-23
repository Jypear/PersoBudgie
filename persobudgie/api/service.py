from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, List

from .controller.handler import add_income, get_incomes, update_income, delete_income

api = FastAPI()


class ReturnIncomeStream(BaseModel):
    id: int
    name: str
    income: float


class AddIncomeStream(BaseModel):
    name: str
    income: float


class UpdateIncomeStream(BaseModel):
    id: int
    name: Optional[str]
    income: Optional[float]


class DeleteIncomeStream(BaseModel):
    id: int


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
