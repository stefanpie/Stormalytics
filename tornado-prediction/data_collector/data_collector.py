import urllib
import urllib.request
import csv
import re

import socket
old_getaddrinfo = socket.getaddrinfo
def new_getaddrinfo(*args, **kwargs):
    responses = old_getaddrinfo(*args, **kwargs)
    return [response
            for response in responses
            if response[0] == socket.AF_INET]
socket.getaddrinfo = new_getaddrinfo

base_url = r"https://mesonet-nexrad.agron.iastate.edu/level2/raw/"

s_list = []

with open('stations.csv', 'r') as csvfile:
    s_list = [str(row[0]) for row in csv.reader(csvfile)]
s_list = s_list[1:]


file_list = []
	
for s in s_list:
	radar_url = base_url + s + "/"
	print(radar_url)
	html = ""
	with urllib.request.urlopen(radar_url) as response:
		html = response.read()
	html = html.decode('utf-8')
	links = re.findall(r'"([A-Z]+_\d+_\d+)"', html)
	links.sort(reverse=True)
	if links:
		print(s + "/" + str(links[0]))
		file_list.append(s + "/" + str(links[0]))
	
print(file_list)
	
#urllib.urlretrieve('http://example.com/file.ext', '/path/to/dir/filename.ext')