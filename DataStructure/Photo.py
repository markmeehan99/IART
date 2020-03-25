class Photo:
    def __init__(self, photoId, orientation, tags):
        self.id = photoId
        self.orientation = orientation
        self.tags = tags

    def __eq__(self, value):
        return self.id == value.id

    def __hash__(self):
        return hash(str(self.id))

    def __repr__(self):
        return str(self.id)
