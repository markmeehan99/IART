from copy import deepcopy
from DataStructure.Slide import Slide
import random
from profilehooks import timecall


class Slideshow:
    horizontal_photos_pool = dict()
    vertical_photos_pool = dict()
    h_photos_size = 0
    v_photos_size = 0
    all_ids_set_h = set()
    all_ids_set_v = set()

    def __init__(self, primary_solution):
        self.score = 0
        self.set_slides(primary_solution)

    def set_slides(self, solution):
        self.slides = solution
        self.current_photo_ids = set()
        self.missing_photo_ids_v = deepcopy(Slideshow.all_ids_set_v)
        self.missing_photo_ids_h = deepcopy(Slideshow.all_ids_set_h)
        for slide in solution:
            if slide.isVertical():
                self.current_photo_ids.add(slide.left_photo.id)
                self.current_photo_ids.add(slide.right_photo.id)
                self.missing_photo_ids_v.discard(slide.left_photo.id)
                self.missing_photo_ids_v.discard(slide.right_photo.id)
            else:
                self.current_photo_ids.add(slide.left_photo.id)
                self.missing_photo_ids_h.discard(slide.left_photo.id)

    def add_slide(self, slide):
        if slide.left_photo.id in self.current_photo_ids:
            return False
        if slide.isVertical():
            if slide.right_photo.id in self.current_photo_ids:
                return False
        self.slides.append(slide)
        if slide.isVertical():
            self.current_photo_ids.add(slide.left_photo.id)
            self.current_photo_ids.add(slide.right_photo.id)
            self.missing_photo_ids_v.discard(slide.left_photo.id)
            self.missing_photo_ids_v.discard(slide.right_photo.id)
        else:
            self.current_photo_ids.add(slide.left_photo.id)
            self.missing_photo_ids_h.discard(slide.left_photo.id)
        return True

    def remove_slide(self, slide):
        if slide.left_photo.id not in self.current_photo_ids:
            return False
        if slide.isVertical():
            if slide.right_photo.id not in self.current_photo_ids:
                return False
        self.slides.remove(slide)
        self.current_photo_ids.discard(slide.left_photo.id)
        self.missing_photo_ids.add(slide.left_photo.id)
        if slide.isVertical():
            self.current_photo_ids.discard(slide.right_photo.id)
            self.missing_photo_ids.add(slide.right_photo.id)
        return True

    @staticmethod
    def getScore(S):
        return S.calcFullScore()

    def calcFullScore(self):
        n_slides = len(self.slides)
        self.score = 0
        j = -1
        for i in range(n_slides):
            if j == -1 or i == n_slides:
                j += 1
                continue
            self.score += Slide.getScore(self.slides[j], self.slides[i])
            j += 1
        return self.score

    def __repr__(self):
        return "SS" + self.slides.__repr__()

    def __len__(self):
        return len(self.slides)

    def __lt__(self, other):
        return self.calcFullScore() < other.calcFullScore()

    @staticmethod
    def get_randomPhoto(orientation, sample_h, sample_v):
        if orientation == 'H':
            s_h = len(sample_h)
            if s_h == 0:
                return None
            i = random.sample(sample_h, 1)[0]
            return [Slideshow.horizontal_photos_pool[i]]
        elif orientation == 'V':
            s_v = len(sample_v)
            if s_v == 0 or s_v == 1:
                return None
            i = random.sample(sample_v, 2)
            return [
                Slideshow.vertical_photos_pool[i[0]],
                Slideshow.vertical_photos_pool[i[1]]
            ]

    @staticmethod
    def get_initial_state(top=None, exactly=False):
        n_verticalp = Slideshow.v_photos_size
        n_horizontalp = Slideshow.h_photos_size
        n_max_slides = top
        if top is None:
            n_max_slides = n_horizontalp
            if n_verticalp % 2:
                n_max_slides += n_verticalp // 2
            else:
                n_max_slides += (n_verticalp - 1) // 2

        n_slides = n_max_slides if exactly else random.randint(
            1, n_max_slides - 1)

        initial_solution = Slideshow([])

        possible = []
        if n_verticalp > 0:
            possible.append('V')
        if n_horizontalp > 0:
            possible.append('H')

        for i in range(n_slides):

            orientation = random.sample(possible, 1)[0]

            while True:
                photos = Slideshow.get_randomPhoto(
                    orientation, initial_solution.missing_photo_ids_h,
                    initial_solution.missing_photo_ids_v)
                if photos is None:
                    continue
                if orientation == 'V':
                    if initial_solution.add_slide(Slide(photos[0], photos[1])):
                        break
                else:
                    if initial_solution.add_slide(Slide(photos[0])):
                        break
        return initial_solution

    @staticmethod
    def reproduce(S1, S2):
        slides_size1 = len(S1.slides)
        slides_size2 = len(S2.slides)
        if slides_size1 != slides_size2:
            return Slideshow.spliceDif(S1, S2)
        else:
            return Slideshow.spliceEq(S1, S2)

    @staticmethod
    def spliceDif(S1, S2):
        minsize = min(len(S1), len(S2))
        # A is the biggest chromossome, B is the smallest
        A = None
        B = None
        if len(S1) == minsize:
            A = S2
            B = S1
        else:
            A = S1
            B = S2
        k = random.choice([-1, 1])
        # k = 1
        #         A1 | A2
        #   A -> XXXX XXXXX 7
        #   B -> XXXX       4
        #
        # k = -1
        #         A1  | A2
        #   A -> XXXXX XXXX
        #   B -> XXXX
        #
        #
        #   C -> A1 B
        #   D -> B A2
        A1 = A.slides[:k * minsize]
        A2 = A.slides[k * minsize:]
        B1 = B.slides

        return [
            Slideshow(Slideshow.RemDups(A1 + B1)),
            Slideshow(Slideshow.RemDups(B1 + A2))
        ]

    @staticmethod
    def spliceEq(A, B):
        midpoint = len(A.slides) // 2
        scramble = random.choice([True, False])
        k = random.choice([True, False])
        if scramble:
            C = []
            D = []
            for i in range(len(A.slides)):
                if i % 2 == 0:
                    C += ([B.slides[i], A.slides[i]]
                          if k else [A.slides[i], B.slides[i]])
                else:
                    D += ([B.slides[i], A.slides[i]]
                          if k else [A.slides[i], B.slides[i]])
            return [
                Slideshow(Slideshow.RemDups(C)),
                Slideshow(Slideshow.RemDups(D))
            ]
        else:
            A1 = A.slides[:midpoint]
            A2 = A.slides[midpoint:]
            B1 = B.slides[:midpoint]
            B2 = B.slides[midpoint:]
            return ([
                Slideshow(Slideshow.RemDups(A1 + B2)),
                Slideshow(Slideshow.RemDups(B1 + A2))
            ] if k else [
                Slideshow(Slideshow.RemDups(B2 + A2)),
                Slideshow(Slideshow.RemDups(B1 + A1))
            ])

    @staticmethod
    def RemDups(slideList):
        found = set()
        result = []
        for slide in slideList:
            if slide.isVertical():
                if slide.left_photo.id in found:
                    continue
                if slide.isVertical():
                    if slide.right_photo.id in found:
                        continue
                    found.add(slide.right_photo.id)
                found.add(slide.left_photo.id)
                result.append(slide)
        return result
