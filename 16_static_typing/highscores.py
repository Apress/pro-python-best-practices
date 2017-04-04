
from typing import NamedTuple, List
import csv

Highscore = NamedTuple('Highscore', [('score', int), ('name', str)])


class HighscoreList:
    """A sorted list of top scores"""
    def __init__(self, places: int=10) -> None:
        self.scores = []     # type: List[Highscore]
        self.places = places

    def add(self, highscore: Highscore) -> None:
        self.scores.append(highscore)
        self.scores.sort()
        self.scores = self.scores[:self.places]

    def __repr__(self) -> str:
        return "\n".join(["{:10s} {}".format(s.name, s.score) for s in self.scores])


def load_highscores(filename: str) -> HighscoreList:
    hs = HighscoreList()
    for row in csv.reader(open(filename)):
        name = row[0]
        score = int(row[1])
        hs.add(Highscore(score, name))
    return hs


if __name__ == '__main__':
    # highscores = load_highscores('scores.csv')
    hs = HighscoreList()
    hs.add(Highscore(5500, 'Ada'))
    hs.add(Highscore(4400, 'Bob'))
    hs.add(Highscore('Charly', 777))
    print(hs)
