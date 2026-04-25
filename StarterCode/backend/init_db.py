import sqlite3

# connect to the database (if file does not exist -- create it)
connection = sqlite3.connect('database.db')

# open the schema.sql file which describes the database
with open('schema.sql') as db_file:
    # run the commands in this file
    connection.executescript(db_file.read())

# connect to the database with a cursor
cur = connection.cursor()

# add two default entries
cur.execute("INSERT INTO destinations (name, notes,cost) VALUES (?, ?, ?)",
            ('Hawaii', 'Beach trip', 3500)
            )
cur.execute("INSERT INTO destinations (name, notes, cost) VALUES (?, ?, ?)",
            ('Bahamas', 'Cruising', 4200)
            )

# commit changes and close the connection
connection.commit()
connection.close()