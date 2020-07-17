from aiogram import types, Bot, executor, Dispatcher
import asyncio
import logging
import youtube_dl
import os


TOKEN = '1305472584:AAEzdWPaSWiW9Xv6EobStVFuJA_zBLF_dq4'
bot = Bot(TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def hello_user(message: types.Message):
	await message.answer('Hello')
	await message.answer(os.getcwd())

@dp.message_handler(commands=['get_music'])
async def get_music(message: types.Message):
	await message.answer('Вставьте ссылку на трек с youtube')
	global last_message
	last_message = message.text


@dp.message_handler(lambda message: message.startswith('https'))
async def send_mus(message: types.Message):
	if last_message == '/get_music':
		url = message.text
		ydl_opts = {
			'format': 'bestaudio/best',
			'postprocessors': [{
				'key': 'FfmpegExtractAudio',
				'preferredcodec': 'mp3',
				'preferredquality': '192'
			}],
		}

		with youtube_dl.YoutubeDL(ydl_opts) as f:
			await message.answer('Загрузка началась')
			f.download([message.text])


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)