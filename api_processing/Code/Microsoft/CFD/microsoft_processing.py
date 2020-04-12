import os
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from datetime import datetime

KEY = "<Insert-Key-here>"
ENDPOINT = "https://researchprojectfaceapi.cognitiveservices.azure.com/"
CHICAGO_DB_PATH = "/Users/samuilstoychev/Desktop/researchproject/api_processing/Datasets/CFD/Images"
S3_BUCKET_PATH = 'https://<Insert-S3-bucket-name-here>.s3.eu-west-2.amazonaws.com/CFD/Images'

def collect_urls():
    """ Form a list of URLs corresponding to CFD image objects in AWS S3 """
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

    # Create a FaceClient object
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    face_attributes=["age", "gender", "smile", "emotion"]

    for single_face_image_url in urls:

        # Process the image through the Face API
        detected_faces = face_client.face.detect_with_url(url=single_face_image_url, return_face_attributes=face_attributes)
        if not detected_faces:
            print("[ERROR]: No face detected for: " + single_face_image_url)

        # Display the detected face ID in the first single-face image.
        # Face IDs are used for comparison to faces (their IDs) detected in other images.

        face = detected_faces[0]
        response = process_face(face, single_face_image_url)
        print("The response for " + single_face_image_url + " is: ")
        print(response)
        log_output(single_face_image_url, response)

    print("Processing complete. ")
