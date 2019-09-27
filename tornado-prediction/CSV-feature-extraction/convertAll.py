import subprocess
import glob
import os

folder = './out'
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
		print ("Creation of the /out directory failed")

path = '.'
filenames = glob.glob(path + '/in/*')
for filename in filenames: #runs through all files in ./in
	subprocess.call(["java", "-classpath", "toolsUI-4.6.11.jar", "ucar.nc2.FileWriter", "-in", filename, "-out", filename + ".nc"]) #uses unidata tool to convert files
	subprocess.call(["rm", filename + ".uncompress"]) #deletes uncompressed files
	subprocess.call(["mv", filename + ".nc", "./out"]) #moves files to ./out