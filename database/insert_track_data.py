import psycopg2
from database.db_config import connect_db
from datetime import datetime

def insert_track_data(track_data):
    try:
        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            for track in track_data:
                spotify_id = track.get('id')
                name = track.get('name')
                album_id = track.get('album', {}).get('id')
                artist_id = track.get('artists', [{}])[0].get('id')
                duration_ms = track.get('duration_ms')
                popularity = track.get('popularity')
                datacriacao = datetime.now()
                cursor.execute("""
                    INSERT INTO tracks (spotify_id, name, album_id, artist_id, duration_ms, popularity, datacriacao)
                    VALUES (%s, %s, %s, %s, %s, %s, %s)
                    ON CONFLICT (spotify_id) DO NOTHING;
                """, (spotify_id, name, album_id, artist_id, duration_ms, popularity,datacriacao))

            connection.commit()
            cursor.close()
            connection.close()
            print("Track data inserted successfully.")
    except Exception as e:
        print(f'Error inserting track data: {e}')
