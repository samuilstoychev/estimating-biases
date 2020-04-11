import os
import sys, traceback
import csv
from datetime import datetime
import inspect

OUTPUT_FILE = 'amazon_output.csv'
LOGS_LOCATION = "./amazon_logs"

def write_to_csv(data):
    """ Write information to a CSV file. """
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(("File Name", "age_low", "age_high",
        "smile_value", "smile_confidence", "gender_value",
        "gender_confidence", "top_emotion"))
        for tuple in data:
            csvwriter.writerow(tuple)

def extract_response_info(response):

    emotions = response["emotions"]
    top_emotion = max(emotions, key=lambda x: emotions[x])

    return (response["age_low"],
        response["age_high"],
        response["smile_value"],
        response["smile_confidence"],
        response["gender_value"],
        response["gender_confidence"],
        top_emotion)

def get_file_name(path):
    return path.split("/")[-1]

def log_to_image_name(log_name):
    return log_name.split(" ")[2][:-4]

if __name__ == "__main__":

    data = []
    logs = os.listdir(LOGS_LOCATION)
    for log in sorted(logs):
        dump = open(LOGS_LOCATION + "/" + log, 'r').read()
        response = eval(dump)

        image_name = log_to_image_name(log)
        row = (image_name, ) +  extract_response_info(response)
        data.append(row)

    try:
        write_to_csv(data)
    except:
        print("Problem with writing data to the CSV file. ")
