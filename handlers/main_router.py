from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter, CommandStart
from aiogram.fsm.context import FSMContext
from FSM import Forecast, Application
from handlers import forecast
from handlers.type_error import TypeErrorFilter
from keyboards import general as g


router = Router()


router.include_routers(forecast.router)


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
        +"<i>e.g. \"Harvard\"</i>",
        reply_markup=ReplyKeyboardRemove(),
    )
    await state.set_state(Forecast.city_choice)


@router.message(StateFilter(None), F.text.lower().contains("application"))
async def start_weather(message: Message, state: FSMContext) -> None:
    await message.answer("Ok, you need application")
    await state.set_state(Application.people_num_choice)


@router.message(StateFilter(None))
async def start_weather(message: Message) -> None:
    await message.answer("I don't understand you")
