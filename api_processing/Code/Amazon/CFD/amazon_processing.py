import boto3
import json
import os
from datetime import datetime

CHICAGO_DB_PATH = "/Users/samuilstoychev/Desktop/researchproject/api_processing/Datasets/CFD/Images"
BUCKET_NAME = "<Insert-S3-bucket-name-here>"
CFD_S3_PATH = "CFD/Images"
amazon_rekognition = boto3.client('rekognition', region_name="eu-west-2")

def collect_images():
    """ Return the S3 paths of the images in CFD. """
    # Get the contents of the current directory
    folders = os.listdir(CHICAGO_DB_PATH)
    # Filter only folders
    folders = list(filter(lambda x: os.path.isdir("/".join([CHICAGO_DB_PATH, x])), folders))
    # Sanity check
    assert len(folders) == 597
    all_images = []
    for folder in folders:
        images = os.listdir("/".join([CHICAGO_DB_PATH, folder]))
        images = filter(lambda x: x[-3:] == "jpg", images)
        images = list(map(lambda x: "/".join([ CFD_S3_PATH, folder, x]), images))
        assert (len(images) > 0 and len(images) < 6)
        all_images += images

    # Make sure there are no duplicates
    assert len(all_images) == len(set(all_images))
    return all_images

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
    images = collect_images()
    print(images)
    counter = 0
    for image in images:
        try:
            response = process_image(image)
            print("Processing: " + image)
            print("Received: " + str(response))
            log_output(image, response)
            counter += 1
            print("Processed " + str(counter) + "/1207 images")
        except Exception as e:
            print("[ERROR]: Faile to process " + image)
    print("Processed " + str(counter) + " images.")
