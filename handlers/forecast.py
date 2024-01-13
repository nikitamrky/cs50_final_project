import re
from datetime import datetime, timedelta

from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from FSM import Forecast, Application
import spacy

from keyboards import general as g, forecast as f
from helpers import get_forecast


# Create new router
router = Router()


NER = spacy.load("en_core_web_sm")


@router.message(StateFilter(Forecast.city_choice))
async def fcast_get_city(message: Message, state: FSMContext) -> None:
    """
    Get city for forecast
    """

    # Navigate to application flow
    if message.text == "Fill application":
        await message.answer(
            "What city do you want to visit? \n<i>e.g. Istanbul</i>",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Application.city_choice)
        return

    # Reprompt if string length is too short or long
    if not (len(message.text) > 1 and len(message.text) < 20):
        await message.reply("It doesn't seem like a city name. Try again.")
        return

    # Extract cities from message
    doc = NER(message.text)
    cities = [ent.text for ent in doc.ents if ent.label_=="GPE"]
    cities = [ent.text for ent in doc.ents if ent.label_=="GPE"]

    if len(cities) > 1:
        await message.reply("I can't multitask, sorry. I'll try to find a forecast for 1st city.")

    if cities:
        await state.update_data(city=cities[0])
    else:
        await state.update_data(city=message.text)
    await message.answer(
        "Specify the date.\n"
        + "<i>We can check forecast for tomorrow or 3 days ahead.</i>",
        reply_markup=f.date_kb(),
    )
    await state.set_state(Forecast.date_choice)


@router.message(StateFilter(Forecast.date_choice))
async def fcast_get_date(message: Message, state: FSMContext) -> None:
    """
    Ask date for forecast
    """
    # Check if user wants to change city
    if "change" in message.text.lower():
        await message.answer(
            "Provide new city.\n"
            + "<i>e.g. \"Milan\"</i>",
            reply_markup=ReplyKeyboardRemove(),
        )
        await state.update_data(city=None)
        await state.set_state(Forecast.city_choice)
        return

    # Navigate to application flow
    if "application" in message.text.lower():
        await message.answer("What city do you want to visit? \n<i>e.g. Istanbul</i>")
        await state.set_state(Application.city_choice)
        return

    # Check if message has "tomorrow"
    if "tomorrow" in message.text.lower():
        date = datetime.now() + timedelta(days=1)

    # Check if message has date
    # TODO: implement utils.get_date function instead of this stupid code
    else:
        date_pattern = re.compile(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b')
        match = date_pattern.search(message.text)

        # Reprompt if no date in message
        if not match:
            await message.reply("There is no correct date in message. Please enter date as DD.MM.YYYY.")
            return

        # Repromt if date is not in correct range
        date = datetime.strptime(match.group(), "%d.%m.%Y")
        cur_date = datetime.now()
        td = date - cur_date
        if td.days < 0 or td.days > 4:
            await message.reply("Date must be in 4 days range starting tomorrow.")
            return

    # Inform user that we are getting forecast ready
    await message.answer("One moment...")

    # Provide forecast if date is correct
    if date:
        user_data = await state.get_data()
        forecast = await get_forecast.get(user_data["city"], date)

        if not forecast:
            await message.answer(
                "My apology, I couldn't get forecast. Maybe <b>city name</b> is not correct? Try again, please.",
                reply_markup=ReplyKeyboardRemove()
            )
            await state.set_state(Forecast.city_choice)
            return

        await message.answer(
            f"That's forecast for {user_data['city'].capitalize()}, 12:00 {date.strftime('%d.%m.%Y')}: \n"
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
        reply_markup=f.new_city_kb()
    )
    await state.set_state(Forecast.city_choice)