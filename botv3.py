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
	await message.answer('Привет!')


@dp.message_handler(commands=['search_music'])
async def search_music(message: types.Message):
	await message.answer('Введите название трека и исполнителя')
	name_song_and_singer = message.text


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
	await bot.send_audio(chat_id=message.from_user.id, audio=and_the_end)


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)