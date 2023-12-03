from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from FSM import Forecast, Application
from handlers import forecast


router = Router()


router.include_routers(forecast.router)


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
