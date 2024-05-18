import subprocess
import json
import os

# Função para ler o conteúdo de um arquivo
def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f'Erro ao ler o arquivo {file_path}: {e}')
        return None

# Função para obter o Client ID e Client Secret dos arquivos
def get_credentials():
    script_dir = os.path.dirname(os.path.abspath(__file__))  # Diretório do script
    ids_dir = os.path.join(script_dir, 'IDs')  # Caminho para a pasta IDs

    client_id_path = os.path.join(ids_dir, 'client_id.txt')
    client_secret_path = os.path.join(ids_dir, 'client_secret.txt')

    client_id = read_file(client_id_path)
    client_secret = read_file(client_secret_path)

    if client_id is None or client_secret is None:
        print('Erro ao obter as credenciais. Verifique se os arquivos de credenciais existem e estão corretos.')
        exit(1)

    return client_id, client_secret

# Função para obter o token de acesso
def get_access_token(client_id, client_secret):
    curl_command = [
        'curl',
        '-X', 'POST',
        'https://accounts.spotify.com/api/token',
        '-H', 'Content-Type: application/x-www-form-urlencoded',
        '-d', f'grant_type=client_credentials&client_id={client_id}&client_secret={client_secret}'
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        token_response = json.loads(result.stdout)
        access_token = token_response.get('access_token')
        if access_token:
            print(f'Token de acesso: {access_token}')
            return access_token
        else:
            print('Erro ao obter o token de acesso:', token_response)
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')
    return None

# Função para obter informações de um artista
def get_artist_info(access_token):
    curl_command = [
        'curl',
        '-X', 'GET',
        f'https://api.spotify.com/v1/artists',
        '-H', f'Authorization: Bearer {access_token}'
    ]

    result = subprocess.run(curl_command, capture_output=True, text=True)

    if result.returncode == 0:
        artist_data = json.loads(result.stdout)
        print(json.dumps(artist_data, indent=4))
    else:
        print(f'Erro ao chamar a API do Spotify: {result.stderr}')

# Função principal que exibe o menu
def main():
    client_id, client_secret = get_credentials()
    access_token = None

    while True:
        print("\nMenu:")
        print("1. Obter Token de Acesso")
        print("2. Buscar Informações de um Artista")
        print("3. Sair")

        choice = input("Escolha uma opção: ")

        if choice == '1':
            access_token = get_access_token(client_id, client_secret)
        elif choice == '2':
            if access_token is None:
                print("Você precisa obter o token de acesso primeiro (opção 1).")
            else:
                artist_id = input("Digite o ID do artista: ")
                get_artist_info(access_token)
        elif choice == '3':
            print("Saindo...")
            break
        else:
            print("Opção inválida, por favor tente novamente.")

if __name__ == '__main__':
    main()
