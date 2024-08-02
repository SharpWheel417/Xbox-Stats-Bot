from src.model import db

class User:
  def __init__(self, name, chat_id, stage, xapi):
    self.name = name
    self.chat_id = chat_id
    self.stage = stage
    self.xapi = xapi

  def add(self):
    ### Проверка на существование юзера
    db.cursor.execute(f'SELECT * FROM users WHERE chat_id={self.chat_id}')
    u = db.cursor.fetchone()
    if u is None:
      db.cursor.execute(f'INSERT INTO users (name, chat_id, stage, xapi) VALUES ("{self.name}", {self.chat_id}, "{self.stage}", "{self.xapi}")')
      # Commit the changes to the database
      db.conn.commit()
    else:
      db.cursor.execute(f'UPDATE users SET stage = ? WHERE chat_id = ?', ('home', self.chat_id))
      print(f'User with chat_id {self.chat_id} already exists')


  def get(self):
    # Create a cursor object to perform database operations
    cursor = db.conn.cursor()
    cursor.execute(f'SELECT * FROM users WHERE chat_id={self.chat_id}')
    u = cursor.fetchone()
    if u is not None:
        user = User(u[1], u[2], u[3], u[4])
    else:
        user = None
    # Close the cursor and the connection to the database
    cursor.close()
    return user

  def get_id(self):
         # Create a cursor object to perform database operations
    cursor = db.conn.cursor()
    cursor.execute(f'SELECT id FROM users WHERE chat_id={self.chat_id}')
    u = cursor.fetchone()
    cursor.close()
    return u

  def get_stage(self):
    cursor = db.conn.cursor()
    cursor.execute(f'SELECT * FROM users WHERE chat_id={self.chat_id}')
    u = cursor.fetchone()
    if u is not None:
        user = User(u[1], u[2], u[3])
    else:
        user = None
    # Close the cursor and the connection to the database
    cursor.close()
    return user.stage



  def set_stage(self):
    # Create a cursor object to perform database operations
    cursor = db.conn.cursor()

    # Check if the user exists
    cursor.execute(f'SELECT * FROM users WHERE chat_id={self.chat_id}')
    u = cursor.fetchone()
    if u is None:
        # If the user doesn't exist, insert a new record
        db.cursor.execute(f'INSERT INTO users (name, chat_id, stage) VALUES ("{self.name}", {self.chat_id}, ?)', (self.stage,))
    else:
        db.cursor.execute(f'UPDATE users SET stage = ? WHERE chat_id = ?', (self.stage, self.chat_id))

    db.conn.commit()


  def set_xapi(self):
    db.cursor.execute(f'UPDATE users SET xapi = ? WHERE chat_id = ?', (self.xapi, self.chat_id))

    db.conn.commit()




def get_all():
    cursor = db.conn.cursor()
    cursor.execute(f'SELECT * FROM users')
    users = []
    for row in db.cursor.fetchall():
        user = User(row[1], row[2], row[3])
        users.append(user)
    # Close the cursor and the connection to the database
    cursor.close()
    return users