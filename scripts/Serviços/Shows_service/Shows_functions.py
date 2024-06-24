import subprocess
import json

# Função para obter informações de um show
def get_show_info(access_token, show_id):
    curl_command = [
        'curl',
        '-X', 'GET',
        f'https://api.spotify.com/v1/shows/{show_id}',
        '-H', f'Authorization: Bearer {access_token}'
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        show_data = json.loads(result.stdout)
        print(json.dumps(show_data, indent=4))
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')
