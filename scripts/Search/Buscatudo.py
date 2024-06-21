
import subprocess
import json
import os
from database.db_config import connect_db

#     Realiza uma pesquisa na API do Spotify usando o comando curl.

#     :param access_token: Token de acesso do usuário.
#     :param query: Consulta de pesquisa.
#     :param types: Lista de tipos de itens para pesquisar. Ex: ['album', 'artist', 'track'].
#     :param market: Código do país (ISO 3166-1 alpha-2) para filtrar resultados.
#     :param limit: Número máximo de resultados a retornar. (0-50)
#     :param offset: Índice do primeiro resultado a retornar. (0-1000)
#     :param include_external: Define se o conteúdo externo é incluído, ex: 'audio'.
#     :return: Resultado da pesquisa em formato JSON.

# scripts/Search/Buscatudo.py


def realizar_pesquisa(access_token):
    query = input("Digite a consulta de pesquisa: ")
    item_types = input("Digite os tipos de itens a pesquisar (album, artist, track), separados por vírgula: ")
    limit = input("Digite o número máximo de resultados (0-50): ")

    url = f"https://api.spotify.com/v1/search?q={query}&type={item_types}&limit={limit}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    curl_command = [
        'curl',
        '--request', 'GET',
        '--url', url,
        '--header', f"Authorization: Bearer {access_token}"
    ]

    print(f"Comando cURL: {' '.join(curl_command)}")

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        search_results = json.loads(result.stdout)
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'search_results.txt')

        with open(file_path, 'w') as file:
            json.dump(search_results, file, indent=4)

        print(f"Resultados da Pesquisa foram salvos em {file_path}")

        # Inserir dados no banco de dados
        insert_to_db(search_results)
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')

def insert_to_db(search_results):
    try:
        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            artists = search_results.get('artists', {}).get('items', [])
            for artist in artists:
                spotify_id = artist.get('id')
                try:
                    cursor.execute('INSERT INTO artistid (spotify_id) VALUES (%s) ON CONFLICT (spotify_id) DO NOTHING', (spotify_id,))
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