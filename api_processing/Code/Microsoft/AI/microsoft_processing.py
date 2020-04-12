import csv
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials
from datetime import datetime

KEY = "<Insert-Key-here>"
ENDPOINT = "https://researchprojectfaceapi.cognitiveservices.azure.com/"
CSV_LOCATION = '../../../Datasets/AI-Generated/faces_data.csv'

def get_input_data():

    with open(CSV_LOCATION, newline='') as csvfile:
        csvreader = csv.reader(csvfile, delimiter=',')
        return list(csvreader)[1:]

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

def log_output(image_url, id, gender, race, age, content):

    content["original_id"] = id
    content["original_gender"] = gender
    content["original_race"] = race
    content["original_age"] = age

    content = str(content)
    print("Received: " + id)
    name = "microsoft_logs/[{}] {}.txt".format(datetime.now(), id)
    print("Logging to: " + name)
    with open(name, 'w') as f:
        f.write(content)
        f.close()

if __name__ == "__main__":
    input_data = get_input_data()
    print("Processing ", len(input_data), " inputs.")
    successful = 0
    failed = []

    # Create a FaceClient object
    face_client = FaceClient(ENDPOINT, CognitiveServicesCredentials(KEY))
    face_attributes=["age", "gender", "smile", "emotion"]

    for input in input_data:
        print("Processed successfully: " + str(successful) + ", failed: " + str(len(failed)))
        single_face_image_url = input[4]
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
            log_output(single_face_image_url, input[0], input[1], input[2], input[3], response)
            successful += 1
        except Exception as e:
            print("[ERROR] Failed to process " + single_face_image_url)
            print(e)
            failed.append(single_face_image_url)

    print("Processed successfully: " + str(successful) + ", failed: " + str(len(failed)))
    print("Failed entries below: ")
    print(failed)
    print("Processing complete. ")
