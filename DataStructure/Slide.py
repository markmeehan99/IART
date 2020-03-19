class Slide:
    def __init__(self, photo): #horizontal constructor
        self.orientation = 'H'
        self.left_photo = photo
        self.right_photo = None
        
        self.tags = self.photo.tags

    def __init__(self, left_photo, right_photo): #vertical constructor
        self.orientation = 'V'
        self.left_photo = left_photo
        self.right_photo = right_photo

        self.tags = list(set(self.left_photo.tags) | set(self.right_photo.tags))

