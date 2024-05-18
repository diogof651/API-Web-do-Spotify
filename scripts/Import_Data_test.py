import subprocess
import json

# Token de acesso do Spotify
SPOTIFY_TOKEN = 'BQAz7PqSqnrQD3_SbkRcTijp0eTHlq48E6R50vSqAa4x7ZfIkXm0wjDFl7lhyOe0v0ANFlSPq3tvKBLJvNR5sBvg544d_Sz9zw6mygITRNFTeZYJ9OM'

# ID do artista que você deseja consultar
ARTIST_ID = '1dfeR4HaWDbWqFHLkxsg1d'  # Exemplo: ID do Queen

# Comando curl para obter informações sobre o artista
curl_command = [
    'curl',
    '-X', 'GET',
    f'https://api.spotify.com/v1/artists/{ARTIST_ID}',
    '-H', f'Authorization: Bearer {SPOTIFY_TOKEN}'
]

# Executa o comando curl
result = subprocess.run(curl_command, capture_output=True, text=True)

# Verifica se a requisição foi bem-sucedida
if result.returncode == 0:
    artist_data = json.loads(result.stdout)
    print(json.dumps(artist_data, indent=4))
else:
    print(f'Erro ao chamar a API do Spotify: {result.stderr}')
