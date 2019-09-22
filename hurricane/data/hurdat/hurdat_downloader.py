import urllib.request
import sys
from tqdm import tqdm


BASE_URL = r"https://www.nhc.noaa.gov/data/hurdat/hurdat2-1851-2018-051019.txt"
FILE_NAME = r"hurdat2-1851-2018-051019.txt"


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_hurdat():
    print("Downloading " + FILE_NAME)
    try:
        with DownloadProgressBar(unit='B', unit_scale=True, miniters=1) as t:
            urllib.request.urlretrieve(BASE_URL, "./{}".format(FILE_NAME), reporthook=t.update_to)
    except Exception:
        print("Failed to download file")


if __name__ == "__main__":
    download_hurdat()
