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

filenames = os.listdir('./in/')
for filename in filenames: #runs through all files in ./in
	print(filename)
	subprocess.call(["java", "-classpath", "toolsUI-4.6.14.jar", "ucar.nc2.FileWriter", "-in", "./in/"+filename, "-out", "./out/"+filename+".nc"]) #uses unidata tool to convert files
	# subprocess.call(["rm", filename + ".uncompress"]) #deletes uncompressed files
	# subprocess.call(["mv", filename + ".nc", "./out"]) #moves files to ./out
	# os.replace("./in/"+filename + ".nc", "./out/"+filename+".nc")
