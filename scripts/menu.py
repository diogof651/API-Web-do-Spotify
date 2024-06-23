import subprocess
import os
import json
import sys

# Adiciona o caminho do projeto ao sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from scripts.Search.Buscatudo import realizar_pesquisa
from scripts.Serviços.Artistas_service.Artistas_functions import get_artist_info
from database.db_config import create_table
from scripts import import_data
from scripts.Serviços.Genres_service.Genres_functions import get_available_genre_seeds

def read_file(file_path):
    try:
        with open(file_path, 'r') as file:
            return file.read().strip()
    except Exception as e:
        print(f'Erro ao ler o arquivo {file_path}: {e}')
        return None

def get_credentials():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    ids_dir = os.path.join(script_dir, 'IDs')

    client_id_path = os.path.join(ids_dir, 'client_id.txt')
    client_secret_path = os.path.join(ids_dir, 'client_secret.txt')

    client_id = read_file(client_id_path)
    client_secret = read_file(client_secret_path)

    if client_id is None or client_secret is None:
        print('Erro ao obter as credenciais. Verifique se os arquivos de credenciais existem e estão corretos.')
        exit(1)

    return client_id, client_secret

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

def main():
    try:
        create_table()  # Garantir que a tabela exista

        client_id, client_secret = get_credentials()
        access_token = get_access_token(client_id, client_secret)
        
        if access_token is None:
            print("Não foi possível obter o token de acesso. Verifique suas credenciais.")
            return

        while True:
            print("\nMenu:")
            print("1. Obter Token de Acesso")
            print("2. Buscar Informações de um Artista")
            print("3. Buscar Gêneros")            
            print("4. Realizar Pesquisa")

            print("5. Sair")

            try:
                choice = input("Escolha uma opção: ")

                if choice == '1':
                    access_token = get_access_token(client_id, client_secret)
                elif choice == '2':
                    if access_token is None:
                        print("Você precisa obter o token de acesso primeiro (opção 1).")
                    else:
                        artist_id = input("Digite o ID do artista: ")
                        get_artist_info(access_token, artist_id)
                        print("Tabela de Gêneros atualizada no Banco de Dados!")
                elif choice == '3':
                    if access_token is None:
                        print("Você precisa obter o token de acesso primeiro (opção 1).")
                    else:
                        get_available_genre_seeds(access_token)
                elif choice == '4':
                    if access_token is None:
                        print("Você precisa obter o token de acesso primeiro (opção 1).")
                    else:
                        realizar_pesquisa(access_token)
                elif choice == '5':
                    if access_token is None:
                        print("Você precisa obter o token de acesso primeiro (opção 1).")
                    else:
                        realizar_pesquisa(access_token)
                elif choice == '5':
                    print("Saindo...")
                    break
                else:
                    print("Opção inválida, por favor tente novamente.")
            except KeyboardInterrupt:
                print("\nPrograma interrompido pelo usuário. Saindo...")
                break
            except Exception as e:
                print(f"Ocorreu um erro: {e}")
    except Exception as e:
        print(f"Erro ao inicializar o programa: {e}")

if __name__ == '__main__':
    main()
