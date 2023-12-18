import asyncio
import re
from aiogram.types import Message

async def get_date(message: Message) -> re.Match:
    """
    Find formatted date in string (DD.MM.YYYY).
    Repromt user if no date in string.
    """

    # Search for date
    date_pattern = re.compile(r'\b\d{1,2}\.\d{1,2}\.\d{4}\b')
    match = date_pattern.search(message.text)

    # Reprompt if no date in message
    if not match:
        await message.reply("There is no correct date in message. Please write as DD.MM.YYYY.")
        return

    return match.group()

