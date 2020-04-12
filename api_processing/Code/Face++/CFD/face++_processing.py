from facepplib import FacePP
import os
import sys, traceback
import csv
import inspect

API_KEY = '<Insert-API-Key-here>'
API_SECRET_KEY = '<Insert-API-Secret-Key-here>'
CHICAGO_DB_PATH = "/Users/samuilstoychev/Desktop/researchproject/api_processing/Datasets/CFD/Images"
OUTPUT_FILE = 'face++_output.csv'
S3_BUCKET_PATH = 'https://<Insert-S3-bucket-name-here>.s3.eu-west-2.amazonaws.com/CFD/Images'

facepp = FacePP(api_key=API_KEY,
                api_secret=API_SECRET_KEY)

def collect_urls():
    """ Form a list of URLs corresponding to CFD image objects in AWS S3
        Note: this is needed since Face++'s API only accepts URLs and not local
        files. """
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
        images = list(map(lambda x: "/".join([S3_BUCKET_PATH, folder, x]), images))
        assert (len(images) > 0 and len(images) < 6)
        all_images += images

    # Make sure there are no duplicates
    assert len(all_images) == len(set(all_images))
    return all_images

def write_to_csv(data):
    """ Write information to a CSV file. """
    with open(OUTPUT_FILE, 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile, quoting=csv.QUOTE_MINIMAL)
        csvwriter.writerow(("File Name", "Target ID", "Image ID",
        "Race", "Gender", "Expression", "Gender", "Age", "Emotion", "Smiling"))
        for tuple in data:
            csvwriter.writerow(tuple)

def extract_file_info(file_url):
    """ Given a URL of an image, extract the gender, race and expression metadata. """
    # Only get the actual file name
    file_name = get_file_name(file_url).split(".")[0]
    file_name = file_name.split("-")
    race = file_name[1][0]
    gender = file_name[1][1]
    expression = file_name[4]
    target_id = file_name[1] + "-" + file_name[2]
    image_id = file_name[3]
    return (target_id, image_id, race, gender, expression)

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
    try:
        # Note: ethnicity not required because it was ommitted by Face++ (API returns empty string)
        response = facepp.image.get(image_url = image_url, return_attributes=['smiling', 'age', 'gender', 'emotion', 'beauty']).__dict__
        log_output(image_url, response)
        print("Logged successfully")
        return (get_file_name(image_url), ) + extract_file_info(image_url) + extract_response_info(response)
    except Exception as e:
        print("Failed to process image: " + image_url)
        print(e)
    finally:
        pass
    return (image_url, "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR", "ERROR")

if __name__ == "__main__":

    images = collect_urls()

    for image in images:
        try:
            process_image(image)
        except Exception as e:
            print("Problem with the image processing loop!")
            print(e)
        finally:
            pass
