from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from FSM import Forecast
from keyboards import general as g, forecast as f
from helpers import get_forecast
import re
from datetime import datetime, timedelta
import spacy


router = Router()


NER = spacy.load("en_core_web_sm")


@router.message(StateFilter(Forecast.city_choice))
async def fcast_get_city(message: Message, state: FSMContext) -> None:
    """
    Get city for forecast
    """
    # TODO: complete city extraction implementation
    if (len(message.text) > 1 and len(message.text) < 20):

        # Extract cities from message
        doc = NER(message.text)
        cities = [ent.text for ent in doc.ents if ent.label_=="GPE"]

        # Check if number of cities != 1
        if len(cities) == 0:
            await message.reply("Couldn't find any cities in your message. Try again.")
            return
        elif len(cities) > 1:
            await message.reply("I can't multitask, sorry. I'll try to find a forecast for 1st city.")

        await state.update_data(city=cities[0])
        await message.answer(
            "Specify the date.\n"
            + "<i>We can check forecast for 5 days from now.</i>",
            reply_markup=f.date_kb(),
            input_field_placeholder="DD.MM.YYYY"
        )
        await state.set_state(Forecast.date_choice)

    else:
        await message.reply("It doesn't seem like a city name. Try again.")

@router.message(StateFilter(Forecast.date_choice))
async def fcast_get_date(message: Message, state: FSMContext) -> None:
    """
    Get date for forecast
    """
    # Check if user wants to change city
    if "change" in message.text.lower():
        await message.answer(
            "Provide new city.\n"
            + "<i>e.g. \"Budva\"</i>",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.set_state(Forecast.city_choice)
        return

    # Check if message has "tomorrow"
    if "tomorrow" in message.text.lower():
        date = datetime.now() + timedelta(days=1)

    # Check if message has date
    else:
        date_pattern = re.compile(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b')
        match = date_pattern.search(message.text)

        # Reprompt if no date in message
        if not match:
            await message.reply("There is no correct date in message. Please write as DD.MM.YYYY.")
            return

        # Repromt if date is not in correct range
        date = datetime.strptime(match.group(), "%d.%m.%Y")
        cur_date = datetime.now()
        td = date - cur_date
        if td.days < 0 or td.days > 4:
            await message.reply("Date must be in 4 days range from today.")
            return

    # Provide forecast if date is correct
    if date:
        user_data = await state.get_data()
        forecast = get_forecast.get(user_data["city"], date)

        if not forecast:
            await message.answer(
                "My apology, I couldn't get forecast. Try later, please.",
                reply_markup=g.fcast_or_app_kb(),
                input_field_placeholder="Select option"
            )
            return

        await message.answer(
            f"That's forecast for {user_data['city'].capitalize()}, {date.strftime('%d.%m.%Y')}: \n"
            f"{forecast}"
        )

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