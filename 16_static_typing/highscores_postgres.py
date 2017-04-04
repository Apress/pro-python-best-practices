import psycopg2

DB_SETUP = '''
CREATE TABLE IF NOT EXISTS scores (
    player VARCHAR(25),
    score INTEGER);
    '''

db = psycopg2.connect(host="127.0.0.1",
                      user="krother",
                      dbname="highscores")
cur = db.cursor()

# create the database
cur.execute(DB_SETUP)

# fill the database with entries
insert = "INSERT INTO scores VALUES (%s,%s);"
cur.execute(insert, ('Ada', 5500))
cur.execute(insert, ('Bob', 4400))
cur.execute(insert, (3300, 'Charlie'))

# retrieve the top five entries in descending order
query = 'SELECT player, score FROM scores ORDER BY score DESC LIMIT 5;'
cur.execute(query)
for result in cur.fetchall():
    print(result)

db.close()
