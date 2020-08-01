import requests
import re
from bs4 import BeautifulSoup as BS
import asyncio


def download_music(request):
	url = 'https://mp3lav.xn--41a.wiki/search'
	r = requests.get(url, params={
			'query': '%20'.join(request)
		})
	data = BS(r.content, 'html.parser')
	url_song = data.find(class_='play-button')
	url_songg = re.findall('h.*?"', str(url_song))[0].strip('"').split('amp;')
	result = ''.join(url_songg)
	return result
	


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

