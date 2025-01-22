import imghdr
import json
import numpy as np
from PIL import Image
from customtkinter import filedialog

def validate_image(file_path):
    valid_types = ['jpeg', 'png']
    file_type = imghdr.what(file_path)
    return file_type in valid_types

def convert_image_to_json(image):
    image_array = np.array(image, dtype=np.float32)
    json_array = json.dumps(image_array.tolist())
    return json_array

def convert_json_to_image(image_data):
    image_array = np.array(json.loads(image_data))
    return Image.fromarray(image_array)

def download_image(image):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg"), ("All files", "*.*")]
    )
    if file_path:
        image_to_save = image.convert("RGB")
        image_to_save.save(file_path)