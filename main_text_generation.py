import json
import os
import shutil

from trdg.generators import (
    GeneratorFromDict,
    GeneratorFromStrings
)


class MyTextGenerator:

    def __init__(self,
                 input_words_file_path: str,
                 out_dir_path: str,
                 nb_of_sentences: int,
                 language: str,  # ['keras', 'numbers']
                 image_dir: str,  # path to the folder of background images
                 from_dict: bool = False):
        """
        Generates synthetic images and a grond truth file containing a JSON dictionary mapping the path of the image
        to its label (the sentence)

        @param input_words_file_path: the words using which to compose sentences
        @param out_dir_path: where to save the images and the ground truth file
        @param nb_of_sentences: the number of sentences to generate
        @param language: the language (dictionary) to use for generation of sentences
        @param image_dir: the directory where background images are stored
        @param from_dict: specifies whether to generate sentences from the dict corresponding to the language
            or generate words using the input_words_file_path
        """
        # Delete the out directory if it exists
        if os.path.isdir(out_dir_path):
            shutil.rmtree(out_dir_path)

        os.mkdir(out_dir_path)
        os.mkdir(f'{out_dir_path}/gt')

        output_ground_truth_file = f'{out_dir_path}/gt/gt.json'

        counter = 0

        with open(file=input_words_file_path, mode='r', encoding='utf-8') as f:
            words_list = []
            lines = f.readlines()
            for line in lines:
                word = line.replace('\n', '')
                words_list.append(word)

        # The generators use the same arguments as the CLI, only as parameters
        if from_dict:
            print('Generating from sentences...')
            generator = GeneratorFromDict(
                length=3,
                allow_variable=True,
                language=language,  # ['keras', '7led']
                count=nb_of_sentences,
                blur=2,
                distorsion_type=3,
                random_blur=True,
                random_skew=True,
                skewing_angle=15,
                text_color='#000000,#888888',
                fit=True,
                size=64,
                # background_type=2
                image_dir=image_dir
            )
        else:
            print('Generating from words...')

            generator = GeneratorFromStrings(
                strings=words_list,
                language=language,  # ['keras', '7led']
                count=nb_of_sentences,
                blur=2,
                distorsion_type=3,
                random_blur=True,
                random_skew=True,
                skewing_angle=15,
                text_color='#000000,#888888',
                fit=True,
                size=64,
                # background_type=2
                image_dir=image_dir
            )
        ground_truth = {}
        for img, lbl in generator:
            # Do something with the pillow images here.
            image_name: str = lbl
            image_name = image_name.replace("/", "")
            identifier = str(counter)

            identifier = identifier.zfill(5)

            image_file_path = os.path.join(out_dir_path, f"{identifier}_{image_name}.jpg")

            try:
                img.save(image_file_path)
                img.close()
                ground_truth[str(image_file_path)] = lbl
                counter += 1

            except AttributeError as e:
                print(f'Skipped saving image {image_file_path} with label {lbl}: {e}')

        # Serializing json
        json_object = json.dumps(ground_truth, indent=4)

        # Writing to sample.json
        with open(file=output_ground_truth_file, mode='w+') as file:
            file.write(json_object)


if __name__ == '__main__':
    current_directory_o = os.getcwd()
    words_file_path_o = f'{current_directory_o}/trdg/dicts/keras.txt'
    output_directory_o = f'{current_directory_o}/out'
    image_dir_o = f'{current_directory_o}/trdg/images/dark'

    bb = MyTextGenerator(input_words_file_path=words_file_path_o,
                         out_dir_path=output_directory_o,
                         nb_of_sentences=10000,
                         language='keras',
                         image_dir=image_dir_o,
                         from_dict=False)
