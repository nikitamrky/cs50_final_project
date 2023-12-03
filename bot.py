import asyncio
import logging
from os import getenv
from aiogram import Bot, Dispatcher, Router, F
from aiogram.types import Message
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from handlers import main_router
from handlers.type_error import TypeErrorFilter


async def main():


    # Enable logging
    logging.basicConfig(level=logging.INFO)


    # Bot token can be obtained via https://t.me/BotFather
    TOKEN = getenv("BOT_TOKEN")
    if TOKEN == None:
        print("Environment variable BOT_TOKEN not found")
        exit(1)


    # Bot instanse
    bot = Bot(token=TOKEN)


    # Make root router (dispatcher) and define storage type for FSM
    dp = Dispatcher(storage=MemoryStorage())


    # Include routers in dispatcher
    dp.include_routers(main_router.router)
    # TODO: dp.include_routers(...)


    # Start command handler
    @dp.message(CommandStart())
    async def cmd_start(message: Message) -> None:
        await message.answer(
            "Hi! What do you want: get forecast or fill an application?",
            # TODO: reply_markup=
        )


    # Bacis catch all handler
    @dp.message(TypeErrorFilter())
    async def catchall_default(message: Message) -> None:
        await message.answer(
            "I understand only when you press buttons on write relevant text."
        )
        # TODO: Reprompt user


    # Launch bot and ingore all collected incoming messages
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
