converter.py and convertAll.py execute a .jar tool in the command line to convert NEXRAD level 2 data into a more usable netCDF format.  converter.py converts one file at a time, while convertAll.py connverts multiple files at a time.

Download toolsUI.jar and netCDFAll.jar from https://github.com/Unidata/thredds/releases/tag/v4.6.11 
and place those jar files in the same directory as converter.py or convertAll.py.

To use converter.py, execute "python converter.py [NEXRAD level 2 data input file name] [desired output file name].nc" in your command line

To use convertAll.py, you must have a directory named "in" and a directory named "out" in the directory where you placed convertAll.py.  Then place all NEXRAD level 2 data in the "in" directory.  Then execute "python convertAll.py" in the command line, and all NEXRAD level 2 data will be converted into a netCDF format and be placed in the "out" directory.

In order to use this tool, you must have Java and Python installed on your system
