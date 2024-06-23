# ENDPOINT
# https://api.spotify.com/v1/audiobooks/{id}
import subprocess
import json

# Função para obter informações de um audiobooks
def get_album_info(access_token, audiobooks_id):
    curl_command = [
        'curl',
        '-X', 'GET',
        f'https://api.spotify.com/v1/audiobooks/{id}',
        '-H', f'Authorization: Bearer {access_token}'
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        audiobooks_data = json.loads(result.stdout)
        print(json.dumps(audiobooks_data, indent=4))
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')