## Objectives: count unique faces, get a list of unique URLs

import os
import json
sum = 0
faces = os.listdir("./faces")

genders = {}
ethnicities = {}
ages = {}

def update_counts(gender, ethnicity, age, n):
    if gender in genders:
        genders[gender] += n
    else:
        genders[gender] = n
    if ethnicity in ethnicities:
        ethnicities[ethnicity] += n
    else:
        ethnicities[ethnicity] = n
    if age in ages:
        ages[age] += n
    else:
        ages[age] = n


for face in faces:
    face_tags = face.split(".")[0]
    face_tags = face_tags.split("_")
    gender = face_tags[0]
    ethnicity = face_tags[1]
    age = face_tags[2]

    with open("./faces/" + face) as json_file:
        python_dict = json.load(json_file)
        n = len(python_dict["faces"])
        update_counts(gender, ethnicity, age, n)
        sum += len(python_dict["faces"])

print(genders)
print(ethnicities)
print(ages)

print("="*20)
print("SUM:", sum)
