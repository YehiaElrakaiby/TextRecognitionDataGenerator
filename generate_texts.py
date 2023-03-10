import os

from trdg.generators import (
    GeneratorFromDict,
    GeneratorFromRandom,
    GeneratorFromStrings,
    GeneratorFromWikipedia,
)
current_directory = os.getcwd()
words_file_path = f'{current_directory}/trdg/dicts/gym.txt'
output_directory = f'{current_directory}/out'
output_ground_truth_file = f'{current_directory}/out_ground_truth/out_ground_truth.txt'

counter = 0

with open(file=words_file_path ,mode='r', encoding='utf-8') as f:
    words_list = []
    lines = f.readlines()
    for line in lines:
        word = line.replace('\n', '')
        words_list.append(word)

# The generators use the same arguments as the CLI, only as parameters
generator = GeneratorFromStrings(
    strings=words_list,
    count=3000,
    blur=2,
    random_blur=True,
    random_skew=True,
    skewing_angle=15,
    text_color='#000000,#888888',
    fit=True,
    size=64,
    background_type=2
)
with open(file=output_ground_truth_file, mode='w+') as file:
    for img, lbl in generator:
        # Do something with the pillow images here.
        image_name: str = lbl
        image_name = image_name.replace("/", "")
        image_file_path = os.path.join(output_directory, f"{image_name}_{counter}.jpg")
        file.write(f'{image_file_path} <--> {lbl}\n')

        img.save(image_file_path)
        img.close()
        counter += 1
