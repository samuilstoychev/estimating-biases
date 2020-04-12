from clarifai.rest import ClarifaiApp
from clarifai.rest import Image as ClImage
import os
import csv
from datetime import datetime

CHICAGO_DB_PATH = "/Users/samuilstoychev/Desktop/researchproject/api_processing/Datasets/CFD/Images"
API_KEY = '<Insert-API-Key-here>'
OUTPUT_FILE = 'clarifai_output.csv'
app = ClarifaiApp(api_key=API_KEY)

def collect_images():
    """ Collect images from the Chicago Database and extract in a list. """
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
        images = list(map(lambda x: "/".join([CHICAGO_DB_PATH, folder, x]), images))
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
        "Race", "Gender", "Expression", "Race", "Race Confidence",
         "Gender", "Gender Confidence", "Age", "Age Confidence"))
        for tuple in data:
            csvwriter.writerow(tuple)

def extract_file_info(file_path):

    """ Given a file path of an image, extract the gender, race and expression metadata. """
    # Only get the actual file name
    file_name = get_file_name(file_path)
    race = file_name[4]
    gender = file_name[5]
    expression = file_name[15]
    target_id = race + gender + "-" + file_name[7:10]
    image_id = file_name[11:14]
    return (target_id, image_id, race, gender, expression)

def log_output(image_path, content):
    content = str(content)
    name = get_file_name(image_path).split(".")[0]
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

def get_file_name(path):
    return path.split("/")[-1]

def process_image(image_path):
    try:
        model = app.models.get('demographics')
        response = model.predict_by_filename(image_path)
        log_output(image_path, response)
        return (get_file_name(image_path), ) + extract_file_info(image_path) + extract_response_info(response)
    except Exception as e:
        print("Failed to process image: " + image_path)
        print(e)
    finally:
        pass

if __name__ == "__main__":
    images = collect_images()

    data = []
    for image in images:
        try:
            output = process_image(image)
            data.append(output)
        except Exception as e:
            print("Problem with the image processing loop!")
            print(e)
        finally:
            pass
    try:
        write_to_csv(data)
    except Exception as e:
        print("Problem with writing data to the CSV file!")
        print(e)
    finally:
        pass
