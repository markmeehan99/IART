class Slide:
    def __init__(self, photos):
        self.photos = photos
        self.tags = []
        for photo in photos:
            for tag in photo.tags:
                if tag not in self.tags:
                    self.tags.append(tag)

