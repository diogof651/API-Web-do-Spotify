import subprocess
import json
from database.insert_genres_data import insert_genres_data

# Função para obter os gêneros disponíveis para recomendações
def get_available_genre_seeds(access_token):
    curl_command = [
        'curl',
        '-X', 'GET',
        'https://api.spotify.com/v1/recommendations/available-genre-seeds',
        '-H', f'Authorization: Bearer {access_token}'
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        genre_seeds_data = json.loads(result.stdout)
        print(json.dumps(genre_seeds_data, indent=4))
        genres = genre_seeds_data
#        for genre in genres['genres']:
            #print(genre)
        insert_genres_data(genres)
        return genre_seeds_data
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')
        return None


 