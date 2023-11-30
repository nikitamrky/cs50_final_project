from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup


router = Router()


@router.message(StateFilter(Forecast))
async def start_weather(message: Message, state: FSMContext) -> None:
    if state.get_state() == "Forecast.city_choice" and message.text.contains("moscow"):
        await message.answer("Forecast for Moscow: ...")