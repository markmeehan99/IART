from copy import deepcopy
from Slide import Slide
import random


class Slideshow:
    horizontal_photos_pool = []
    all_ids_set = set()
    vertical_photos_pool = []

    def __init__(self, primary_solution):
        self.score = 0
        self.set_slides(primary_solution)

    def set_slides(self, solution):
        self.slides = solution
        self.current_photo_ids = set()
        self.missing_photo_ids = deepcopy(Slideshow.all_ids_set)
        for slide in solution:
            self.current_photo_ids.add(slide.left_photo.id)
            if slide.right_photo is not None:
                self.current_photo_ids.add(slide.right_photo.id)

    def add_slide(self, slide):
        if slide.left_photo.id in self.current_photo_ids:
            return
        if slide.isVertical():
            if slide.right_photo.id in self.current_photo_ids:
                return
        self.slides.append(slide)
        self.current_photo_ids.add(slide.left_photo.id)
        self.missing_photo_ids.discard(slide.left_photo.id)
        if slide.isVertical():
            self.current_photo_ids.add(slide.right_photo.id)
            self.missing_photo_ids.discard(slide.right_photo.id)

    def remove_slide(self, slide):
        if slide.left_photo.id not in self.current_photo_ids:
            return
        if slide.isVertical():
            if slide.right_photo.id not in self.current_photo_ids:
                return
        self.slides.remove(slide)
        self.current_photo_ids.discard(slide.left_photo.id)
        self.missing_photo_ids.add(slide.left_photo.id)
        if slide.isVertical():
            self.current_photo_ids.discard(slide.right_photo.id)
            self.missing_photo_ids.add(slide.right_photo.id)

    def calcFullScore(self):
        n_slides = len(self.slides)
        j = -1
        for i in range(n_slides):
            if j == -1 or i == n_slides:
                pass
            self.score += Slide.getScore(self.slides[j], self.slides[i])
            j += 1

    @staticmethod
    def get_initial_state():
        n_verticalp = len(Slideshow.vertical_photos_pool)
        n_horizontalp = len(Slideshow.horizontal_photos_pool)
        n_max_slides = n_horizontalp

        if n_verticalp % 2:
            n_max_slides += n_verticalp / 2
        else:
            n_max_slides += (n_verticalp - 1) / 2

        n_slides = random.randint(1, n_max_slides)

        initial_solution = Slideshow()

        i = 1
        for i in range(n_slides):
            orientation = 0  # vertical slide by default

            if (n_verticalp > 1 and n_horizontalp > 0):
                orientation = random.randint(0, 1)
            elif n_horizontalp > 0:
                orientation = 1

            if (orientation):  # horizontal slide
                n = random.randint(1, n_horizontalp)

                photo = Slideshow.horizontal_photos_pool[n]

                # create slide
                initial_solution.add_slide(Slide(photo))
            else:  # vertical slide
                # left photo
                n = random.randint(1, n_verticalp)

                left_photo = Slideshow.vertical_photos_pool[n]

                n_verticalp -= 1

                # right photo
                n = random.randint(1, n_verticalp)

                right_photo = Slideshow.vertical_photos_pool[n]

                # create slide
                initial_solution.add_slide(Slide(left_photo, right_photo))

        return initial_solution
