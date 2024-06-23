# ENDPOINT
# https://api.spotify.com/v1/browse/categories


# Examples of ISO 639-1 codes
# Code	English	French	German	Endonym
# en	English	anglais	Englisch	English
# es	Spanish	espagnol	Spanisch	español
# pt	Portuguese	portugais	Portugiesisch	português


import subprocess
import json

# Função para obter informações de uma categoria
def get_categories_info(access_token, categories_id):
    curl_command = [
        'curl',
        '-X', 'GET',
        f'https://api.spotify.com/v1/browse/categories',
        '-H', f'Authorization: Bearer {access_token}'
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        categories_data = json.loads(result.stdout)
        print(json.dumps(categories_data, indent=4))
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')