import requests
import os
import urllib
import bs4
import glob
import subprocess
import urllib.request
import wget


#testfile = urllib.URLopener()
res = requests.get('https://mesonet-nexrad.agron.iastate.edu/level2/raw/')
soup = bs4.BeautifulSoup(res.text, 'lxml')
i = 0
for link in soup.find_all('a'):
	k = 0
	if (i >= 6):
		#print(link['href'])
		if (link['href'][0] == 'K'):
			res1 = requests.get('https://mesonet-nexrad.agron.iastate.edu/level2/raw/' + link['href'])
			soup1 = bs4.BeautifulSoup(res1.text, 'lxml')
			for link1 in soup1.find_all('a'):
				if (k >= 6):
					if (link1.find_next("a") == None):
						#testfile.retrieve('https://nomads.ncep.noaa.gov/pub/data/nccf/radar/nexrad_level2/' + link['href'] + link1['href'], "./out/" + link['href'])
						#print(link['href'] + link1['href'])
						#os.system("wget -O ./in/" + link['href'][:-1] + " https://mesonet-nexrad.agron.iastate.edu/level2/raw/" + link['href'] + link1.find_previous("a")['href'])
						filename = link1.find_previous("a").find_previous("a")
						while ('MDM' in filename['href']):
							filename = filename.find_previous("a")
						url = "https://mesonet-nexrad.agron.iastate.edu/level2/raw/" + link['href'] + filename['href']
						wget.download(url, './in/')
						print(link['href'] + filename['href'])
						#subprocess.call(["java", "-classpath", "toolsUI-4.6.11.jar", "ucar.nc2.FileWriter", "-in", "./in/" + link['href'][:-1], "-out", "./in/" + link['href'][:-1] + ".nc"]) #uses unidata tool to convert files
				k = k + 1
	i = i + 1

'''
path = '.'
filenames = glob.glob(path + '/in/*')
for filename in filenames: #runs through all files in ./in
	subprocess.call(["java", "-classpath", "toolsUI-4.6.11.jar", "ucar.nc2.FileWriter", "-in", filename, "-out", filename + ".nc"]) #uses unidata tool to convert files
	subprocess.call(["rm", filename + ".uncompress"]) #deletes uncompressed files
	subprocess.call(["mv", filename + ".nc", "./out"]) #moves files to ./out


'''