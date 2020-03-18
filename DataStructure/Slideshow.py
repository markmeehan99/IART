class Slideshow:
    def __init__(self, id, primary_solution):
        self.id = id
        self.slides = primary_solution
        
    def set_slides(self, slide_set):
        self.slides = slide_set
    
    def add_slide(self, slide):
        self.slides.append(slide)    

