from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from FSM import Forecast
from keyboards import general as g, forecast as f


router = Router()


@router.message(StateFilter(Forecast.city_choice))
async def fcast_get_city(message: Message, state: FSMContext) -> None:
    """
    Get city for forecast
    """
    if ("moscow" in message.text.lower()):
        await message.answer(
            "Specify the date.\n"
            + "<i>We can check forecast for 5 days from now.</i>",
            reply_markup=f.date_kb(),
            input_field_placeholder="DD.MM.YYYY"
        )
        await state.set_state(Forecast.date_choice)


@router.message(StateFilter(Forecast.date_choice))
async def fcast_get_date(message: Message, state: FSMContext) -> None:
    """
    Get date for forecast
    """
    if ("04.12.2023" in message.text.lower()) or ("tomorrow" in message.text.lower()):
        await message.answer("That's forecast for Moscow: ...")
        await message.answer(
            "Do you want to go there?",
            reply_markup=g.yes_no_kb()
        )
        await state.set_state(Forecast.result)


@router.message(StateFilter(Forecast.result), F.text.lower().contains("yes"))
async def fcast_continue(message: Message, state: FSMContext) -> None:
    """
    Get positive answer and change flow to aplication fulfilling
    """
    await message.answer("Cool!", reply_markup=ReplyKeyboardRemove()) # TODO: Finish message
    await state.clear() # TODO: change for new state in Application flow


@router.message(StateFilter(Forecast.result), F.text.lower().contains("no"))
async def fcast_continue(message: Message, state: FSMContext) -> None:
    """
    Get negative answer and ask for city again
    """
    await message.answer(
        "OK, write another city and we will check again!",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Forecast.city_choice)