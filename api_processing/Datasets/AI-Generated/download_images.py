import csv
import urllib.request

CSV_LOCATION = './faces_data.csv'

def get_input_data():

    with open(CSV_LOCATION, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        return list(csvreader)[1:]

inputs = get_input_data()
ids = [x[0] for x in inputs]

for input in inputs:
    id = input[0]
    gender = input[1]
    race = input[2]
    age = input[3]
    url = input[4]
    output_name = "_".join([id,gender,race,age]) + ".jpeg"
    urllib.request.urlretrieve(url, "./images/" + output_name)
