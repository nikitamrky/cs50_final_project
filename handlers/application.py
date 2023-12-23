from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from FSM import Forecast, Application
from keyboards import application as a
from helpers import utils
from datetime import datetime


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
        await message.answer(
            "What city do you want to visit? \n<i>e.g. Istanbul</i>",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Application.city_choice)

    # Ask number of people if cur_state == "Forecast.result"
    else:
        await message.answer(
            "How many people will go on the tour?",
            reply_markup=a.people_kb()
        )
        await state.set_state(Application.people_num_choice)


@router.message(StateFilter(Application.city_choice))
async def app_people(message: Message, state: FSMContext) -> None:
    """
    Ask how many people go on tour
    """

    await message.answer(
        "How many people will go on the tour?",
        reply_markup=a.people_kb()
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
    await state.update_data(people_num=people_num)
    await message.answer(
        "What is the expected budget for the trip in US dollars? \n <i>e.g. \"1200\"</i>",
        reply_markup=a.budget_kb()
    )
    await state.set_state(Application.budget_choice)


@router.message(StateFilter(Application.budget_choice))
async def app_trip_date(message: Message, state: FSMContext) -> None:
    """
    Ask trip date
    """

    # Navigate to previous state
    if message.text == "Change number of people":
        await message.answer(
            "How many people will go on the tour?",
            reply_markup=a.people_kb(),
        )
        await state.set_state(Application.people_num_choice)
        return

    # Delete spaces and commas/dots if any
    s = message.text.replace(" ", "")
    s = message.text.replace(".", "")
    s = message.text.replace(",", "")

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
    await state.update_data(budget=budget)
    await message.answer(
        "Provide the approximate start date of your trip as DD/MM/YYYY.",
        reply_markup=a.trip_date_kb()
    )
    await state.set_state(Application.date_choice)


@router.message(StateFilter(Application.date_choice))
async def app_trip_duration(message: Message, state: FSMContext) -> None:
    """
    Ask for trip duration
    """

    # Navigate to previous state
    if message.text == "Change budget":
        await message.answer(
            "What is the expected budget for the trip in US dollars? \n<i>e.g. \"1200\"</i>",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Application.budget_choice)
        return

    # Reprompt if no right formatted date in answer
    date_str = await utils.get_date(message)
    if not date_str:
        return

    # Reprompt if date has passed
    else:
        try:
            date = datetime.strptime(date_str, "%d.%m.%Y")
        except:
            try:
                date = datetime.strptime(date_str, "%d/%m/%Y")
            except:
                await message.answer("Coundn't parse date from your message. Please enter it again.")
                return
        cur_date = datetime.now()
        td = date - cur_date
        if td.days < 0:
            await message.reply("We can't send you to the past! Please enter correct date as DD.MM.YYYY.")
            return

    # Save data and ask for trip duration
    await state.update_data(start_date=date_str)
    await message.answer(
        "Approximately how many days do you want to travel?",
        reply_markup=a.trip_duration_kb()
    )
    await state.set_state(Application.duration_choice)


@router.message(StateFilter(Application.duration_choice))
async def app_name(message: Message, state: FSMContext) -> None:
    """
    Ask if name from Telegram is correct.
    If not, ask user name.
    """

    # Navigate to previous state
    if message.text == "Change start date":
        await message.answer(
            "Provide the approximate start date of your trip as DD/MM/YYYY.",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Application.date_choice)
        return

    # Repromt if no integer in message
    try:
        duration = int(message.text)
    except:
        await message.reply(
            "Please provide an integer of days, e.g. \"10\".\n" \
            "Or send \"/start\" command."
        )
        return

    # Reprompt if duration is negative or more than 30 days:
    if duration < 1 or duration > 30:
        await message.reply(
            "Sorry, we can only offer tours from 1 to 30 days.\n" \
            "Please change duration or send \"/start\" command."
        )
        return

    # Save data
    await state.update_data(duration=duration)

    # Get user name and ask if it is correct
    name = message.from_user.full_name
    await state.update_data(name=name)
    await message.answer(
        f"Is your name {name}?\n" \
        f"Please send \"yes\" or write correct name",
        reply_markup=a.username_kb()
    )
    await state.set_state(Application.name)



@router.message(StateFilter(Application.name))
async def app_phone(message: Message, state: FSMContext) -> None:
    """
    Save user's name and ask phone number.
    """

    # Navigate to previous state
    if message.text == "Change trip duration":
        await message.answer(
            "Approximately how many days do you want to travel?",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Application.duration_choice)
        return

    # Udpate name if answer was not "yes"
    if not message.text.lower() == "yes":
        await state.update_data(name=message.text)

    # Ask phone
    await message.answer(
        "Please enter your phone number, we will contact you during business hours.\n" \
        "<i>e.g. \"617 555−1234\"</i>",
        reply_markup=a.phone_kb()
    )
    await state.set_state(Application.phone)


@router.message(StateFilter(Application.phone))
async def app_final(message: Message, state: FSMContext) -> None:
    """
    Save phone number and ask for confirmation or additional comment.
    """

    # Navigate to previous state
    if message.text == "Change my name":
        await message.answer(
            "Please write your name",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Application.name)
        return

    # Return if there is no valid phone number
    phone = await utils.get_phone(message)
    if not phone:
        return

    # Save data
    await state.update_data(phone=phone)

    # Ask confirmation or additional comment
    data = await state.get_data()
    await message.answer(
        "Wonderful! Please review your application:\n\n" \
        f"<b>Your name: {data['name']}\n" \
        f"Phone number: {data['phone']}\n" \
        f"Trip to: {data['city']}\n" \
        f"Number of participants: {data['people_num']}\n" \
        f"Budget, $: {data['budget']}\n" \
        f"Trip date: {data['start_date']}\n" \
        f"Trip duration, days: {data['duration']}</b>\n\n" \
        "If everything is correct, please write additional comment in next message or press \"Send application\".",
        reply_markup=a.save_app_kb()
    )
    await state.set_state(Application.final)


@router.message(StateFilter(Application.final))
async def app_save(message: Message, state: FSMContext) -> None:
    """
    Confirm application and save in in database
    """

    # Navigate to previous state
    if message.text == "Change phone number":
        await message.answer(
            "Please enter your phone number.\n" \
            "<i>e.g. \"617 555−1234\"</i>",
            reply_markup=ReplyKeyboardRemove()
        )
        await state.set_state(Application.phone)
        return

    # Start application from scratch
    if message.text == "Start from scratch":
        await state.clear()
        await state.set_state(Application.city_choice)
        await message.answer(
            "What city do you want to visit?",
            reply_markup=ReplyKeyboardRemove()
        )
        return

    # Save "-" in comment variable if user didn't provide comment
    if message.text == "Send application":
        comment = "-"

    # Or save comment
    else:
        comment = message.text

    # Save application in database
    data = await state.get_data()
    result = await utils.save_app(data, comment)

    # Inform user if error happened
    if not result:
        await message.answer(
            "Something went wrong: we couldn't save your application.\n" \
            "Please fill another one later.",
            reply_markup=a.final_kb()
        )
        return

    # Comfirm application saving
    await message.answer(
        "<b>Thank you for contacting CS50 Tour!</b>\n" \
        "We have received your application and will get in touch shortly at the provided phone number.",
        reply_markup=a.final_kb()
    )
    await state.clear()