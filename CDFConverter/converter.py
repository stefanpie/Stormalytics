import subprocess
import sys
subprocess.call(["java", "-classpath", "toolsUI-4.6.11.jar", "ucar.nc2.FileWriter", "-in", sys.argv[1], "-out", sys.argv[2]]) #uses commandline to run converter tool jar file
subprocess.call(["rm", sys.argv[1] + ".uncompress"]) #deletes uncompressed file
