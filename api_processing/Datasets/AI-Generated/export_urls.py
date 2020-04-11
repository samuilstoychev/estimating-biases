import os
import json
import csv
faces = os.listdir("./faces")

rows = []

for file in faces:
    face_tags = file.split(".")[0].split("_")

    gender = face_tags[0]
    ethnicity = face_tags[1]
    age = face_tags[2]

    with open("./faces/" + file) as json_file:
        python_dict = json.load(json_file)
        for obj in python_dict["faces"]:
            id = obj["id"]
            url = obj["urls"][4]['512']
            rows.append((id, gender, ethnicity, age, url))

# Open file and write the information
with open("faces_data.csv", "w", newline='') as output_file:
    csvwriter = csv.writer(output_file, quoting=csv.QUOTE_MINIMAL)
    csvwriter.writerow(("ID", "Gender", "Ethnicity", "Age", "URL"))
    for row in rows:
        csvwriter.writerow(row)
