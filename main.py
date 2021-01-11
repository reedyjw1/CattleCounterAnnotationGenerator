import csv
import json
import requests
from tqdm import tqdm

original_csv = 'hive.csv'
new_csv = 'allAnnotations.csv'
csvDelimiter = ','


def getPointsConverted(row, size, axisType):

    jsonObjects = json.loads(row)
    arrayOfValues = []

    for jsonObject in jsonObjects:

        xMin = jsonObject["p1"]["x"]
        yMin = jsonObject["p1"]["y"]
        xMax = jsonObject["p2"]["x"]
        yMax = jsonObject["p2"]["y"]

        if axisType == 'xmin':
            arrayOfValues.append(xMin * float(size))

        elif axisType == 'ymin':
            arrayOfValues.append(yMin * float(size))

        elif axisType == 'xmax':
            arrayOfValues.append(xMax * float(size))

        elif axisType == 'ymax':
            arrayOfValues.append(yMax * float(size))

    return arrayOfValues



def convert_annotations(csvfilename, delimiterused, newfilename):
    originalrows = []

    with open(csvfilename, newline='') as file:
        reader = csv.reader(file, delimiter=delimiterused, quotechar='"')
        next(reader)
        for row in reader:
            originalrows.append(row)

    with open(newfilename, 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(["filename", "width", "height", "class", "xmin", "ymin", "xmax", "ymax"])
        for row in originalrows:
            fileName = row[10] + '.jpg'
            width = row[20]
            height = row[19]
            className = "cattle"

            xmin = getPointsConverted(row[24], width, 'xmin')
            ymin = getPointsConverted(row[24], height, 'ymin')
            xmax = getPointsConverted(row[24], width, 'xmax')
            ymax = getPointsConverted(row[24], height, 'ymax')

            writer.writerow([fileName, width, height, className, xmin, ymin, xmax, ymax])


def downloadImages(csvfilename, delimiterused):
    with open(csvfilename, newline='') as file:
        reader = csv.reader(file, delimiter=delimiterused, quotechar='"')
        next(reader)

        for row in tqdm(reader):
            url = row[7]
            filename = row[10]
            saveDir = "images/" + filename + ".jpg"
            myFile = requests.get(url)
            open(saveDir, 'wb').write(myFile.content)


# convert_annotations(original_csv, csvDelimiter, new_csv)

downloadImages(original_csv, csvDelimiter)
