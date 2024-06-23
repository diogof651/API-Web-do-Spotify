import psycopg2

from database.insert_codPaises_iso_3166 import insert_codPaises_iso_3166

def connect_db():
    try:
        connection = psycopg2.connect(
            dbname="spotify",  # Nome do banco de dados
            user="postgres",  # Seu usuário do PostgreSQL
            password="123",  # Sua senha do PostgreSQL
            host="localhost",  # Host onde o PostgreSQL está sendo executado
            port=5433  # Porta do PostgreSQL (deve ser um número inteiro)
        )
        return connection
    except Exception as e:
        print(f'Erro ao conectar ao banco de dados: {e}')
        return None

def create_table():
    try:
        connection = connect_db()
        if connection:
            with connection:
                with connection.cursor() as cursor:
                    create_table_artistid = '''
                        CREATE TABLE IF NOT EXISTS artistid (
                            id SERIAL PRIMARY KEY,
                            spotify_id VARCHAR(255) UNIQUE NOT NULL,
                            datacriacao timestamp with time zone NOT NULL
                        );
                    '''
                    create_table_albums = '''
                        CREATE TABLE IF NOT EXISTS albums (
                            id VARCHAR(255) PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            album_type VARCHAR(50),
                            release_date DATE,
                            total_tracks INTEGER,
                            external_url VARCHAR(255),
                            datacriacao timestamp with time zone NOT NULL
                        );
                    '''
                    create_table_artists = '''
                        CREATE TABLE IF NOT EXISTS artists (
                            id VARCHAR(255) PRIMARY KEY,
                            name VARCHAR(255) NOT NULL,
                            external_url VARCHAR(255),
                            datacriacao timestamp with time zone NOT NULL
                        );
                    '''
                    create_table_album_artists = '''
                        CREATE TABLE IF NOT EXISTS album_artists (
                            album_id VARCHAR(255) REFERENCES albums (id),
                            artist_id VARCHAR(255) REFERENCES artists (id),
                            PRIMARY KEY (album_id, artist_id),
                            datacriacao timestamp with time zone NOT NULL
                        );
                    '''
                    create_table_track = '''
                        CREATE TABLE IF NOT EXISTS tracks (
                            id SERIAL PRIMARY KEY,
                            spotify_id VARCHAR(255) UNIQUE NOT NULL,
                            name VARCHAR(255) NOT NULL,
                            album_id VARCHAR(255),
                            artist_id VARCHAR(255),
                            duration_ms INT,
                            popularity INT,
                            datacriacao timestamp with time zone NOT NULL
                        );
                        '''
                    create_table_genres = '''
                        CREATE TABLE IF NOT EXISTS genres (
                            id SERIAL PRIMARY KEY,
                            genrename VARCHAR(255) UNIQUE NOT NULL,
                            datacriacao timestamp with time zone NOT NULL
                        );
                    '''
                    create_table_market = ('''
                        CREATE TABLE IF NOT EXISTS market (
                            code CHAR(2) PRIMARY KEY,
                            country_name VARCHAR(255),
                            year INT
                        );
                        ''')

                    cursor.execute(create_table_track)
                    cursor.execute(create_table_artistid)
                    cursor.execute(create_table_albums)
                    cursor.execute(create_table_artists)
                    cursor.execute(create_table_album_artists)
                    cursor.execute(create_table_genres)
                    cursor.execute(create_table_market)
                    cursor.execute(insert_codPaises_iso_3166(cursor))  #Diogo 23/06/2024 insere dados na tabela market
                    
                print("Tabelas criadas com sucesso.")
    except Exception as e:
        print(f'Erro ao inserir dados tabelas: {e}')
    finally:
        if connection:
            connection.close()

# Exemplo de execução da função create_table()
create_table()
