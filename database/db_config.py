# database/db_config.py

import psycopg2
from psycopg2 import sql

def connect_db():
    try:
        connection = psycopg2.connect(
            dbname="spotify",
            user="seu_usuario",       # Substitua pelo seu usuário do banco de dados
            password="sua_senha",     # Substitua pela sua senha do banco de dados
            host="localhost"
        )
        return connection
    except Exception as e:
        print(f'Erro ao conectar ao banco de dados: {e}')
        return None

def create_table():
    connection = connect_db()
    if connection:
        cursor = connection.cursor()
        create_table_query = '''
            CREATE TABLE IF NOT EXISTS artistid (
                id SERIAL PRIMARY KEY,
                spotify_id VARCHAR(255) UNIQUE NOT NULL
            );
        '''
        try:
            cursor.execute(create_table_query)
            connection.commit()
            print("Tabela 'artistid' criada com sucesso.")
        except Exception as e:
            print(f'Erro ao criar tabela: {e}')
        finally:
            cursor.close()
            connection.close()
