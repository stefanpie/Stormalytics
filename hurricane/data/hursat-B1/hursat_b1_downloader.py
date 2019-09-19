#import netCDF4
import urllib.request as rq
import requests
import os
import sys

BASE_URL = "https://www.ncei.noaa.gov/data/hurricane-satellite-hursat-b1/archive/v06/"


#Returns a set of filenames that have already been downloaded
def get_downloaded_hurricanes():
    try:
        to_return = set()
        index = open("index.csv", "r")
        lines = index.readlines()[1:]
        for line in lines:
            to_return.add(line.split(",")[0])
        index.close()
        return to_return
    except FileNotFoundError:
        return set()


#Find the links that exist on a page
def find_links(url):
    found_links = []
    lines = requests.request("GET", url).text.split("\n")
    for line in lines:
        if "<tr><td" == line[:7]:
            found_links.append(url + line.split("\"")[3])
    return found_links[1:] #ignore the parent dir link


#if the csv is empty, adds the labels
def prep_csv():
    index = open("index.csv", "a")
    if os.path.getsize("index.csv") == 0: #if the file is empty
        index.write("filename, start_year, start_day, hemisphere, lat, lon, name, acquisition_date\n")
    index.close()


#Given a filename, adds to the csv file with relevant metadata.
def filename_to_csv(filename):
    index = open("index.csv", "a")
    split_by_underscore = filename.split("_")
    start_year = split_by_underscore[3][:4]
    start_day = split_by_underscore[3][4:7]
    hemisphere = split_by_underscore[3][7]
    latitude = split_by_underscore[3][8:10]
    longitude = split_by_underscore[3][10:]
    name = split_by_underscore[4]
    acquisition_date = split_by_underscore[5][1:9]
    index.write("{0},{1},{2},{3},{4},{5},{6},{7}\n".format(filename, start_year, start_day, hemisphere, latitude,
                                                           longitude, name, acquisition_date))
    index.close()


#does the stuff
def main():
    prep_csv()
    downloaded_hurricanes = get_downloaded_hurricanes()
    os.makedirs("data", exist_ok=True)  # Makes the data folder if it's not already there
    year_links = find_links(BASE_URL)
    for year_link in year_links:
        print("Entering folder {}".format(year_link))
        file_links = find_links(year_link)
        for file_link in file_links:
            filename = file_link.split("/")[-1] #get the filename from the URL
            if filename not in downloaded_hurricanes:
                print("Downloading {}".format(filename))
                try:
                    rq.urlretrieve(file_link, "data/{}".format(filename))
                    filename_to_csv(filename)
                except Exception:
                    print("Failed to download file")
            else:
                print("{} already in index.csv; skipped".format(filename))


if __name__ == "__main__":
    sys.exit(main())


