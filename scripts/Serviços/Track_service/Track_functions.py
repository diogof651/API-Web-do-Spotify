import subprocess
import json

# Função para obter informações de uma faixa
def get_track_info(access_token, track_id):
    curl_command = [
        'curl',
        '-X', 'GET',
        f'https://api.spotify.com/v1/tracks/{track_id}',
        '-H', f'Authorization: Bearer {access_token}'
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        track_data = json.loads(result.stdout)
        print(json.dumps(track_data, indent=4))
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')

