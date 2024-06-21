import psycopg2

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
                    create_table_query = '''
                        CREATE TABLE IF NOT EXISTS artistid (
                            id SERIAL PRIMARY KEY,
                            spotify_id VARCHAR(255) UNIQUE NOT NULL
                        );
                    '''
                    cursor.execute(create_table_query)
                print("Tabela 'artistid' criada com sucesso.")
    except Exception as e:
        print(f'Erro ao criar tabela: {e}')
    finally:
        if connection:
            connection.close()

# Exemplo de execução da função create_table()
create_table()
