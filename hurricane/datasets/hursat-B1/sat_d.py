from bs4 import BeautifulSoup
import requests
import os
import urllib
from itertools import repeat
from joblib import Parallel, delayed
import tarfile
from pprint import pprint

BASE_URL = 'https://www.ncei.noaa.gov/data/hurricane-satellite-hursat-b1/archive/v06/'

def list_file_dir(url, ext=''):
    page = requests.get(url).text
    # print (page)
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.select('table tr:nth-child(n+4) a')]

def download_hursat_b1_file(link, data_dir):
    file_name = link.split("/")[-1]
    print(file_name)
    os.makedirs(data_dir+"hursat-b1/raw_data/", exist_ok=True) 
    urllib.request.urlretrieve(link, data_dir+"hursat-b1/raw_data/"+file_name)

def extract_hursat_b1_tar_gz_file(fp, data_dir):
    dir_name  = os.path.basename(fp).replace('.tar.gz', '')
    print(dir_name)
    os.makedirs(data_dir+"hursat-b1/raw_data_extracted/", exist_ok=True)
    with tarfile.open(fp, "r:gz") as tar:
        tar.extractall(data_dir+"hursat-b1/raw_data_extracted/"+dir_name+"/")

def download_hursat_b1(data_dir):
    hurricane_file_links = []

    year_folders = list_file_dir(BASE_URL)
    year_folders = [x for x in year_folders if int(x[-5:-1]) > 1979]
    for year_folder in year_folders:
        for hurricane_file in list_file_dir(year_folder): 
            hurricane_file_links.append(hurricane_file)
    print(hurricane_file_links.__len__())
    # for data_url in hurricane_file_links:
    #     download_hursat_b1_file(data_url, data_dir)
    Parallel(n_jobs=-1, verbose=0)(delayed(download_hursat_b1_file)(data_url, data_dir) for data_url in hurricane_file_links)

def post_download_extract_hursat_b1(data_dir):
    hursat_b1_tar_gz_files = []
    for file in os.listdir(data_dir + 'hursat-b1/raw_data/'):
        if file.endswith(".tar.gz"):
            hursat_b1_tar_gz_files.append(os.path.join(data_dir + 'hursat-b1/raw_data/', file))
    # print(hursat_b1_tar_gz_files)
    for f in hursat_b1_tar_gz_files[:]:
        extract_hursat_b1_tar_gz_file(f, data_dir)

if __name__ == "__main__":
    DATA_DIR = "../../data/"
    # download_hursat_b1(DATA_DIR)
    post_download_extract_hursat_b1(DATA_DIR)