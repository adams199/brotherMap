from geocodio import GeocodioClient
from geocodio.exceptions import GeocodioDataError
import csv
import re

DataFile = "oldDataBrotherMap.csv"

geoFile = open('newBrothers.geojson', 'w')
geoFile.write('{"type":"FeatureCollection","features":[\n')

client = GeocodioClient("0c410ad5ac00a2e7a055ade70475c465605a6ed")
geo_pattern = re.compile("'lat': -*[0-9]+.[0-9]+, 'lng': -*[0-9]+.[0-9]+")
num_pattern = re.compile("-*[0-9]+.[0-9]+")
i = 0

with open(DataFile) as f:
    numberofLines = len(f.readlines())
with open(DataFile) as data:
    reader = csv.reader(data, delimiter=",")
    for array in reader:
        name = array[0]           # this is a string
        address = array[1]
        try:
            location = client.geocode(address)
            geo = re.search(geo_pattern, str(location))
            nums = re.findall(num_pattern, geo.group())
            lat = nums[0].strip("'")  # this is a string
            lng = nums[1].strip("'")  # this is a string

            # now to take the lat, long, and name and to build the .geojson...
            geoLine = '\t{"type":"Feature","geometry":{"type":"Point","coordinates":[' +\
                lng + ',' + lat + ']},"properties":{"title":"' + name + '"}}'
            if i < (numberofLines-1):
                geoLine += ',\n'
            geoFile.write(geoLine)
            print(str(i) + " wrote geoFile line")
        except GeocodioDataError:
            print('Could not process '+name+'\nPlease check address: '+address+'\n')
        i += 1
        
geoFile.write('\n]}')
geoFile.close()
