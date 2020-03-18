import sys
from DataStructure.Photo import *

def parse_input_file(file_name, vertical_photos, horizontal_photos):
    with open(file_name) as input_file:
        num_photos = input_file.readline()

        id = 0
        for new_photo in input_file:
            [orientation, num_tags, tags] = new_photo.rstrip().split(" ", 2)
            if orientation == 'H':
                horizontal_photos.gallery.append(Photo(id, orientation, tags))

            elif orientation == 'V':
                vertical_photos.gallery.append(Photo(id, orientation, tags))

            id += 1