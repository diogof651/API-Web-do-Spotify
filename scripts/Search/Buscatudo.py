from datetime import datetime
import subprocess
import json
import os
import psycopg2  # Importe psycopg2 para conectar ao PostgreSQL
from database.db_config import connect_db  # Importe a função connect_db do seu arquivo db_config
from database.insert_track_data import insert_track_data
from database.insert_genres_data import insert_genres_data
from scripts.Serviços.Genres_service.Genres_functions import get_available_genre_seeds

from datetime import datetime
import subprocess
import json
import os
import psycopg2  # Importe psycopg2 para conectar ao PostgreSQL
from database.db_config import connect_db  # Importe a função connect_db do seu arquivo db_config
from database.insert_track_data import insert_track_data
from database.insert_genres_data import insert_genres_data
from scripts.Serviços.Genres_service.Genres_functions import get_available_genre_seeds

def realizar_pesquisa(access_token):
    query = input("Digite a consulta de pesquisa: ")

    if query.lower() == 'genres':
        genres = get_available_genre_seeds(access_token)
        if genres:
            print("Gêneros disponíveis:")
            for genre in genres['genres']:
                print(genre)
                if 'genre' in item_types:
                    insert_genres_data(all_results)
        return

    item_types = input("Digite os tipos de itens a pesquisar (album, artist, track, playlist, show, episode, audiobook), separados por vírgula: ")
    limit = int(input("Digite o número máximo de resultados por página (máximo 50): "))
    total_results = int(input("Digite o número total de resultados desejados: "))

    url = f"https://api.spotify.com/v1/search?q={query}&type={item_types}&limit={limit}"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    all_results = []
    url_with_offset = url  # Começa com a URL sem offset
    print(url)
    # Executa a busca
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
        return

    if result.stdout:
        try:
            search_results = json.loads(result.stdout)

            if 'artist' in item_types.split(','):
                while len(all_results) < total_results:
                    items = search_results.get('artists', {}).get('items', [])
                    all_results.extend(items)
                    if len(all_results) >= total_results:
                        break
                    next_offset = len(all_results)
                    url_with_offset = f"{url}&offset={next_offset}"
                    curl_command = [
                        'curl',
                        '--request', 'GET',
                        '--url', url_with_offset,
                        '--header', f"Authorization: Bearer {access_token}"
                    ]
                    result = subprocess.run(curl_command, capture_output=True, text=True, check=True, encoding='utf-8')
                    if result.stdout:
                        search_results = json.loads(result.stdout)
                    else:
                        print(f'A saída do subprocesso está vazia. Verifique a consulta.')
                        break
            else:  # Se não for 'artist', apenas salve os resultados sem buscar itens
                if 'album' in item_types.split(','):
                    all_results.extend(search_results.get('albums', {}).get('items', []))
                if 'track' in item_types.split(','):
                    all_results.extend(search_results.get('tracks', {}).get('items', []))
                if 'playlist' in item_types.split(','):
                    all_results.extend(search_results.get('playlists', {}).get('items', []))
                if 'show' in item_types.split(','):
                    all_results.extend(search_results.get('shows', {}).get('items', []))
                if 'episode' in item_types.split(','):
                    while len(all_results) < total_results:
                        items = search_results.get('episodes', {}).get('items', [])
                        all_results.extend(items)
                        if len(all_results) >= total_results:
                            break
                        next_offset = len(all_results)
                        url_with_offset = f"{url}&offset={next_offset}"
                        curl_command = [
                            'curl',
                            '--request', 'GET',
                            '--url', url_with_offset,
                            '--header', f"Authorization: Bearer {access_token}"
                        ]
                        result = subprocess.run(curl_command, capture_output=True, text=True, check=True, encoding='utf-8')
                        if result.stdout:
                            search_results = json.loads(result.stdout)
                        else:
                            print(f'A saída do subprocesso está vazia. Verifique a consulta.')
                            break
                if 'audiobook' in item_types.split(','):
                    all_results.extend(search_results.get('audiobooks', {}).get('items', []))

        except (json.JSONDecodeError, AttributeError) as e:
            print(f'Erro ao decodificar ou processar os resultados da API: {e}')
            return

    else:
        print(f'A saída do subprocesso está vazia. Verifique a consulta.')
        return

    # Salvar resultados no arquivo com nome padrão
    file_name = f"search_results_{query}.txt"
    file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), file_name)

    with open(file_path, 'w', encoding='utf-8') as file:
        json.dump(all_results, file, indent=4, ensure_ascii=False)

    print(f"Resultados da Pesquisa foram salvos em {file_path}")

    # Inserir dados no banco de dados
    if 'artist' in item_types.split(','):
        insert_to_db(all_results)
    if 'track' in item_types:
        insert_track_data(all_results)





def insert_to_db(search_results):
    try:
        connection = connect_db()
        if connection:
            cursor = connection.cursor()
            datacriacao = datetime.now()  # Get the current timestamp
            for item in search_results:
                if 'id' in item:
                    spotify_id = item['id']

                    # Verificar se o spotify_id já existe no banco de dados
                    cursor.execute('SELECT spotify_id FROM artistid WHERE spotify_id = %s', (spotify_id,))
                    existing_id = cursor.fetchone()

                    if existing_id:
                        print(f'Spotify ID {spotify_id} já existe no banco de dados. Pulando inserção.')
                    else:
                        # Inserir o spotify_id no banco de dados
                        try:
                            cursor.execute(
                                'INSERT INTO artistid (spotify_id, datacriacao) VALUES (%s, %s) ON CONFLICT (spotify_id) DO NOTHING',
                                (spotify_id, datacriacao)
                            )
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
