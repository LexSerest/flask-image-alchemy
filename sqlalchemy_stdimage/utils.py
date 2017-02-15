from os.path import split, join, splitext
from uuid import uuid4
from wand.image import Image as WandImage


def get_unique_filename(file_name, upload_to):
    _, file_extension = splitext(file_name)
    new_file_name = str(uuid4()) + file_extension
    if upload_to:
        return join(upload_to.strip('/'), new_file_name)
    return new_file_name

def validate_variations(variations):
    for key, value in variations.items():
        if not isinstance(key, str):
            raise ValueError("Variation name should be `str` type")
        if not isinstance(value, dict):
            raise ValueError("Variation should contains `dict`")
        if 'height' not in value.keys():
            raise ValueError("Missing 'height' value")
        if 'width' not in value.keys():
            raise ValueError("Missing 'width' value")
    return variations

def resize_image(image_file, options):
    img = WandImage(file=image_file)
    img.resize(
        height=options.get('height'),
        width=options.get('width')
    )
    return img

def create_new_filename(original_file_path, thumbnail_name):
    pathname, file_name = split(original_file_path)
    original_file_path, ext = file_name.split(".")
    new_file_name = "{old_name}.{thumbnail_name}.{ext}".format(
        old_name=original_file_path,
        thumbnail_name=thumbnail_name,
        ext=ext,
    )
    return join(pathname, new_file_name)

def process_thumbnail(file, filename, variations, storage):
    for name, options in variations.items():
        file.seek(0)
        new_file = resize_image(file, options)
        new_file_name = create_new_filename(filename, name)
        storage.write(new_file.make_blob(), new_file_name)
        yield name, new_file_name