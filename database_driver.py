import sqlite3

database_name = 'placeholder.db'

def initialize_database():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS images
                 (image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 image_data BLOB NOT NULL,
                 image_name TEXT NOT NULL)''')

    connection.commit()
    connection.close()

def insert_image(image_data, image_name):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    query = "INSERT INTO images (image_data, image_name) VALUES (%s, %s)"
    values = (image_data, image_name)
    cursor.execute(query, values)
    connection.commit()
    connection.close()

def retrieve_image(image_id):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    query = "SELECT image_data, image_name FROM images WHERE image_id = (%s,)"
    value = (image_id,)
    cursor.execute(query, value)
    row = cursor.fetchone()
    return row[0], row[1]

def get_number_of_images():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT COUNT(*) FROM images")
    row_count = len(cursor.fetchall())

    connection.commit()
    connection.close()
    return row_count