from src.model import db

class Game:
  def __init__(self, user_id, name, game_id):
    self.user_id = user_id
    self.name = name
    self.game_id = game_id

  def add(self):
    ### Проверка на существование юзера
    db.cursor.execute(f'SELECT * FROM games WHERE user_id={self.user_id} AND game_id={self.game_id}')
    u = db.cursor.fetchone()
    if u is None:
      db.cursor.execute(f'INSERT INTO games (user_id, name, game_id) VALUES ({self.user_id}, "{self.name}", {self.game_id})')
      # Commit the changes to the database
      db.conn.commit()
    else:
      print(f'Game {self.game_id} already exists')


  def get_all(self):
    db.cursor.execute(f'SELECT * FROM games WHERE user_id={self.user_id}')
    games = []
    for row in db.cursor.fetchall():
        game = Game('', row[2], row[3])
        games.append(game)
    # Close the cursor and the connection to the database
    return games

  def get_game_id(self):
    db.cursor.execute(f'SELECT game_id FROM games WHERE name = "{self.name}"')
    return db.cursor.fetchone()[0]
