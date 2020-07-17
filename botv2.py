from aiogram import types, Bot, executor, Dispatcher
import asyncio
import logging
import requests
import os
from bs4 import BeautifulSoup as BS
import re


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
	await message.answer('Введите название песни и исполнителя')
	global last_message
	last_message = message.text


@dp.message_handler(lambda message: message.text.startswith('!'))
async def send_mus(message: types.Message):
	if last_message == '/get_music':
		lst_sound = message.text.split()
		check = True
		sound, url_with_sound, result, aft = '', '', '', ''
		if len(lst_sound) == 1:
			sound = str(lst_sound[0])
		else:
			for obj in lst_sound:
				if obj != lst_sound[-1]:
					sound += obj
					sound += '+'
				else:
					sound += obj
		r = requests.get('https://zaycev.net/search.html', params={
				'query_search': sound
			})
		data = BS(r.content, 'html.parser')
		s = data.find_all(class_='musicset-track__fullname')
		lst = []
		for i in s:
		    lst.append(i.get_text())
		c = []
		for cont, j in enumerate(lst):
		    a = j.split()
		    ind = a.index('–')
		    del a[ind]
		    for i in lst_sound:
		        res = re.findall(i, j)
		        c.append(res)
		    if (len(c) == len(lst_sound)) and (len(c) == len(a)):
		        ind = cont
		        check = False
		        break
		    c = []
		    if not check:
		    	break

		url_with_sound = re.findall('/.*?l', str(s[ind]))[-1]
		url = 'https://zaycev.net' + url_with_sound
		r = requests.get(url)
		data = BS(r.content, 'html.parser')
		download_class = data.find(class_='button-download__link')
		try:
		    download = re.findall('/.+?n', str(download_class))[0]
		except:
		    await message.answer('Извините, мне не удалось найти трек, возможно позже будет добавлен ресурс')
		result_download_url = 'https://zaycev.net' + download
		await message.answer('Для загрузки трека перейдите по ссылке:\n'result_download_url)


if __name__ == '__main__':
	executor.start_polling(dp, skip_updates=True)
