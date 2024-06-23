import psycopg2
from database.db_config import connect_db
from datetime import datetime

def insert_genres_data(genres_data):
    try:
        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            datacriacao = datetime.now()

            for genre in genres_data['genres']:
                cursor.execute("""
                    INSERT INTO genres (genrename, datacriacao)
                    VALUES (%s, %s)
                    ON CONFLICT (genrename) DO NOTHING;
                """, (genre, datacriacao))

            connection.commit()
            cursor.close()
            connection.close()
            print("Genres data inserted successfully.")
    except Exception as e:
        print(f'Error inserting genres data: {e}')
