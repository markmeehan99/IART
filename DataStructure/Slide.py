class Slide:
    def __init__(self, left_photo, right_photo=None):
        self.orientation = 'V'
        self.left_photo = left_photo
        self.right_photo = right_photo

        if right_photo is not None:
            self.tags = set(self.left_photo.tags) | set(self.right_photo.tags)
        else:
            self.tags = set(left_photo.tags)

    def isVertical(self):
        return self.right_photo is not None

    def __eq__(self, value):
        if self.orientation != value.orientation:
            return False
        if self.left_photo != value.left_photo:
            return False
        if self.isVertical():
            if self.right_photo != value.right_photo:
                return False
        return True

    # Heuristics
    @staticmethod
    def getCommonTagsCount(prevSlide, nextSlide):
        return len(prevSlide.tags.intersection(nextSlide.tags))

    @staticmethod
    def getUniqueTags(prevSlide, nextSlide):
        return len(prevSlide.tags - nextSlide.tags)

    @staticmethod
    def getScore(prevSlide, nextSlide):
        h1 = Slide.getCommonTagsCount(prevSlide, nextSlide)
        h2 = Slide.getUniqueTags(prevSlide, nextSlide)
        h3 = Slide.getUniqueTags(nextSlide, prevSlide)

        return min(h1, h2, h3)
