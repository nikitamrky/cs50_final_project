from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from FSM import Forecast, Application
from keyboards import application as a
from helpers import utils

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
        await message.answer(
            "How many people will go on the tour?",
            reply_markup=a.people_kb(),
            input_field_placeholder="Select or send an integer"
        )
        await state.set_state(Application.people_num_choice)


@router.message(StateFilter(Application.city_choice))
async def app_city(message: Message, state: FSMContext) -> None:
    """
    Ask city
    """

    await message.answer(
        "How many people will go on the tour?",
        reply_markup=a.people_kb(),
        input_field_placeholder="Select or send an integer"
    )
    await state.update_data(city=message.text)
    await state.set_state(Application.people_num_choice)


@router.message(StateFilter(Application.people_num_choice))
async def app_budget(message: Message, state: FSMContext) -> None:
    """
    Ask budget
    """

    # If user asks to change city, reprompt him and change state
    if message.text == "Change city":
        await message.answer(
            "What city do you want to visit? \n<i>e.g. Istanbul</i>",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Application.city_choice)
        return

    # Reprompt if answer is no integer
    try:
        people_num = int(message.text)
    except:
        await message.reply("Please provide an integer, e.g. \"3\", or send \"/start\" command.")
        return

    # Reprompt if number of people is less than 0 or more than 20
    if people_num < 1 or people_num > 20:
        await message.reply("Sorry, we can offer tours only for 1-20 people. Please change the number.")
        return

    # Save data and ask budget
    # TODO: add button for changing number of people
    await state.update_data(people_num=people_num)
    await message.answer(
        "What is the expected budget for the trip in US dollars? \n <i>e.g. \"1200\"</i>",
        reply_markup=ReplyKeyboardRemove()
    )
    await state.set_state(Application.budget_choice)


@router.message(StateFilter(Application.budget_choice))
async def app_trip_date(message: Message, state: FSMContext) -> None:
    """
    Ask trip date
    """

    # Delete spaces if any
    s = message.text
    s.replace(" ", "")

    # Repropmt if answer is no integer
    try:
        budget = int(s)
    except:
        await message.reply("Please provide an integer, e.g. \"800\" or \"2000\".")
        return

    # Reprompt if budget is lower than $50 per person
    data = await state.get_data()
    if  budget / data["people_num"] < 50:
        await message.reply(
            "Sorry, we don't have offers cheaper than $50 per person." \
            "Please change budget or send \"/start\" command"
        )
        return

    # Save data and ask start date
    # TODO: add button for changing budget
    await state.update_data(budget=budget)
    await message.answer("Provide the approximate start date of your trip as DD/MM/YYYY.")
    await state.set_state(Application.date_choice)


@router.message(StateFilter(Application.date_choice))
async def app_trip_duration(message: Message, state: FSMContext) -> None:
    """
    Ask for trip duration
    """

    # Reprompt if user wants to change budget

    # Reprompt if no right formatted date in answer
    date_str = await utils.get_date(message)
    if not date_str:
        return

    else:
        # Reprompt if date has passed
        await message.answer(f"Date is {date_str}")



