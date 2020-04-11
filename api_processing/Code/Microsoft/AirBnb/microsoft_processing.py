import asyncio
import io
import glob
import os
import sys
import time
import uuid
import boto3
import requests
from urllib.parse import urlparse
from io import BytesIO
from PIL import Image, ImageDraw
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from azure.cognitiveservices.vision.face.models import TrainingStatusType, Person, SnapshotObjectType, OperationStatusType
from datetime import datetime

KEY = "7f277b3127a447dfb03836f9b6934487"
ENDPOINT = "https://researchprojectfaceapi.cognitiveservices.azure.com/"
S3_BUCKET_PATH = "https://airbnb-sample.s3.eu-west-2.amazonaws.com/"

def collect_urls():
    image_urls = []
    s3 = boto3.resource('s3')
    nimstim_bucket = s3.Bucket('airbnb-sample')
    for file in nimstim_bucket.objects.all():
        image_urls.append(S3_BUCKET_PATH + file.key)
    return image_urls

def process_face(face, image_url):
    information = dict()
    emotion = dict()

    information["source"] = image_url

    information["face_id"] = face.face_id
    information["age"] = face.face_attributes.age
    information["gender"] = face.face_attributes.gender._value_
    information["smile"] = face.face_attributes.smile

    emotion["anger"] = face.face_attributes.emotion.anger
    emotion["contempt"] = face.face_attributes.emotion.contempt
    emotion["disgust"] = face.face_attributes.emotion.disgust
    emotion["fear"] = face.face_attributes.emotion.fear
    emotion["happiness"] = face.face_attributes.emotion.happiness
    emotion["neutral"] = face.face_attributes.emotion.neutral
    emotion["sadness"] = face.face_attributes.emotion.sadness
    emotion["surprise"] = face.face_attributes.emotion.surprise

    information["emotion"] = emotion

    return information

def log_output(image_url, content):
    content = str(content)
    name = os.path.basename(image_url)
    print("Received: " + name)
    name = "microsoft_logs/[{}] {}.txt".format(datetime.now(), name)
    print("Logging to: " + name)
    with open(name, 'w') as f:
        f.write(content)
        f.close()

if __name__ == "__main__":
    urls = collect_urls()
    print("Processing " + str(len(urls)) + " urls.")
    successful = 0
    failed = []

    # Create a FaceClient object
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    face_attributes=["age", "gender", "smile", "emotion"]

    for single_face_image_url in urls:
        print("Processed successfully: " + str(successful) + ", failed: " + str(len(failed)))
        try:
            # Process the image through the Face API
            detected_faces = face_client.face.detect_with_url(url=single_face_image_url, return_face_attributes=face_attributes)
            if not detected_faces:
                print("[ERROR]: No face detected for: " + single_face_image_url)
                failed.append(single_face_image_url)
                continue

            # Display the detected face ID in the first single-face image.
            # Face IDs are used for comparison to faces (their IDs) detected in other images.
            face = detected_faces[0]
            response = process_face(face, single_face_image_url)
            print("The response for " + single_face_image_url + " is: ")
            print(response)
            log_output(single_face_image_url, response)
            successful += 1
        except Exception as e:
            print("[ERROR] Failed to process " + single_face_image_url)
            print(e)
            failed.append(single_face_image_url)

    print("Failed entries below: ")
    print(failed)
    print("Processing complete. ")
