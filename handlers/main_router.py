from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from FSM import Forecast, Application
from handlers import forecast
from handlers import application as app
from handlers.type_error import TypeErrorFilter
from keyboards import general as g
import spacy


router = Router()


router.include_routers(forecast.router, app.router)


# "Start" command handler
@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext) -> None:
    await message.answer(
        "Hi! What do you want: get forecast or fill an application?",
        reply_markup=g.fcast_or_app_kb(),
        input_field_placeholder="Select option"
    )
    await state.clear()


# Bacis catch all handler
@router.message(TypeErrorFilter())
async def catchall_default(message: Message) -> None:
    await message.answer(
        "Bot understands only when you press buttons on write relevant text."
    )
    await message.answer(
        "Please select forecast or application."
    )


@router.message(StateFilter(None), F.text.lower().contains("forecast"))
async def start_weather(message: Message, state: FSMContext) -> None:
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


@router.message(StateFilter(None))
async def catch_all(message: Message) -> None:
    await message.answer("I don't understand you")
