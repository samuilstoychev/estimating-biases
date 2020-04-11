import os
import shutil
import random

HK_PATH = "/Users/samuilstoychev/AirBnb/hk/"
CH_PATH = "/Users/samuilstoychev/AirBnb/chicago/kevin/"
DEST = "/Users/samuilstoychev/Desktop/researchproject/api_processing/Datasets/AirBnb/random_sample"

hk_pictures = os.listdir(HK_PATH)
ch_pictures = os.listdir(CH_PATH)

hk_random_500 = random.sample(range(1, len(hk_pictures)),500)
ch_random_500 = random.sample(range(1, len(ch_pictures)),500)

count = 0

for index in hk_random_500:
    file_name = hk_pictures[index]
    if file_name.split(".")[-1] == "jpg":
        file_path = HK_PATH + file_name
        shutil.copy(file_path, DEST)
        count += 1
for index in ch_random_500:
    file_name = ch_pictures[index]
    if file_name.split(".")[-1] == "jpg":
        file_path = CH_PATH + file_name
        shutil.copy(file_path, DEST)
        count += 1

print("Sampled " + str(count) + " random images. ")
