import subprocess
import json

# Função para obter informações de mercados
def get_markets_info(access_token):
    curl_command = [
        'curl',
        '-X', 'GET',
        'https://api.spotify.com/v1/markets',
        '-H', f'Authorization: Bearer {access_token}'
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        markets_data = json.loads(result.stdout)
        print(json.dumps(markets_data, indent=4))
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')
