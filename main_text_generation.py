import json
import os
import shutil

from trdg.generators import (
    GeneratorFromDict,
    GeneratorFromStrings
)


class MyTextGenerator:

    def __init__(self,
                 dict_file_name: str,
                 out_folder_name: str,
                 nb_of_sentences: int,
                 sentence_length: int,
                 fonts_folder_name: str,  # ['gym_text', 'gym_times', 'gym_numbers']
                 background_folder_name: str
                 ):
        """
        Generates synthetic images and a ground truth file containing a JSON dictionary mapping the path of the image
        to its label (the sentence)

        @param dict_file_name: the words to use (from_dict=False) or using which to compose sentences (from_dict=True)
        @param out_folder_name: where to save the images and the ground truth file
        @param nb_of_sentences: the number of sentences to generate
        @param fonts_folder_name: the language (dictionary words) to use for generation of sentences
        @param background_folder_name: the directory where background images are stored
        """
        current_directory = os.getcwd()
        dict_file_path = f'{current_directory}/trdg/dicts/{dict_file_name}'
        output_folder_path = f'{current_directory}/out/{out_folder_name}'
        background_folder_path = f'{current_directory}/trdg/images/{background_folder_name}'
        fonts_folder_path = f'{current_directory}/trdg/fonts/{fonts_folder_name}'

        # Delete the out directory if it exists
        if os.path.isdir(output_folder_path):
            shutil.rmtree(output_folder_path)

        os.mkdir(output_folder_path)
        os.mkdir(f'{output_folder_path}/gt')

        output_ground_truth_file = f'{output_folder_path}/gt/gt.json'

        counter = 0

        with open(file=f"{dict_file_path}.txt", mode='r', encoding='utf-8') as f:
            words_list = []
            lines = f.readlines()
            for line in lines:
                word = line.replace('\n', '')
                words_list.append(word)

        # The generators use the same arguments as the CLI, only as parameters
        print('Generating from sentences...')
        generator = GeneratorFromDict(
            length=sentence_length,
            allow_variable=True,
            language=dict_file_name,  # ['keras', '7led']
            fonts=[fonts_folder_name],
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
            image_dir=background_folder_name
        )

        ground_truth = {}
        for img, lbl in generator:
            # Do something with the pillow images here.
            image_name: str = lbl
            image_name = image_name.replace("/", "")
            identifier = str(counter)

            identifier = identifier.zfill(5)

            image_file_path = os.path.join(out_folder_name, f"{identifier}_{image_name}.jpg")

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

    dict_file = 'gym_text'  # ['gym_text', 'gym_numbers', 'gym_times'] in trdg/dicts
    fonts_folder = 'fit_race'  # ['led', 'fit_race'] folder in trdg/fonts
    background_folder = 'dark'  # ['dark'] folder in trdg/images
    output_folder_name = f'{dict_file}_{fonts_folder}'
    sentence_length = 1

    bb = MyTextGenerator(dict_file_name=dict_file,
                         out_folder_name=output_folder_name,
                         nb_of_sentences=100,
                         fonts_folder_name=fonts_folder,
                         background_folder_name=background_folder,
                         sentence_length=sentence_length)

