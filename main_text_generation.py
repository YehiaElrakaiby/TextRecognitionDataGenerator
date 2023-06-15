import json
import os
import pathlib
import random
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
                 background_folder_name: str,
                 ):
        """
        Generates synthetic images and a ground truth file containing a JSON dictionary mapping the path of the image
        to its label (the sentence)

        @param dict_file_name: the words to use
        @param out_folder_name: where to save the images and the ground truth file
        @param nb_of_sentences: the number of sentences to generate
        @param fonts_folder_name: the language (dictionary words) to use for generation of sentences
        @param background_folder_name: the directory where background images are stored
        """

        current_directory = os.getcwd()
        dict_file_path = f'{current_directory}/trdg/dicts/{dict_file_name}'
        output_folder_path = f'{current_directory}/out/{out_folder_name}'
        background_folder_path = f'{current_directory}/trdg/images/{background_folder_name}'

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
            fonts=fonts_folder_name,
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
            image_dir=background_folder_path
        )

        ground_truth = {}
        for img, lbl in generator:
            # Do something with the pillow images here.
            image_name: str = lbl
            image_name = image_name.replace("/", "")
            identifier = str(counter)

            identifier = identifier.zfill(5)

            image_file_path = os.path.join(output_folder_path, f"{identifier}_{image_name}.jpg")

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

    @staticmethod
    def generate_time():
        # Generate a random time in the format HH:MM:SS or HH:MM
        hour = str(random.randint(0, 23)).zfill(2)
        minute = str(random.randint(0, 59)).zfill(2)
        second = str(random.randint(0, 59)).zfill(2)
        # rand_1_4 = random.randint(0, 4)
        # if rand_1_4 == 4:
        #    separator = "."
        # else:
        separator = ":"

        rand_1_4 = random.randint(0, 4)

        if rand_1_4 != 4:
            time_str = f'{minute}{separator}{second}'
        else:
            time_str = f'{hour}{separator}{minute}{separator}{second}'

        return time_str

    @staticmethod
    def generate_number():
        # Generate a random number in the format XXX.XX, XXX,xX or XXXXX
        number = str(random.randint(0, 99999))
        decimals = str(random.randint(0, 99)).zfill(2)
        rand_1_2 = random.randint(0, 2)
        if rand_1_2 == 2:
            separator = ','
        else:
            separator = '.'

        rand_1_2 = random.randint(0, 2)
        if rand_1_2 == 2:
            return number
        else:
            return f'{number}{separator}{decimals}'

    @staticmethod
    def generate_time_dictionary(number_entries):
        current_directory = os.getcwd()

        dict_directory: pathlib.Path = pathlib.Path(f'{current_directory}/trdg/dicts')

        file_path = dict_directory.joinpath("gym_times.txt")  # Specify the filename

        # Open the file in append mode (a+)
        # This will create the file if it doesn't exist and position the cursor at the end of the file
        with open(file_path, "a+") as file:
            for i in range(number_entries):
                file.write(f"{MyTextGenerator.generate_time()}\n")  # Write the data you want to append

    @staticmethod
    def generate_number_dictionary(number_entries):
        current_directory = os.getcwd()

        dict_directory: pathlib.Path = pathlib.Path(f'{current_directory}/trdg/dicts')

        file_path = dict_directory.joinpath("gym_numbers.txt")  # Specify the filename

        # Open the file in append mode (a+)
        # This will create the file if it doesn't exist and position the cursor at the end of the file
        with open(file_path, "a+") as file:
            for i in range(number_entries):
                file.write(f"{MyTextGenerator.generate_number()}\n")  # Write the data you want to append


if __name__ == '__main__':
    dict_file_i = 'gym_numbers'  # ['gym_text', 'gym_numbers', 'gym_times'] in trdg/dicts
    fonts_folder_i = 'fit_race'  # ['led', 'fit_race'] folder in trdg/fonts
    background_folder_i = 'dark'  # ['dark'] folder in trdg/images
    output_folder_name_i = f'{dict_file_i}_{fonts_folder_i}'
    sentence_length_i = 1

    # MyTextGenerator.generate_time_dictionary(number_entries=100000)
    # MyTextGenerator.generate_number_dictionary(number_entries=100000)

    bb = MyTextGenerator(dict_file_name=dict_file_i,
                         out_folder_name=output_folder_name_i,
                         nb_of_sentences=100000,
                         fonts_folder_name=fonts_folder_i,
                         background_folder_name=background_folder_i,
                         sentence_length=sentence_length_i)
