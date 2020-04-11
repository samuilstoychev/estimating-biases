from PIL import Image
import os

NIMSTIM_PATH = '/Users/samuilstoychev/Desktop/researchproject/api_processing/Datasets/NimStim/Crop-White Background/'

def create_jpg(name):
    img = Image.open(NIMSTIM_PATH + name)
    img = img.convert('RGB')
    name = name.split(".")[0] + ".jpeg"
    img.save("./converted/" + name, "jpeg")

for filename in os.listdir(NIMSTIM_PATH):
    # Filter images (the folder might contain OS files such as .DS_Store)
    extension = filename.split(".")[-1]

    if extension == "BMP":
        print(1)
        create_jpg(filename)
