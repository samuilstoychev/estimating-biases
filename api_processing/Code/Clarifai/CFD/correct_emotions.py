import csv

""" This script edits the Expression field which currently only shows H
instead the full HO or HC. Also fields are assigned unique names to
make the analysis process easier. """

def getEmotion(name):
    name = name[:-4]
    return name.split("-")[4]

rows = []

with open('clarifai_output.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        filename = row["File Name"]
        row["Expression"] = getEmotion(filename)
        rows.append(row)

with open('clarifai_output_CORRECTED.csv', 'w', newline='') as csvfile:

    fields = ['File Name', 'Target ID', 'Image ID', 'Race', 'Gender', 'Expression', 'Clarifai Race', 'Race Confidence', 'Clarifai Gender', 'Gender Confidence', 'Clarifai Age', 'Age Confidence']

    writer = csv.DictWriter(csvfile, fieldnames=fields)

    writer.writeheader()
    for row in rows:
        writer.writerow(row)
