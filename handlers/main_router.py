from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from FSM import Forecast, Application
from handlers import forecast
from handlers import application as app
from helpers import utils as u
from keyboards import general as g, application as a
import spacy


router = Router()


router.include_routers(forecast.router, app.router)


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    """
    Command "/start" handler
    """

    await message.answer(
        "Hi! What do you want: get forecast or fill application?",
        reply_markup=g.fcast_or_app_kb(),
    )
    await state.clear()


@router.message(u.TypeErrorFilter())
async def catchall_default(message: Message) -> None:
    """
    Unsupported message type handler
    """

    await message.answer(
        "Bot understands only when you press buttons on write relevant text."
    )


@router.message(StateFilter(None), F.text.lower().contains("forecast"))
async def start_weather(message: Message, state: FSMContext) -> None:
    """
    Ask city if user chose forecast
    """
    await message.answer(
        "Provide city for checking forecast.\n"
        +"<i>e.g. \"Cambridge\"</i>",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Forecast.city_choice)


@router.message(StateFilter(None), F.text.lower().contains("application"))
@router.message(StateFilter(Forecast.result), F.text.lower().contains("yes"))
async def start_application(message: Message, state: FSMContext) -> None:
    """
    Ask city if wasn't provided
    or
    Ask number of people if city is set in forecast flow
    """
    # Stored into handlers/application.py
    await app.start_points_handler(message, state)


@router.message(F.text.contains(a.main_menu_button_text))
async def main_menu(message: Message, state: FSMContext) -> None:
    """
        Navigate to main menu
    """
    await message.answer(
        "What do you want: get forecast or fill application?",
        reply_markup=g.fcast_or_app_kb(),
    )
    await state.clear()


@router.message(StateFilter(None))
async def catch_all(message: Message) -> None:
    """
        Catch all handler
    """
    await message.answer("Please choose an option")
