import asyncio
from aiogram import types, Dispatcher, Bot, executor
import logging
import requests
from bs4 import BeautifulSoup as BS
import re


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
	await bot.send_message(chat_id=mes_id, text='Введите название трека и исполнителя')


@dp.message_handler(lambda message: message.text.startswith('!'))
async def download_music(message: types.Message):
	request = message.text.split()
	elem = request.pop(0).lstrip('!')
	request.append(elem)
	url = 'https://mp3lav.xn--41a.wiki/search'
	r = requests.get(url, params={
			'query': '%20'.join(request)
		})
	data = BS(r.content, 'html.parser')
	url_song = data.find(class_='special-title')
	url_songg = re.findall('".*?"', str(url_song))[1].strip('"')
	url_song = 'https://mp3lav.xn--41a.wiki' + url_songg
	r = requests.get(url_song)
	data = BS(r.content, 'html.parser')
	find_download_url = data.find_all(class_='btn view-action-btn pull-right')
	download_url = re.findall('".*?"', str(find_download_url))[2].strip('"').split('amp;')
	and_the_end = ''.join(download_url)
	await bot.send_audio(chat_id=message.from_user.id, audio=and_the_end, reply_markup=reply_button())


@dp.callback_query_handler(lambda call: call.data == 'bitcoin')
async def current_bitcoin_rate(call):
	url = 'https://yobit.net/api/2/btc_usd/ticker'
	r = requests.get(url).json()
	await bot.send_message(chat_id=mes_id, text=str(r['ticker']['sell']) + ' ' + 'долларов США', reply_markup=reply_button())


@dp.message_handler(lambda message: message.text == 'Доступные действия')
async def current_bitcoin_rate(message: types.Message):
	global mes_id
	mes_id = message.chat.id
	await bot.send_message(chat_id=mes_id, text='Доступные действия:', reply_markup=get_base_keybord())


def get_base_keybord():
	keyboard = types.InlineKeyboardMarkup(resize_keyboard=True)
	res = types.InlineKeyboardButton(text='Найти песню', callback_data='search_music')
	res1 = types.InlineKeyboardButton(text='Скачать любое приложение бесплатно 😈', callback_data='bitcoi')
	res2 = types.InlineKeyboardButton(text='Курс биткоина', callback_data='bitcoin')
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