import urllib.request
import sys
from tqdm import tqdm


BASE_URL = r"https://www.ncei.noaa.gov/data/international-best-track-archive-for-climate-stewardship-ibtracs/v04r00/access/csv/"
serial_number_index_data_file_name = r"IBTrACS_SerialNumber_NameMapping_v04r00_20190919.txt"
main_data_file_name = r"ibtracs.ALL.list.v04r00.csv"



class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_ibtracs():
    print("Downloading " + serial_number_index_data_file_name)
    try:
        with DownloadProgressBar(unit='B', unit_scale=True, miniters=1) as t:
            urllib.request.urlretrieve(BASE_URL + "/" + serial_number_index_data_file_name, "./{}".format(serial_number_index_data_file_name), reporthook=t.update_to)
    except Exception:
        print("Failed to download file")
    
    print("Downloading " + main_data_file_name)
    try:
        with DownloadProgressBar(unit='B', unit_scale=True, miniters=1) as t:
            urllib.request.urlretrieve(BASE_URL + "/" + main_data_file_name, "./{}".format(main_data_file_name), reporthook=t.update_to)
    except Exception:
        print("Failed to download file")


if __name__ == "__main__":
    download_ibtracs()
