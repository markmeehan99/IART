class Slide:
    def __init__(self, left_photo, right_photo=None):
        self.orientation = 'H'
        self.left_photo = left_photo
        self.right_photo = right_photo
        self.tags = left_photo.tags

        if right_photo is not None:
            self.tags |= self.right_photo.tags
            self.orientation = 'V'

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

    def __hash__(self):
        h = hash(self.left_photo)
        if self.isVertical():
            h += hash(self.right_photo)
        return h

    def __repr__(self):
        s = "S<" + self.left_photo.__repr__()
        if self.isVertical():
            s += ", " + self.right_photo.__repr__()
        return s + ">"

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
