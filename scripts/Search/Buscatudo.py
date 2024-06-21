import subprocess
import json
import os
import psycopg2  # Importe psycopg2 para conectar ao PostgreSQL
from database.db_config import connect_db  # Importe a função connect_db do seu arquivo db_config

def realizar_pesquisa(access_token):
    query = input("Digite a consulta de pesquisa: ")
    item_types = input("Digite os tipos de itens a pesquisar (album, artist, track), separados por vírgula: ")
    limit = int(input("Digite o número máximo de resultados por página (máximo 50): "))
    total_results = int(input("Digite o número total de resultados desejados: "))

    url = f"https://api.spotify.com/v1/search?q={query}&type={item_types}&limit={limit}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    all_results = []
    offset = 0

    while len(all_results) < total_results:
        url_with_offset = f"{url}&offset={offset}"
        curl_command = [
            'curl',
            '--request', 'GET',
            '--url', url_with_offset,
            '--header', f"Authorization: Bearer {access_token}"
        ]

        try:
            result = subprocess.run(curl_command, capture_output=True, text=True, check=True, encoding='utf-8')
        except subprocess.CalledProcessError as e:
            print(f'Erro ao chamar a API do Spotify: {e}')
            break

        if result.stdout:
            try:
                search_results = json.loads(result.stdout)
                items = search_results.get('artists', {}).get('items', [])  # Ajuste para acessar corretamente os itens de artistas
                all_results.extend(items)
                offset += limit
            except (json.JSONDecodeError, AttributeError) as e:
                print(f'Erro ao decodificar ou processar os resultados da API: {e}')
                break
        else:
            print(f'A saída do subprocesso está vazia. Verifique a consulta.')

    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'search_results.txt')
    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(all_results, file, indent=4, ensure_ascii=False)

    print(f"Resultados da Pesquisa foram salvos em {file_path}")

    # Inserir dados no banco de dados
    insert_to_db(all_results)


def insert_to_db(search_results):
    try:
        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            for artist in search_results:
                spotify_id = artist.get('id')

                # Verificar se o spotify_id já existe no banco de dados
                cursor.execute('SELECT spotify_id FROM artistid WHERE spotify_id = %s', (spotify_id,))
                existing_id = cursor.fetchone()

                if existing_id:
                    print(f'Spotify ID {spotify_id} já existe no banco de dados. Pulando inserção.')
                else:
                    # Inserir o spotify_id no banco de dados
                    try:
                        cursor.execute('INSERT INTO artistid (spotify_id) VALUES (%s)', (spotify_id,))
                        print(f'Inserido ID do artista: {spotify_id}')
                    except Exception as e:
                        print(f'Erro ao inserir dados no banco de dados: {e}')

            connection.commit()
            cursor.close()
            connection.close()

            print("Dados inseridos no banco de dados com sucesso.")
    except Exception as e:
        print(f'Erro ao conectar ou inserir dados no banco de dados: {e}')


# Exemplo de uso (comentado)
# """
# access_token = 'seu_token_de_acesso_aqui'
# query = 'remaster track:Doxy artist:Miles Davis'
# results = search_spotify(access_token, query, types=['album', 'track'], limit=10)

# if results:
#     for item_type in ['albums', 'tracks', 'artists']:
#         print(f"\n{item_type.capitalize()}:")
#         for item in results.get(item_type, {}).get('items', []):
#             if item_type == 'albums':
#                 print(f"Álbum: {item['name']}, ID: {item['id']}, Artistas: {', '.join(artist['name'] for artist in item['artists'])}")
#             elif item_type == 'tracks':
#                 print(f"Faixa: {item['name']}, ID: {item['id']}, Artista: {item['artists'][0]['name']}")
#             elif item_type == 'artists':
#                 print(f"Artista: {item['name']}, ID: {item['id']}")
# """
