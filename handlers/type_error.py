from aiogram.filters import Filter
from aiogram import F
from aiogram.types import Message

# Filter all types of messages but regular text
class TypeErrorFilter(Filter):
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