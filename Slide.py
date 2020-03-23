class Slide:
    def __init__(self, photos):
        self.photos = photos
        self.tags = []
        
        for photo in photos:
            self.tags = list(set(self.tags) | set(photo.tags))

