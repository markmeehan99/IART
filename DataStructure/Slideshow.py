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
            return False
        if slide.isVertical():
            if slide.right_photo.id in self.current_photo_ids:
                return False
        self.slides.append(slide)
        self.current_photo_ids.add(slide.left_photo.id)
        self.missing_photo_ids.discard(slide.left_photo.id)
        if slide.isVertical():
            self.current_photo_ids.add(slide.right_photo.id)
            self.missing_photo_ids.discard(slide.right_photo.id)
        return True

    def remove_slide(self, slide):
        if slide.left_photo.id not in self.current_photo_ids:
            return False
        if slide.isVertical():
            if slide.right_photo.id not in self.current_photo_ids:
                return False
        self.slides.remove(slide)
        self.current_photo_ids.discard(slide.left_photo.id)
        self.missing_photo_ids.add(slide.left_photo.id)
        if slide.isVertical():
            self.current_photo_ids.discard(slide.right_photo.id)
            self.missing_photo_ids.add(slide.right_photo.id)
        return True

    def calcFullScore(self):
        n_slides = len(self.slides)
        j = -1
        for i in range(n_slides):
            if j == -1 or i == n_slides:
                pass
            self.score += Slide.getScore(self.slides[j], self.slides[i])
            j += 1

    @staticmethod
    def get_randomPhoto(orientation):
        photo_array = Slideshow.horizontal_photos_pool if (
            orientation) else Slideshow.vertical_photos_pool
        n_photos = len(Slideshow.horizontal_photos_pool) if (
            orientation) else len(Slideshow.vertical_photos_pool)
        return photo_array[random.randint(1, n_photos)]

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
            orientation = 0  # 0 is vertical, 1 is horizontal

            if (n_verticalp > 1 and n_horizontalp > 0):
                orientation = random.randint(0, 1)
            elif n_horizontalp > 0:
                orientation = 1

            while True:
                photo = Slideshow.get_randomPhoto(orientation)
                if initial_solution.add_slide(Slide(photo)):
                    break
        return initial_solution

    @staticmethod
    def reproduce(S1, S2):
        slides_size1 = len(S1.slides)
        slides_size2 = len(S1.slides)
        # if slides_size1 != slides_size2:

    @staticmethod
    def spliceDif(S1, S2, size1, size2):
        minsize = min(size1, size2)
        # A is the biggest chromossome, B is the smallest
        A = None
        B = None
        if size1 == minsize:
            A = S2
            B = S1
        else:
            A = S1
            B = S2
        k = random.choice([-1, 1])
        # k = 1
        #         A1 | A2
        #   A -> XXXX XXXXX
        #   B -> XXXX
        #
        # k = -1
        #         A1  | A2
        #   A -> XXXXX XXXX
        #   B -> XXXX
        #
        #
        #   C -> A1 B
        #   D -> B A2
        A1 = deepcopy(A.slides[:k * minsize])
        A2 = deepcopy(A.slides[k * minsize:])
        B1 = deepcopy(B.slides)

        return [A1 + B1, B1 + A2, A.tags.intersection(B.tags)]
