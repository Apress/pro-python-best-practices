
from collections import namedtuple

Highscore = namedtuple('Highscore', ['score', 'name'])

highscores = []


def add(name, score):
    assert type(name) is str
    assert type(score) is int
    hs = Highscore(score, name)
    highscores.append(hs)
    assert len(highscores) < 5


add('Ada', 5500)
add('Bob', 4400)
add(3300, 'Charly')
