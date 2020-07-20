import asyncio
from aiogram import types, Dispatcher, Bot, executor
import logging
import requests
from bs4 import BeautifulSoup as BS
import re
import parsing


TOKEN = '1305472584:AAEzdWPaSWiW9Xv6EobStVFuJA_zBLF_dq4'
bot = Bot(TOKEN)
dp = Dispatcher(bot)
logging.basicConfig(level=logging.INFO)


@dp.message_handler(commands=['start'])
async def start_bot(message: types.Message):
	global mes_id
	mes_id = message.chat.id
	await bot.send_message(chat_id=message.chat.id, text='Привет! Смотри что я могу:', reply_markup=get_base_keybord())


@dp.callback_query_handler(lambda call: call.data == 'search_music')
async def search_music(call):
	global last_message
	last_message = call.data
	await bot.send_message(chat_id=mes_id, text='Введите название песни и исполнителя')


@dp.callback_query_handler(lambda call: call.data == 'bitcoin')
async def current_bitcoin_rate(call):
	url = 'https://yobit.net/api/2/btc_usd/ticker'
	r = requests.get(url).json()
	await bot.send_message(chat_id=mes_id, text=str(r['ticker']['sell']) + ' ' + 'долларов США', reply_markup=reply_button())


@dp.callback_query_handler(lambda call: call.data == 'app')
async def download_app(call):
	global last_message
	last_message = 'app'
	await bot.send_message(chat_id=mes_id, text='Введите название приложения')


@dp.message_handler(lambda message: message.text == 'Доступные действия')
async def current_bitcoin_rate(message: types.Message):
	global mes_id
	mes_id = message.chat.id
	await bot.send_message(chat_id=mes_id, text='Доступные действия:', reply_markup=get_base_keybord())


@dp.message_handler(lambda message: message.text == 'Стоп')
async def current_bitcoin_rate(message: types.Message):
	global last_message
	last_message = '0'


@dp.message_handler(lambda message: message.text)
async def download_files(message: types.Message):
	global last_message, res
	if last_message == 'search_music':
		request = message.text.split()
		result = parsing.download_music(request)
		await bot.send_audio(chat_id=mes_id, audio=result, reply_markup=reply_button())

	elif last_message == 'app':
		app = message.text.split()
		lst = parsing.download_app(app)
		try:
			await bot.send_photo(chat_id=mes_id, photo=lst['picture'], caption=lst['name_app'] + '\n' + lst['description'] + '\n' + lst['download_url'])
		except:
			await bot.send_message(chat_id=mes_id, text='Извините, к сожалению ничего не найдено 😔')



def get_base_keybord():
	keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
	res = types.InlineKeyboardButton(text='Найти песню 🤩', callback_data='search_music')
	res1 = types.InlineKeyboardButton(text='Скачать приложение или игру бесплатно 😈', callback_data='app')
	res2 = types.InlineKeyboardButton(text='Курс биткоина 🤑', callback_data='bitcoin')
	keyboard.add(res)
	keyboard.add(res1)
	keyboard.add(res2)
	return keyboard


def reply_button():
	button = types.ReplyKeyboardMarkup(resize_keyboard=True)
	res = types.KeyboardButton(text='Доступные действия')
	button.add(res)
	return button


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True) 