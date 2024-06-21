import subprocess
import json

# Credenciais da API do Spotify
CLIENT_ID = '76b6ccdf37334e00bd2d36cb5d8bf4ca'
CLIENT_SECRET = '29eab5b3e6e446d5904d46be3c305866'
# BQAz7PqSqnrQD3_SbkRcTijp0eTHlq48E6R50vSqAa4x7ZfIkXm0wjDFl7lhyOe0v0ANFlSPq3tvKBLJvNR5sBvg544d_Sz9zw6mygITRNFTeZYJ9OM
# Comando curl para obter o token de acesso
curl_command = [
    'curl',
    '-X', 'POST',
    'https://accounts.spotify.com/api/token',
    '-H', 'Content-Type: application/x-www-form-urlencoded',
    '-d', f'grant_type=client_credentials&client_id={CLIENT_ID}&client_secret={CLIENT_SECRET}'
]

# Executa o comando curl
result = subprocess.run(curl_command, capture_output=True, text=True)

# Verifica se a requisição foi bem-sucedida
if result.returncode == 0:
    token_response = json.loads(result.stdout)
    access_token = token_response.get('access_token')
    if access_token:
        print(f'Token de acesso: {access_token}')
    else:
        print('Erro ao obter o token de acesso:', token_response)
else:
    print(f'Erro ao chamar a API do Spotify: {result.stderr}')
