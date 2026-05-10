from .gender_detection import guess_gender

def similarity_score(w1, w2):

    gender1 = guess_gender(w1)
    gender2 = guess_gender(w2)

    score = 0.0

    if gender1 == gender2:
        score += 0.9

    if w1 == w2:
        score += 0.9

    if len(set(w1) & set(w2)) > 0:
        score += 0.2

    return round(score, 2)