"""
Utility functions
"""

import os
import numpy as np
from PIL import Image

def load_dict(lang):
    """Read the dictionnary file and returns all words in it.
    """

    lang_dict = []
    with open(
        os.path.join(os.path.dirname(__file__), "dicts", lang + ".txt"),
        "r",
        encoding="utf8",
        errors="ignore",
    ) as d:
        lang_dict = [l for l in d.read().splitlines() if len(l) > 0]
    return lang_dict


def load_fonts(lang):
    """Load all fonts in the fonts directories
    """

    if lang == "cn":
        return [
            os.path.join(os.path.dirname(__file__), "fonts/cn", font)
            for font in os.listdir(os.path.join(os.path.dirname(__file__), "fonts/cn"))
        ]
    else:
        return [
            os.path.join(os.path.dirname(__file__), "fonts/latin", font)
            for font in os.listdir(
                os.path.join(os.path.dirname(__file__), "fonts/latin")
            )
        ]

def mask_to_bboxes(mask):
    """Process the mask and turns it into a list of AABB bounding boxes
    """

    mask_arr = np.array(mask)

    bboxes = []

    i = 0
    while True:
        try:
            color_tuple = ((i + 1) // (255 * 255), (i + 1) // 255, (i + 1) % 255)
            letter = np.where(np.all(mask_arr == color_tuple, axis=-1))
            bboxes.append((
                max(0, np.min(letter[1]) - 1),
                max(0, np.min(letter[0]) - 1),
                min(mask_arr.shape[1] - 1, np.max(letter[1]) + 1),
                min(mask_arr.shape[0] - 1, np.max(letter[0]) + 1),
            ))
            i += 1
        except Exception as ex:
            break

    return bboxes        

def draw_bounding_boxes(img, bboxes, color="green"):
    d = ImageDraw.Draw(img)

    for bbox in bboxes:
        d.rectangle(bbox, outline=color)
