from DataStructure.Slide import *
import random


def get_initial_state(vertical_photos, horizontal_photos):
    n_verticalp = len(vertical_photos)
    n_horizontalp = len(horizontal_photos)

    n_max_slides = n_horizontalp

    if n_verticalp % 2:
        n_max_slides += n_verticalp / 2
    else:
        n_max_slides += (n_verticalp - 1) / 2

    n_slides = random.randint(1, n_max_slides)

    initial_state = []

    i = 1
    for i in n_slides:
        orientation = 0  # vertical slide by default

        if (n_verticalp > 1 and n_horizontalp > 0):
            orientation = random.randint(0, 1)
        elif n_horizontalp > 0:
            orientation = 1

        if (orientation):  #horizontal slide
            n = random.randint(1, n_horizontalp)

            photo = horizontal_photos[n]

            horizontal_photos.remove(horizontal_photos[n])

            n_horizontalp -= 1

            #create slide
            initial_state.append(Slide(photo))
        else:  #vertical slide
            #left photo
            n = random.randint(1, n_verticalp)

            left_photo = vertical_photos[n]

            vertical_photos.remove(vertical_photos[n])

            n_verticalp -= 1

            #right photo
            n = random.randint(1, n_verticalp)

            right_photo = vertical_photos[n]

            vertical_photos.remove(vertical_photos[n])

            n_verticalp -= 1

            #create slide
            initial_state.append(Slide(left_photo, right_photo))

    return initial_state