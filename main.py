import csv
import math
from random import uniform

FILENAME = '4G_ - Copy (4).csv'


def runner(name):
    def metersToDecimalDegrees(_lat, _lon, xOffset, yOffset):
        latDD = _lat + (yOffset / 111319.5)
        lonDD = _lon + (xOffset / 82073.34)
        return [latDD, lonDD]

    def calcPointOnCircle(angle, radius):
        xOffset = radius * math.sin(math.radians(angle))
        yOffset = radius * math.cos(math.radians(angle))
        return [xOffset, yOffset]

    def indexDictBuilder(dictRow):
        indexDict = {}
        scalingFactor = 10
        definition = {'index0': (0, 150),
                      'index1': (150, 300),
                      'index2': (300, 600),
                      'index3': (600, 1100),
                      'index4': (1100, 2300),
                      'index5': (2300, 3600),
                      'index6': (3600, 36000)}
        for key in dictRow.keys():
            if 'index' in key:
                scaledUsers = math.ceil(int(dictRow['Users']) / scalingFactor)
                ta = (float(dictRow[key]) / 100)
                temp = math.ceil(ta * scaledUsers)
                indexDict[temp] = definition[key]
        return indexDict

    with open(name, newline='') as csvfile, \
            open('file2.csv', mode='w', newline='') as out_file:
        fieldnames = ['Latitude', 'Longitude']
        writer = csv.DictWriter(out_file, fieldnames=fieldnames)
        writer.writeheader()
        reader = csv.DictReader(csvfile)
        for row in reader:
            indices = indexDictBuilder(row)
            minAngle = float(row['Azimuth']) - (float(row['HBeamWidth']) / 2)
            maxAngle = float(row['Azimuth']) + (float(row['HBeamWidth']) / 2)
            lat = float(row['Latitude'])
            lon = float(row['Longitude'])
            for keyNum, val in indices.items():
                for i in range(0, keyNum):
                    x, y = calcPointOnCircle(uniform(minAngle, maxAngle),
                                             uniform(val[0], val[1]))
                    newLat, newLon = metersToDecimalDegrees(lat, lon, x, y)
                    writer.writerow({'Latitude': newLat, 'Longitude': newLon})
                    print(newLat, newLon)
        print('all done')


if __name__ == '__main__':
    runner(FILENAME)
