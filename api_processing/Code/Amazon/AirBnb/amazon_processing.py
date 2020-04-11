import boto3
import json
import os
from datetime import datetime

BUCKET_NAME = "airbnb-sample"
S3_BUCKET_PATH = "https://airbnb-sample.s3.eu-west-2.amazonaws.com/"
amazon_rekognition = boto3.client('rekognition', region_name="eu-west-2")

def collect_urls():
    image_urls = []
    s3 = boto3.resource('s3')
    nimstim_bucket = s3.Bucket(BUCKET_NAME)
    for file in nimstim_bucket.objects.all():
        image_urls.append(file.key)
    return image_urls

def emotions_to_dict(emotions):
    emotions_dict = dict()
    for emotion in emotions:
        emotions_dict[emotion["Type"]] = emotion["Confidence"]
    return emotions_dict

def process_image(image):
    response = amazon_rekognition.detect_faces(
        Image = {'S3Object': {'Bucket': BUCKET_NAME, 'Name': image}},
        Attributes=['ALL']
    )
    if len(response) == 0:
        raise Exception("No face detected for " + image)

    info = dict()
    response = response['FaceDetails'][0]
    info["age_low"] = response['AgeRange']['Low']
    info["age_high"] = response['AgeRange']['High']
    info["smile_value"] = response["Smile"]["Value"]
    info["smile_confidence"] = response["Smile"]["Confidence"]
    info["gender_value"] = response["Gender"]["Value"]
    info["gender_confidence"] = response["Gender"]["Confidence"]
    info["emotions"] = emotions_to_dict(response["Emotions"])

    return info

def log_output(image_name, content):
    content = str(content)
    name = os.path.basename(image_name)
    print("Received: " + name)
    name = "amazon_logs/[{}] {}.txt".format(datetime.now(), name)
    print("Logging to: " + name)
    with open(name, 'w') as f:
        f.write(content)
        f.close()

if __name__ == "__main__":
    images = collect_urls()
    print("Processing: ", images)

    successful = 0
    failed = []

    for image in images:
        try:
            print("Processing: " + image)
            response = process_image(image)
            print("Received: " + str(response))
            log_output(image, response)
            successful += 1
        except Exception as e:
            print("[ERROR]: Failed to process " + image)
            print(e)
            failed.append(image)
        finally:
            print("Successful:", successful, "Failed:", len(failed))

    print("Failed images: ", failed)
