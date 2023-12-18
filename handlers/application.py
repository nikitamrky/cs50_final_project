from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from FSM import Forecast, Application
from keyboards import application as a


router = Router()


async def start_points_handler(message: Message, state: FSMContext) -> None:
    """
    Handle both starting points:
    - After /start command (without defined city)
    - From forecast result
    """
    cur_state = await state.get_state()

    # If user got here after /start command
    if cur_state == None:
        await message.answer("What city do you want to visit? \n<i>e.g. Istanbul</i>")
        await state.set_state(Application.city_choice)

    # Ask number of people if cur_state == "Forecast.result"
    else:
        # TODO: make a keyboard with options
        await message.answer(
            "How many people will go on the tour?",
            reply_markup=a.people_kb()
        )
        await state.set_state(Application.people_num_choice)


@router.message(StateFilter(Application.city_choice))
async def app_city(message: Message, state: FSMContext) -> None:
    # TODO: make a keyboard with options
    await message.answer(
        "How many people will go on the tour?",
        reply_markup=a.people_kb()
    )
    await state.update_data(city=message.text)
    await state.set_state(Application.people_num_choice)


@router.message(StateFilter(Application.people_num_choice))
async def app_city(message: Message, state: FSMContext) -> None:
    pass
    # TODO: Extract number of people from text
    # TODO: Add a keyboard with suggestions