from aiogram import types, Bot, executor, Dispatcher
import asyncio
import logging


TOKEN = '1305472584:AAEzdWPaSWiW9Xv6EobStVFuJA_zBLF_dq4'
bot = Bot(TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def hello_user(message: types.Message):
	await message.answer('Hello')


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)