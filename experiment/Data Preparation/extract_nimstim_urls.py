import boto3
import csv

BUCKET_NAME = "nimstim-dataset-jpeg"
PATH = "https://nimstim-dataset-jpeg.s3.eu-west-2.amazonaws.com/"
OUTPUT_FILE = "nimstim_urls.csv"

def collect_urls():
    image_urls = []
    s3 = boto3.resource('s3')
    nimstim_bucket = s3.Bucket(BUCKET_NAME)
    for file in nimstim_bucket.objects.all():
        image_urls.append(file.key)
    return image_urls

def write_to_csv(data):
    """ Write information to a CSV file. """
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(("URL",))
        for row in data:
            csvwriter.writerow((row,))

def extract_neutral(images):
    seen = []
    result = []
    for image in images:
        emotion = image.split("_")[1][:2]
        subject = image.split("_")[0]
        if subject in seen:
            continue
        if emotion in ["ne", "NE"]:
            seen.append(subject)
            result.append(image)
    return result

urls = collect_urls()
neutral_urls = [(PATH + x) for x in extract_neutral(urls)]

write_to_csv(neutral_urls)
