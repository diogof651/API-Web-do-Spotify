# ENDPOINT
# https://api.spotify.com/v1/playlists/{playlist_id}

import subprocess
import json

# Função para obter informações de um artista
def get_playlist_id(access_token, playlist_id):
    curl_command = [
        'curl',
        '-X', 'GET',
        f'https://api.spotify.com/v1/playlists/{playlist_id}',
        '-H', f'Authorization: Bearer {access_token}'
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        artist_data = json.loads(result.stdout)
        print(json.dumps(artist_data, indent=4))
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')

    
