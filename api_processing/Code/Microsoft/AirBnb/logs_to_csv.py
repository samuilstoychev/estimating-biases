import os
import sys, traceback
import csv
from datetime import datetime
import inspect

OUTPUT_FILE = 'microsoft_output.csv'
LOGS_LOCATION = "./microsoft_logs"

def write_to_csv(data):
    """ Write information to a CSV file. """
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(("Source", "Age", "Gender",
        "Smile", "Emotion"))
        for tuple in data:
            csvwriter.writerow(tuple)

def extract_response_info(response):

    src = response["source"]
    age = response["age"]
    gender = response["gender"]
    smile = response["smile"]
    emotions = response["emotion"]
    emotion = max(emotions, key=lambda x: emotions[x])
    return (src, age, gender, smile, emotion)

if __name__ == "__main__":

    data = []
    logs = os.listdir(LOGS_LOCATION)
    for log in sorted(logs):
        dump = open(LOGS_LOCATION + "/" + log, 'r').read()
        response = eval(dump)

        row = extract_response_info(response)
        data.append(row)

    try:
        write_to_csv(data)
    except:
        print("Problem with writing data to the CSV file. ")
