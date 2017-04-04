
import sqlite3

DB_SETUP = '''
CREATE TABLE IF NOT EXISTS scores (
    player VARCHAR(25),
    score INTEGER);
    '''

# create the database
db = sqlite3.connect('highscores.sqlite')
db.executescript(DB_SETUP)

# fill the database with entries
insert = 'INSERT INTO scores VALUES (?,?);'
db.execute(insert, ('Ada', 5500))
db.execute(insert, ('Bob', 4400))
db.execute(insert, (3300, 'Charlie'))


# retrieve the top five entries in descending order
query = 'SELECT player, score FROM scores ORDER BY score DESC LIMIT 5;'
for result in db.execute(query):
    player, score = result
    print(result)
