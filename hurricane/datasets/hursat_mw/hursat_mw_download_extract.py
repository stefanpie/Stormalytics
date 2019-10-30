from bs4 import BeautifulSoup
import requests
import os
import urllib
from itertools import repeat
from joblib import Parallel, delayed
import tarfile
from pprint import pprint
import shutil
import csv



BASE_URL = 'https://www.ncei.noaa.gov/data/hurricane-satellite-hursat-mw/archive/v05/'

def list_file_dir(url, ext=''):
    page = requests.get(url).text
    # print (page)
    soup = BeautifulSoup(page, 'html.parser')
    return [url + '/' + node.get('href') for node in soup.select('table tr:nth-child(n+4) a')]

def download_hursat_mw_file(link, data_dir):
    file_name = link.split("/")[-1]
    print(file_name)
    os.makedirs(data_dir+"hursat_mw/raw_data/", exist_ok=True) 
    urllib.request.urlretrieve(link, data_dir+"hursat_mw/raw_data/"+file_name)

def download_hursat_mw(data_dir):
    hurricane_file_links = []

    year_folders = list_file_dir(BASE_URL)
    year_folders = [x for x in year_folders if int(x[-5:-1]) > 1979]
    for year_folder in year_folders:
        for hurricane_file in list_file_dir(year_folder): 
            hurricane_file_links.append(hurricane_file)
    print(hurricane_file_links.__len__())
    for data_url in hurricane_file_links:
        download_hursat_mw_file(data_url, data_dir)
    # Parallel(n_jobs=-1, verbose=0)(delayed(download_hursat_mw_file)(data_url, data_dir) for data_url in hurricane_file_links)

def extract_hursat_mw_tar_gz_file(fp, data_dir):
    dir_name  = os.path.basename(fp).replace('.tar.gz', '')
    print(dir_name)
    os.makedirs(data_dir+"hursat_mw/raw_data_extracted/", exist_ok=True)
    with tarfile.open(fp, "r:gz") as tar:
        tar.extractall(data_dir+ "hursat_mw/raw_data_extracted/"+dir_name)


def post_download_extract_hursat_mw(data_dir):
    hursat_mw_tar_gz_files = []
    for file in os.listdir(data_dir + 'hursat_mw/raw_data/'):
        if file.endswith(".tar.gz"):
            hursat_mw_tar_gz_files.append(os.path.join(data_dir + 'hursat_mw/raw_data/', file))
    print(hursat_mw_tar_gz_files)
    
    for f in hursat_mw_tar_gz_files:
        extract_hursat_mw_tar_gz_file(f, data_dir)
    # Parallel(n_jobs=-1, verbose=0)(delayed(extract_hursat_mw_tar_gz_file)(f, data_dir) for f in hursat_mw_tar_gz_files)


    for item in os.listdir(data_dir+ "hursat_mw/raw_data_extracted/"):
        base_dir = data_dir+ "hursat_mw/raw_data_extracted/" + item + "/"
        # print(base_dir)
        for root, dirs, files in os.walk(base_dir):
            for file in files:
                fp = os.path.join(root,file).replace("\\", "/")
                # print(fp)
                shutil.move(fp,base_dir) # change you destination dir
        for d in os.listdir(base_dir):
            if os.path.isdir(base_dir + d):
                # print(base_dir + d)
                shutil.rmtree(base_dir + d)
    

def get_index_data_hursat_mw(file_name):
    data = {}
    file_name = os.path.basename(file_name)
    return data

def index_hursat_mw(data_dir):
    data_list = []
    for dirpath, dirnames, filenames in os.walk(data_dir+"hursat_mw/raw_data_extracted/"):
        for filename in [f for f in filenames if f.endswith(".nc")]:
            # print (os.path.join(dirpath, filename))
            data = {}
            print(filename)
            file_strings = filename.split(".")
            # print(file_strings)
            data['cyclone_begin_year'] = int(file_strings[0][0:4])
            data['cyclone_begin_day'] = int(file_strings[0][4:7])
            data['hemisphere'] = file_strings[0][7]
            data['lat'] = int(file_strings[0][8:10])
            data['lon'] = int(file_strings[0][10:13])
            data['storm_name'] = file_strings[1]
            data['acquisition_year'] = int(file_strings[2])
            data['acquisition_month'] = int(file_strings[3])
            data['acquisition_day'] = int(file_strings[4])
            data['acquisition_hour'] = int(file_strings[5][0:2])
            data['acquisition_minute'] = int(file_strings[5][2:4])
            data['view_zenith_angle'] = int(file_strings[6])
            data['isccp_satellite_id'] = file_strings[7]
            data['representative_ibtracs_wind_speed'] = int(file_strings[8])
            data['file_suffix'] = file_strings[9]
            data['file_version'] = file_strings[10]
            data['file_extension'] = file_strings[11]
            data['file_path_in_data_dir'] = os.path.join(dirpath, filename).replace("\\", "/").replace(data_dir, "")
            # print(data)
            data_list.append(data)
    keys = data_list[0].keys()
    with open(data_dir+"hursat_mw/hursat_mw_index.csv", 'w') as output_file:
        dict_writer = csv.DictWriter(output_file, keys)
        dict_writer.writeheader()
        dict_writer.writerows(data_list)



if __name__ == "__main__":
    DATA_DIR = "../../data/"
    download_hursat_mw(DATA_DIR)
    post_download_extract_hursat_mw(DATA_DIR)
    index_hursat_mw(DATA_DIR)