from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from handlers import forecast
# TODO: include another routers?


router = Router()


router.include_routers(forecast.router)


class Forecast(StatesGroup): # TODO: Похоже, что стейты недоступны во вложенных роутерах
    city_choice = State()
    date_choice = State()


class Application(StatesGroup): # Не уверен, что стейты будут доступны во вложенных роутерах
    people_num_choice = State()


@router.message(StateFilter(None), F.text.lower().contains("forecast"))
async def start_weather(message: Message, state: FSMContext) -> None:
    await message.answer("Provide city for checking forecast")
    await state.set_state(Forecast.city_choice)


@router.message(StateFilter(None), F.text.lower().contains("application"))
async def start_weather(message: Message, state: FSMContext) -> None:
    await message.answer("Ok, you need application")
    await state.set_state(Application.people_num_choice)


@router.message(StateFilter(None))
async def start_weather(message: Message) -> None:
    await message.answer("I don't understand you")
