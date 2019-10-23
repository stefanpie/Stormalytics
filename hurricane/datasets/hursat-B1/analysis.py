import tarfile
import os
import netCDF4.utils as netcdf

DATA_DIR = "data/"

#unfinished
def data_from_tarball(path):
    os.makedirs("temp")
    file = tarfile.TarFile(path)
    file.extractall("temp/")
    cdfs = os.listdir("temp/")
    for cdf in cdfs:
        pass


def get_all_tarballs(dir):
    return [i for i in os.listdir(dir) if i[-7:] == ".tar.gz"]
