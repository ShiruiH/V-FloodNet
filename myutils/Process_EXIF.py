import os
from PIL import Image
from PIL.ExifTags import TAGS
from datetime import datetime


def get_date_taken(path, return_type='datetime'):
    """
    return_type:
        "datetime" -> returns a datetime object
        "string"   -> returns string in 'YYYY:MM:DD HH:MM:SS' (EXIF format)
    """
    try:
        image = Image.open(path)
        exif_data = image._getexif()
        if exif_data is not None:
            for tag, value in exif_data.items():
                decoded = TAGS.get(tag, tag)
                if decoded == 'DateTimeOriginal':
                    if return_type == 'string':
                        return value  # EXIF already stores it as 'YYYY:MM:DD HH:MM:SS'
                    return datetime.strptime(value, "%Y:%m:%d %H:%M:%S")
    except Exception as e:
        print(f'Error reading {path}: {e}')
    return None


def rename_with_date_taken(file_path, return_type):
    date_str = get_date_taken(file_path, return_type)
    if date_str:
        dt = datetime.strptime(date_str, '%Y:%m:%d %H:%M:%S')
        new_name = dt.strftime('%Y-%m-%d-%H-%M-%S') + os.path.splitext(file_path)[1]
        new_path = os.path.join(os.path.dirname(file_path), new_name)
        os.rename(file_path, new_path)
        print(f"Renamed to: {new_name}")
    else:
        print(f"No Date Taken found for: {file_path}")
