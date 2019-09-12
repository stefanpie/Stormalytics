import subprocess
import glob
path = '.'
filenames = glob.glob(path + '/in/*')
for filename in filenames: #runs through all files in ./in
	subprocess.call(["java", "-classpath", "toolsUI-4.6.11.jar", "ucar.nc2.FileWriter", "-in", filename, "-out", filename + ".nc"]) #uses unidata tool to convert files
	subprocess.call(["rm", filename + ".uncompress"]) #deletes uncompressed files
	subprocess.call(["mv", filename + ".nc", "./out"]) #moves files to ./out
