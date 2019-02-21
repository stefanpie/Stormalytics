import subprocess
import sys
import os
subprocess.call(["java", "-classpath", "toolsUI-4.6.11.jar", "ucar.nc2.FileWriter", "-in", sys.argv[1], "-out", sys.argv[2]]) #uses commandline to run converter tool jar file
os.system("rm " + sys.argv[1] + ".uncompress") #deletes uncompressed file
