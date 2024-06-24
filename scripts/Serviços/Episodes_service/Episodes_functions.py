import subprocess
import json

# Função para obter informações de um episódio
def get_episode_info(access_token, episode_id):
    curl_command = [
        'curl',
        '-X', 'GET',
        f'https://api.spotify.com/v1/episodes/{episode_id}',
        '-H', f'Authorization: Bearer {access_token}'
    ]
    print(curl_command)
    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        episode_data = json.loads(result.stdout)
        print(json.dumps(episode_data, indent=4))
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')
