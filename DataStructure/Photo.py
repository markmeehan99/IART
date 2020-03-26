class Photo:
    def __init__(self, photoId, orientation, tags):
        self.id = photoId
        self.orientation = orientation
        self.tags = tags

    def __eq__(self, value):
        return self.id == value.id