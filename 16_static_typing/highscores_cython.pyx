

cdef struct Highscore:
    char *name
    int score

cdef Highscore scores[5]

scores[0] = Highscore('Ada', 5500)
scores[1] = Highscore('Bob', 4400)
scores[2] = Highscore(3300, 'Charly')


for i in range(2):
    print(scores[i].name, scores[i].score)
