import asyncio
import logging
from os import getenv
from aiogram import Bot, Dispatcher, Router
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import main_router


# Telegram bot link: https://t.me/cs50_tour_bot


async def main():

    # Enable logging
    logging.basicConfig(level=logging.INFO)

    # Bot token can be obtained via https://t.me/BotFather
    TOKEN = getenv("BOT_TOKEN")
    if TOKEN == None:
        print("Environment variable BOT_TOKEN not found")
        exit(1)

    # Get openweathermap.org API key
    API_KEY = getenv("WEATHER_API_KEY")
    if API_KEY == None:
        print("Environment variable WEATHER_API_KEY not found")
        exit(1)

    # Bot instanse
    bot = Bot(token=TOKEN, parse_mode="HTML")

    # Make root router (dispatcher) and define storage type for FSM
    dp = Dispatcher(storage=MemoryStorage())

    # Include routers in dispatcher
    dp.include_routers(main_router.router)

    # Launch bot and ingore all collected incoming messages
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
