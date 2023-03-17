import json
import os
from trdg.generators import (
    GeneratorFromDict,
    GeneratorFromRandom,
    GeneratorFromStrings,
    GeneratorFromWikipedia,
)


class MyTextGenerator:
    def __init__(self, input_words_file_path: str, out_dir_path: str, nb_of_words: int,
                 from_dict: bool = False):
        output_ground_truth_file = f'{out_dir_path}/gt/gt.json'

        counter = 0

        with open(file=input_words_file_path, mode='r', encoding='utf-8') as f:
            words_list = []
            lines = f.readlines()
            for line in lines:
                word = line.replace('\n', '')
                words_list.append(word)

        # The generators use the same arguments as the CLI, only as parameters
        generator = GeneratorFromStrings(
            strings=words_list,
            language="latin",  # ['latin, '7led']
            count=nb_of_words,
            blur=2,
            distorsion_type=3,
            random_blur=True,
            random_skew=True,
            skewing_angle=15,
            text_color='#000000,#888888',
            fit=True,
            size=64,
            background_type=2
        )
        ground_truth = {}
        for img, lbl in generator:
            # Do something with the pillow images here.
            image_name: str = lbl
            image_name = image_name.replace("/", "")
            image_file_path = os.path.join(out_dir_path, f"{image_name}_{counter}.jpg")
            ground_truth[str(image_file_path)] = lbl

            img.save(image_file_path)
            img.close()
            counter += 1

        # Serializing json
        json_object = json.dumps(ground_truth, indent=4)

        # Writing to sample.json
        with open(file=output_ground_truth_file, mode='w+') as file:
            file.write(json_object)


if __name__ == '__main__':
    current_directory_o = os.getcwd()
    words_file_path_o = f'{current_directory_o}/trdg/dicts/gym.txt'
    output_directory_o = f'{current_directory_o}/out'

    bb = MyTextGenerator(input_words_file_path=words_file_path_o,
                         out_dir_path=output_directory_o,
                         nb_of_words=3000)
