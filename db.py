from config import conn


def create_schemas():
    with conn:
        cur = conn.cursor()
        cur.execute('''
        CREATE TABLE IF NOT EXISTS Piggies(id SERIAL PRIMARY KEY, link VARCHAR(200));
        CREATE TABLE IF NOT EXISTS Users(id BIGINT PRIMARY KEY, times_won INT);
        CREATE TABLE IF NOT EXISTS Games(id SERIAL PRIMARY KEY, played DATE, winner_id BIGINT REFERENCES Users(id));
        CREATE TABLE IF NOT EXISTS Phrases(id SERIAL PRIMARY KEY, prelude VARCHAR(200), final VARCHAR(200));
        ''')


def get_pigs(pig_id):
    with conn:
        cur = conn.cursor()
        cur.execute('select link from Piggies where id=(%s)', (pig_id,))
        return cur.fetchone()[0]


def get_players() -> list[int]:
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT id FROM Users')
        return [i[0] for i in cur.fetchall()]


def check_not_played_today() -> bool:
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT played FROM Games WHERE played=CURRENT_DATE')
        return not (cur.fetchall())


def add_to_game(member_id):
    with conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO Users(id, times_won) VALUES(%s, %s);', (member_id, 0))


def get_phrase(phrase_id, phrase_type):
    with conn:
        cur = conn.cursor()
        if phrase_type == 'prelude':
            cur.execute('SELECT prelude FROM Phrases where id=(%s)', (phrase_id,))
        elif phrase_type == 'final':
            cur.execute('SELECT final FROM Phrases where id=(%s)', (phrase_id,))
        else:
            pass
        return cur.fetchone()[0]


def get_stats():
    with conn:
        cur = conn.cursor()
        cur.execute('SELECT id, times_won FROM Users ORDER BY times_won DESC')
        return [i for i in cur.fetchall()]


def reg_game(winner_id):
    with conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO Games(played, winner_id) VALUES(CURRENT_DATE, (%s))', (winner_id,))
        cur.execute('UPDATE Users SET times_won=times_won+1 WHERE id=(%s)', (winner_id,))


def fill_phrases(prelude, final):
    with conn:
        cur = conn.cursor()
        for i in range(len(prelude)):
            cur.execute('INSERT INTO PHRASES(prelude, final) VALUES(%s, %s)', (prelude[i], final[i]))


def fill_photos():
    with conn:
        cur = conn.cursor()
        with open('photos.txt', 'r') as f:
            for line in f:
                cur.execute('INSERT INTO Piggies(link) VALUES(%s)', (line.strip(),))
