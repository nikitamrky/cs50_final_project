import asyncio
import re
import sqlite3

from aiogram.types import Message
from aiogram.filters import Filter
from aiogram import F


# Filter all types of messages but regular text
class TypeErrorFilter(Filter):
    """
    Filter for non-text message types
    """
    async def __call__(self, message: Message) -> bool:
        types = [
            "audio",
            "document",
            "photo",
            "sticker",
            "video",
            "voice",
            "video_note",
            "contact",
            "location",
            "venue",
            "poll",
            "dice"
        ]
        l = dir(message)
        return any(
            getattr(message, i, None) for i in l if i in types
        )


async def get_date(message: Message) -> str:
    """
    Find formatted date in string (DD.MM.YYYY).
    Repromt user if no date in string.
    """

    # Search for date
    date_pattern = re.compile(r'\b\d{1,2}[./]\d{1,2}[./]\d{4}\b')
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
    phone_pattern = re.compile(r'\(?\d{3}\)?[−\-_.\s]?(\d{1}[−\-_.\s]?){7}')
    match = phone_pattern.search(message.text)

    # Reprompt if no phone number in message
    if not match:
        await message.reply(
            "There doesn't seem to be a valid phone number here." \
            "Please enter phone number, e.g. \"(617)555−1234\", or send \"/start\" command."
        )
        return

    return match.group()


def save_app(data: dict, comment: str) -> bool:
    """
    Save user application in database and return true if successful.
    """

    # Connect to database in order to save user applications
    conn = sqlite3.connect('applications.db')
    db = conn.cursor()

    try:
        db.execute(
            "INSERT INTO applications (name, phone, city, people, budget, start_date, duration, comment) " \
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                data['name'],
                data['phone'],
                data['city'],
                int(data['people_num']),
                int(data['budget']),
                data['start_date'],
                int(data['duration']),
                comment
            )
        )
        conn.commit()
    except:
        conn.close()
        return False

    conn.close()
    return True