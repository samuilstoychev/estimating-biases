from facepplib import FacePP
import os
import csv
from datetime import datetime
import inspect

OUTPUT_FILE = 'face++_output.csv'
LOGS_LOCATION = "./face++_logs"

def write_to_csv(data):
    """ Write information to a CSV file. """
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(("File Name", "Target ID", "Gender",
        "Race", "Age", "Face++ Gender", "Face++ Age", "Face++ Emotion", "Face++ Smiling"))
        for tuple in data:
            csvwriter.writerow(tuple)

def extract_file_info(img_name):
    """ Given a URL of an image, extract the gender, race and expression metadata. """
    # Only get the actual file name
    print("Processing:", img_name)
    labels = image_name.split(".")[0]
    target_id, target_gender, target_race, target_age = labels.split("_")

    return (target_id, target_gender, target_race, target_age)

def extract_response_info(response):
    gender = response["_decoded_attrs"]["faces"][0]["attributes"]["gender"]["value"]

    age = response["_decoded_attrs"]["faces"][0]["attributes"]["age"]["value"]

    emotions = response["_decoded_attrs"]["faces"][0]["attributes"]["emotion"]
    emotion = max(emotions, key=lambda x: emotions[x])

    smile = response["_decoded_attrs"]["faces"][0]["attributes"]["smile"]["value"]
    smile = "True" if smile>50 else "False"
    return (gender, age, emotion, smile)

def get_file_name(path):
    return path.split("/")[-1]

def log_to_image_name(log_name):
    return log_name.split(" ")[2][:-3] + "jpeg"

if __name__ == "__main__":

    data = []
    logs = os.listdir(LOGS_LOCATION)
    for log in logs:
        dump = open(LOGS_LOCATION + "/" + log, 'r').read()
        dump = dump.replace("<facepplib.managers.ResourceManager object for Image resource>", "''")
        response = eval(dump)
        image_name = log_to_image_name(log)
        row = (image_name, ) + extract_file_info(image_name) + extract_response_info(response)
        data.append(row)

    try:
        write_to_csv(data)
    except:
        print("Problem with writing data to the CSV file. ")
