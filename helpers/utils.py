import asyncio
import re
from aiogram.types import Message
import sqlite3


# Connect to database in order to save user applications
conn = sqlite3.connect('applications.db')
db = conn.cursor()


async def get_date(message: Message) -> str:
    """
    Find formatted date in string (DD.MM.YYYY).
    Repromt user if no date in string.
    """

    # Search for date
    date_pattern = re.compile(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b')
    match = date_pattern.search(message.text)

    # Reprompt if no date in message
    if not match:
        await message.reply(
            "There is no correct date in message." \
            "Please enter date as DD.MM.YYYY or send \"/start\" command."
        )
        return

    return match.group()


async def get_phone(message: Message) -> str:
    """
    Find phone number in string (e.g. "(617)555−1234").
    Reprompt user if no phone number in string.
    """

    # Search for string
    phone_pattern = re.compile(r'(\(?\d{3}\)?[-.\s]?(\d{1}[-.\s]?){7})')
    match = phone_pattern.search(message.text)

    # Reprompt if no phone number in message
    if not match:
        await message.reply(
            "There doesn't seem to be a valid phone number here." \
            "Please enter phone number, e.g. \"(617)555−1234\", or send \"/start\" command."
        )
        return

    return match.group()


async def save_app(data: dict, comment: str) -> bool:
    """
    Save user application in database and return true if successful.
    """
    try:
        db.execute(
            "INSERT INTO applications (name, phone, city, people, budget, start_date, duration, comment)" \
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                data['name'],
                data['phone'],
                data['city'],
                data['people_num'],
                data['budget'],
                data['start_date'],
                data['duration'],
                comment
            )
        )
    except:
        return False

    return True