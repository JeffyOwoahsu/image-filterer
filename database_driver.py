import sqlite3

database_name = 'store_images.db'

def initialize_database():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS images
                 (image_id INTEGER PRIMARY KEY AUTOINCREMENT,
                 image_data TEXT NOT NULL,
                 image_name TEXT NOT NULL)''')

    connection.commit()
    connection.close()

def insert_image_to_database(image_data, image_name):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    query = "INSERT INTO images (image_data, image_name) VALUES (?, ?)"
    values = (image_data, image_name)
    cursor.execute(query, values)
    connection.commit()
    connection.close()

def retrieve_image_from_database(image_id):
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    query = "SELECT image_data, image_name FROM images WHERE image_id = ?"
    value = (image_id,)
    cursor.execute(query, value)
    row = cursor.fetchone()
    if row is not None:
        return row[0], row[1]
    else:
        raise Exception("Something went wrong in the database.")

def get_number_of_images():
    connection = sqlite3.connect(database_name)
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM images")
    row_count = len(cursor.fetchall())

    connection.commit()
    connection.close()
    return row_count