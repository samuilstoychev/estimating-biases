from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import os
import csv
from datetime import datetime
import boto3

API_KEY = '0a87ea2453a04d27be8ef263c795e147'
BUCKET_NAME = 'nimstim-dataset-jpeg'
S3_URL = "https://nimstim-dataset-jpeg.s3.eu-west-2.amazonaws.com/"
app = ClarifaiApp(api_key=API_KEY)

def collect_urls():
    image_urls = []
    s3 = boto3.resource('s3')
    nimstim_bucket = s3.Bucket(BUCKET_NAME)
    for file in nimstim_bucket.objects.all():
        image_urls.append(S3_URL + file.key)
    return image_urls

def log_output(image_url, content):
    content = str(content)
    name = image_url.split("/")[-1]
    name = name.split(".")[0]
    name = "clarifai_logs/[{}] {}.txt".format(datetime.now(), name)
    with open(name, 'w') as f:
        f.write(content)
        f.close()

def extract_response_info(response):
    gender = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["gender_appearance"]["concepts"][0]["name"]
    gender_confidence = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["gender_appearance"]["concepts"][0]["value"]

    age = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["age_appearance"]["concepts"][0]["name"]
    age_confidence = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["age_appearance"]["concepts"][0]["value"]

    race = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["multicultural_appearance"]["concepts"][0]["name"]
    race_confidence = response["outputs"][0]["data"]["regions"][0]["data"]["face"]["multicultural_appearance"]["concepts"][0]["value"]

    return (race, race_confidence, gender, gender_confidence, age, age_confidence)

def process_image(image_url):
    model = app.models.get('demographics')
    response = model.predict_by_url(url=image_url)
    log_output(image_url, response)

if __name__ == "__main__":
    images = collect_urls()

    successful = 0
    failed = []

    for image in images:
        try:
            process_image(image)
            successful += 1
        except Exception as e:
            print("Problem with the image processing loop!")
            print(e)
            failed.append(image)
        finally:
            print("Successful:", successful, "Failed:", len(failed))
