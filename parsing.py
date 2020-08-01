import requests
import re
from bs4 import BeautifulSoup as BS
import asyncio


async def download_music(request):
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
	r = requests.get(and_the_end)
	data = BS(r.content, "html.parser")
	await asyncio.sleep(5)
	find_class = data.find_all(class_="download-button")[0]
	find_url = re.findall('".*?"', str(find_class))[0].strip('"')
	return find_url


def download_app(request):
	try:
		all_params = {}
		url = 'https://pdalife.ru/search/'
		base_url = 'https://pdalife.ru'
		the_outcome = url + '-'.join(request)
		r = requests.get(the_outcome)
		data = BS(r.content, 'html.parser')
		find_url_for_app = data.find(class_='color-android')
		rs_find_url_for_app = re.findall('/.*?l', str(find_url_for_app))[0]
		app = base_url + str(rs_find_url_for_app)
		r = requests.get(app)
		data = BS(r.content, 'html.parser')
		name_app = data.find_all(class_='publication-title')[0].get_text()
		picture = data.find_all(class_='game__poster-picture')[0]
		url_picture = re.findall('"h.*"', str(picture))[0].strip('"')
		app_description = data.find_all(class_='game__description text')[0].get_text().split('\n')
		all_params['name_app'] = name_app
		all_params['picture'] = url_picture
		all_params['description'] = app_description[0]
		all_params['download_url'] = app
		return all_params
	except:
		pass

