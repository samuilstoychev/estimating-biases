from facepplib import FacePP
import os
import csv
from datetime import datetime
import inspect
import boto3

API_KEY = '<Insert-API-Key-here>'
API_SECRET_KEY = '<Insert-API-Secret-Key-here>'
BUCKET_NAME = '<Insert-S3-bucket-name-here>'
S3_URL = "https://<Insert-S3-bucket-name-here>.s3.eu-west-2.amazonaws.com/"

facepp = FacePP(api_key=API_KEY,
                api_secret=API_SECRET_KEY)

def collect_urls():
    image_urls = []
    s3 = boto3.resource('s3')
    nimstim_bucket = s3.Bucket(BUCKET_NAME)
    for file in nimstim_bucket.objects.all():
        image_urls.append(S3_URL + file.key)
    return image_urls

def log_output(image_url, content):
    content = str(content)
    name = get_file_name(image_url).split(".")[0]
    print("The name is " + name)
    name = "face++_logs/[{}] {}.txt".format(datetime.now(), name)
    print(name)
    with open(name, 'w') as f:
        f.write(content)
        f.close()

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

def process_image(image_url):
    print("Received " + image_url)
        # Note: ethnicity not required because it was ommitted by Face++ (API returns empty string)
    response = facepp.image.get(image_url = image_url, return_attributes=['smiling', 'age', 'gender', 'emotion', 'beauty']).__dict__
    log_output(image_url, response)
    print("Logged successfully")

if __name__ == "__main__":

    images = collect_urls()
    successful = 0
    failed = []

    for image in images:
        try:
            process_image(image)
            successful += 1
        except Exception as e:
            print("[ERROR]: Failed to process", image)
            print(e)
            failed.append(image)
        finally:
            print("Successful:", successful, "Failed:", len(failed))
    print("Failed to process: ")
    print(failed)
