from copy import deepcopy
from Slide import Slide


class Slideshow:
    horizontal_photos_pool = []
    all_ids_set = set()
    vertical_photos_pool = []

    def __init__(self, id, primary_solution):
        self.id = id
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
