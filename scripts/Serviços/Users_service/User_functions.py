import subprocess
import json

def get_user_info(access_token, user_id):
    curl_command = [
        'curl',
        '-X', 'GET',
        f'https://api.spotify.com/v1/users/{user_id}',
        '-H', f'Authorization: Bearer {access_token}'
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        user_data = json.loads(result.stdout)
        print(json.dumps(user_data, indent=4))
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')