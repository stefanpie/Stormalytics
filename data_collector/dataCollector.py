import requests
import urllib
import bs4
#testfile = urllib.URLopener()
res = requests.get('https://nomads.ncep.noaa.gov/pub/data/nccf/radar/nexrad_level2/')
soup = bs4.BeautifulSoup(res.text, 'lxml')
i = 0
for link in soup.find_all('a'):
	k = 0
	if (i >= 2):
		res1 = requests.get('https://nomads.ncep.noaa.gov/pub/data/nccf/radar/nexrad_level2/' + link['href'])
		soup1 = bs4.BeautifulSoup(res1.text, 'lxml')
		for link1 in soup1.find_all('a'):
			if (k >= 2):
				if (link1.find_next("a") == None):
					#testfile.retrieve('https://nomads.ncep.noaa.gov/pub/data/nccf/radar/nexrad_level2/' + link['href'] + link1['href'], "./out/" + link['href'])
					print(link['href'] + link1['href'])
			k = k + 1
		print(link['href'])
	i = i + 1