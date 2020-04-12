import os
import csv
from datetime import datetime
import inspect

OUTPUT_FILE = 'microsoft_output.csv'
LOGS_LOCATION = "./microsoft_logs"

def write_to_csv(data):
    """ Write information to a CSV file. """
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(("ID", "Source", "Gender",
        "Ethinicty", "Age", "Microsoft Gender", "Microsoft Age", "Microsoft Emotion", "Microsoft Smiling"))
        for tuple in data:
            csvwriter.writerow(tuple)

def extract_response_info(response):
    id = response["original_id"]
    source = response["source"]
    gender = response["original_gender"]
    ethnicity = response["original_race"]
    age = response["original_age"]
    ms_gender = response["gender"]
    ms_age = response["age"]
    emotions = response["emotion"]
    ms_emotion = max(emotions, key=lambda x: emotions[x])
    ms_smile = response["smile"]

    return (id, source, gender, ethnicity, age, ms_gender, ms_age, ms_emotion, ms_smile)

def get_file_name(path):
    return path.split("/")[-1]

def log_to_id(log_name):
    return log_name.split(" ")[2][:-4]

if __name__ == "__main__":

    data = []
    logs = os.listdir(LOGS_LOCATION)
    for log in sorted(logs):
        dump = open(LOGS_LOCATION + "/" + log, 'r').read()
        response = eval(dump)

        id = log_to_id(log)
        row = extract_response_info(response)
        data.append(row)

    try:
        write_to_csv(data)
    except:
        print("Problem with writing data to the CSV file. ")
