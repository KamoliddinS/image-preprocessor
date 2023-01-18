
from PIL import Image
import cv2
import numpy as np

from io import BytesIO

def read_image_file(file) -> Image.Image:
    image = Image.open(BytesIO(file))
    return image


