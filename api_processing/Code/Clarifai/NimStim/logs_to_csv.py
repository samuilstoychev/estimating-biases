import os
import sys, traceback
import csv
from datetime import datetime
import inspect

OUTPUT_FILE = 'clarifai_output.csv'
LOGS_LOCATION = "./clarifai_logs"

def write_to_csv(data):
    """ Write information to a CSV file. """
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(("File Name", "Target ID", "Gender", "Emotion", "Mouth",
        'Clarifai Race', 'Race Confidence', 'Clarifai Gender', 'Gender Confidence',
        'Clarifai Age', 'Age Confidence'))
        for tuple in data:
            csvwriter.writerow(tuple)

def extract_file_info(img_name):
    """ Given a URL of an image, extract the gender, race and expression metadata. """
    # Only get the actual file name
    print("Processing:", img_name)
    labels = image_name.split(".")[0]
    identifier, target_emotion, target_mouth = labels.split("_")
    target_id, target_gender = identifier[:-1], identifier[-1]

    return (target_id, target_gender, target_emotion, target_mouth)

def extract_response_info(response):

    gender = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["gender_appearance"]["concepts"][0]["name"]
    gender_confidence = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["gender_appearance"]["concepts"][0]["value"]

    age = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["age_appearance"]["concepts"][0]["name"]
    age_confidence = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["age_appearance"]["concepts"][0]["value"]

    race = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["multicultural_appearance"]["concepts"][0]["name"]
    race_confidence = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["multicultural_appearance"]["concepts"][0]["value"]

    return (race, race_confidence, gender, gender_confidence, age, age_confidence)

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
        row = (image_name + '.jpeg', ) + extract_file_info(image_name) + extract_response_info(response)
        data.append(row)

    try:
        write_to_csv(data)
    except:
        print("Problem with writing data to the CSV file. ")
