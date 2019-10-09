import urllib.request

print('Downloading ToolsUI jar file...')

url = 'http://artifacts.unidata.ucar.edu/content/repositories/unidata-releases/edu/ucar/toolsUI/4.6.14/toolsUI-4.6.14.jar'
urllib.request.urlretrieve(url, './toolsUI-4.6.14.jar')

print("Done")