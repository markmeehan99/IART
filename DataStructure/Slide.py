class Slide:
    def __init__(self, left_photo, right_photo=None):
        self.orientation = 'H'
        self.left_photo = left_photo #the left photo of a Slide object is always different than None (is a Photo object)
        self.right_photo = right_photo # when the orientation of the slide if Horizontal, the right photo is null
        self.tags = left_photo.tags

        if right_photo is not None: #in this case, the right photo argument in not null, and therefore the slide is vertical
            self.tags |= self.right_photo.tags
            self.orientation = 'V'

    def isVertical(self): 
        return self.right_photo is not None

    #update tag union when there is a change in one of the vertical photos
    def update_tags(self):
        self.tags = self.left_photo.tags

        if self.right_photo is not None:
            self.tags |= self.right_photo.tags

    #compare "equal" function of this class
    def __eq__(self, value):
        if self.orientation != value.orientation:
            return False
        if self.left_photo != value.left_photo:
            return False
        if self.isVertical():
            if self.right_photo != value.right_photo:
                return False
        return True

    #hash to insert on the dictionary
    def __hash__(self):
        h = hash(self.left_photo)
        if self.isVertical():
            h += hash(self.right_photo)
        return h

    #defines the way slideshow is going to print itself: S<PHOTO_ID>S<PHOTO_L_ID, PHOTO_R_ID>
    def __repr__(self):
        s = "S<" + self.left_photo.__repr__()
        if self.isVertical():
            s += ", " + self.right_photo.__repr__()
        return s + ">"

    # Heuristics
    @staticmethod
    def getCommonTagsCount(prevSlide, nextSlide):
        return len(prevSlide.tags & nextSlide.tags)

    @staticmethod
    def getUniqueTags(prevSlide, nextSlide):
        return len(prevSlide.tags - nextSlide.tags)

    @staticmethod
    def getScore(prevSlide, nextSlide):
        h1 = Slide.getCommonTagsCount(prevSlide, nextSlide)
        h2 = Slide.getUniqueTags(prevSlide, nextSlide)
        h3 = Slide.getUniqueTags(nextSlide, prevSlide)

        return min(h1, h2, h3)
