from geocodio import GeocodioClient
from geocodio.exceptions import GeocodioDataError
import re
import bs4
import requests

URL = 'https://docs.google.com/spreadsheets/d/e/2PACX-1vSD3MRGlkbpxYV3agtpCUShQTCDNHqMHm3-' \
      'fw5AEJXcOzm2uNBBMzeVx1IUNeco2NjCAq3vLoC9H2CD/pub?output=csv'
r = requests.get(URL)
soup = bs4.BeautifulSoup(r.content, 'html5lib')
lines = soup.prettify().split('\n')
brothers = lines[5:-2]
i = 0
geoFile = open('newBrothers.geojson', 'w')
geoFile.write('{"type":"FeatureCollection","features":[\n')

client = GeocodioClient("0c410ad5ac00a2e7a055ade70475c465605a6ed")
geo_pattern = re.compile("'lat': -*[0-9]+.[0-9]+, 'lng': -*[0-9]+.[0-9]+")
num_pattern = re.compile("-*[0-9]+.[0-9]+")

for brother in brothers:
    i += 1
    try:
        data = brother.split(',')
        zip_code = data[1].strip("'")
        name = data[2].strip("'")
        try:
            location = client.geocode(zip_code)
            geo = re.search(geo_pattern, str(location))
            nums = re.findall(num_pattern, geo.group())
            lat = nums[0].strip("'")  # this is a string
            lng = nums[1].strip("'")  # this is a string

            # now to take the lat, long, and name and to build the .geojson...
            geoLine = '\t{"type":"Feature","geometry":{"type":"Point","coordinates":[' + \
                      lng + ',' + lat + ']},"properties":{"title":"' + name + '"}}'
            if i < len(brothers):
                geoLine += ',\n'
            geoFile.write(geoLine)
            print(str(i) + " wrote geoFile line")
        except GeocodioDataError:
            print('Could not process ' + name + '\nPlease check zip code: ' + zip_code + '\n')
    except IndexError:
        print("Error in some data index (possibly commas in zip code or name)")

geoFile.write('\n]}')
geoFile.close()

# old way
# import csv
# DataFile = "oldDataBrotherMap.csv"
#
# with open(DataFile) as f:
#     numberofLines = len(f.readlines())
# with open(DataFile) as data:
#     reader = csv.reader(data, delimiter=",")
#     for array in reader:
#         name = array[0]           # this is a string
#         address = array[1]
#         try:
#             location = client.geocode(address)
#             geo = re.search(geo_pattern, str(location))
#             nums = re.findall(num_pattern, geo.group())
#             lat = nums[0].strip("'")  # this is a string
#             lng = nums[1].strip("'")  # this is a string
#
#             # now to take the lat, long, and name and to build the .geojson...
#             geoLine = '\t{"type":"Feature","geometry":{"type":"Point","coordinates":[' +\
#                 lng + ',' + lat + ']},"properties":{"title":"' + name + '"}}'
#             if i < (numberofLines-1):
#                 geoLine += ',\n'
#             geoFile.write(geoLine)
#             print(str(i) + " wrote geoFile line")
#         except GeocodioDataError:
#             print('Could not process '+name+'\nPlease check address: '+address+'\n')
#         i += 1
#
# geoFile.write('\n]}')
# geoFile.close()
