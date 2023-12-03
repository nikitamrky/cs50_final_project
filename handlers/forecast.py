from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from FSM import Forecast


router = Router()


@router.message(StateFilter(Forecast.city_choice))
async def fcast_get_city(message: Message, state: FSMContext) -> None:
    """
    Get city for forecast
    """
    if ("moscow" in message.text.lower()):
        await message.answer(
            "Specify the date in the format DD.MM.YYYY. \n"
            + "<i>We can check forecast for 5 days from now</i>"
        )
        await state.set_state(Forecast.date_choice)


@router.message(StateFilter(Forecast.date_choice))
async def fcast_get_date(message: Message, state: FSMContext) -> None:
    """
    Get date for forecast
    """
    if "04.12.2023" in message.text:
        await message.answer("That's forecast for Moscow: ...")
        await message.answer("Do you want to go there?")
        await state.set_state(Forecast.result)