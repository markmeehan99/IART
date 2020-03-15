def getScore(Slide1Tags, Slide2Tags):
    h1 = getCommonTagsCount(Slide1Tags, Slide2Tags)
    h2 = getUniqueTags(Slide1Tags, Slide2Tags)
    h3 = getUniqueTags(Slide2Tags, Slide1Tags)
    
    return min(h1, h2, h3)


def getCommonTagsCount(PreviousTags, NextTags):
    return len(list(set(PreviousTags).intersection(NextTags)))

def getUniqueTags(BaseTags, ComparedTags):
    return len(list(set(BaseTags) - set(ComparedTags)))
