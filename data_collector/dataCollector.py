import requests
import os
import urllib
import bs4
import glob
import subprocess

#testfile = urllib.URLopener()
res = requests.get('https://mesonet-nexrad.agron.iastate.edu/level2/raw/')
soup = bs4.BeautifulSoup(res.text, 'lxml')
i = 0
for link in soup.find_all('a'):
	k = 0
	if (i >= 6):
		print(link['href'])
		res1 = requests.get('https://mesonet-nexrad.agron.iastate.edu/level2/raw/' + link['href'])
		soup1 = bs4.BeautifulSoup(res1.text, 'lxml')
		for link1 in soup1.find_all('a'):
			if (k >= 6):
				if (link1.find_next("a") == None):
					#testfile.retrieve('https://nomads.ncep.noaa.gov/pub/data/nccf/radar/nexrad_level2/' + link['href'] + link1['href'], "./out/" + link['href'])
					os.system("wget -O ./in/" + link['href'][:-1] + " https://mesonet-nexrad.agron.iastate.edu/level2/raw/" + link['href'] + link1['href'])
					print(link['href'] + link1.find_previous("a")['href'])
			k = k + 1
	i = i + 1

path = '.'
filenames = glob.glob(path + '/in/*')
for filename in filenames: #runs through all files in ./in
	subprocess.call(["java", "-classpath", "toolsUI-4.6.11.jar", "ucar.nc2.FileWriter", "-in", filename, "-out", filename + ".nc"]) #uses unidata tool to convert files
	subprocess.call(["rm", filename + ".uncompress"]) #deletes uncompressed files
	subprocess.call(["mv", filename + ".nc", "./out"]) #moves files to ./out
