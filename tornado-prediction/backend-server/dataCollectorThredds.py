import requests
import os
import urllib
import bs4
import glob
import subprocess
import urllib.request
import wget
import shutil


folder = './in'
if (os.path.exists(folder)):
	for the_file in os.listdir(folder):
		file_path = os.path.join(folder, the_file)
		try:
			if os.path.isfile(file_path):
				os.unlink(file_path)
		except Exception as e:
			print(e)
else:
	try:
		os.mkdir(folder)
	except OSError:
		print ("Creation of the /in directory failed")

#testfile = urllib.URLopener()
res = requests.get('https://thredds.ucar.edu/thredds/catalog/nexrad/level2/catalog.html')
soup = bs4.BeautifulSoup(res.text, 'lxml')
i = 0
for link in soup.find_all('a'):
	#print(link['href'])
	if (link['href'][0] == 'K'):
		res2 = requests.get('https://thredds.ucar.edu/thredds/catalog/nexrad/level2/' + link['href'])
		#print(link['href'])
		soup2 = bs4.BeautifulSoup(res2.text, 'lxml')
		link2 = soup2.a.find_next('a')
		#print('https://thredds.ucar.edu/thredds/catalog/nexrad/level2/' + link['href'].split('/')[0] + '/' + link2['href'])
		res3 = requests.get('https://thredds.ucar.edu/thredds/catalog/nexrad/level2/' + link['href'].split('/')[0] + '/' + link2['href'])
		soup3 = bs4.BeautifulSoup(res3.text, 'lxml')
		link3 = soup3.a.find_next('a').find_next('a')
		url = 'https://thredds.ucar.edu/thredds/fileServer/nexrad/level2/' + link['href'].split('/')[0] + '/' + link2['href'].split('/')[0] + '/' + link3['href'].split('/')[-1]
		print(link['href'].split('/')[0] + '/' + link2['href'].split('/')[0] + '/' + link3['href'].split('/')[-1])
		wget.download(url, './in/')
		
							

'''
path = '.'
filenames = glob.glob(path + '/in/*')
for filename in filenames: #runs through all files in ./in
	subprocess.call(["java", "-classpath", "toolsUI-4.6.11.jar", "ucar.nc2.FileWriter", "-in", filename, "-out", filename + ".nc"]) #uses unidata tool to convert files
	subprocess.call(["rm", filename + ".uncompress"]) #deletes uncompressed files
	subprocess.call(["mv", filename + ".nc", "./out"]) #moves files to ./out


'''