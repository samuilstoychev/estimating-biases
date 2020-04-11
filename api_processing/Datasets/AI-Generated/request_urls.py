import requests
import json
from flask import jsonify
import itertools

API_KEY = 'API-Key KyjeDwiDLw0nO1FTbOhV0w'
genders = ["male", "female"]
ethnicities = ["white", "latino", "asian", "black"]
ages = ["infant", "child", "young-adult", "adult", "elderly"]

def generate_uri(gender, ethnicity, age):
    return "https://api.generated.photos/api/v1/faces?per_page=100&gender={}&ethnicity={}&age={}".format(gender, ethnicity, age)

if __name__ == "__main__":

    for x in itertools.product(genders, ethnicities, ages):
        gender = x[0]
        ethnicity = x[1]
        age = x[2]

        uri = generate_uri(gender, ethnicity, age)
        response = requests.get(uri, headers={'Authorization': API_KEY})
        output_file_name = "{}_{}_{}.json".format(gender, ethnicity, age)

        with open(output_file_name, 'w') as output_file:
            response_json = json.loads(response.text)
            json.dump(response_json, output_file)
