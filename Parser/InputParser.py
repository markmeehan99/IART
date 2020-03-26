import sys
from DataStructure.Photo import Photo as Photo
from DataStructure.Slideshow import Slideshow


def parse_input_file(file_name):
    with open(file_name) as input_file:
        num_photos = input_file.readline()

        id = 0
        for new_photo in input_file:
            [orientation, num_tags, tags] = new_photo.rstrip().split(" ", 2)
            if orientation == 'H':
                Slideshow.horizontal_photos_pool[id] = Photo(
                    id, orientation, tags)
                Slideshow.h_photos_size += 1
                Slideshow.all_ids_set_h.add(id)
            elif orientation == 'V':
                Slideshow.vertical_photos_pool[id] = Photo(
                    id, orientation, tags)
                Slideshow.v_photos_size += 1
                Slideshow.all_ids_set_v.add(id)
            id += 1
