import imghdr

def validate_image(file_path):
    valid_types = ['jpeg', 'png']
    file_type = imghdr.what(file_path)
    return file_type in valid_types