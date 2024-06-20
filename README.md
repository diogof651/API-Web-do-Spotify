# Spotify API Database Integration

## Descrição do Projeto

Este projeto foi desenvolvido como parte de um trabalho prático para a disciplina de Laboratório de Banco de Dados na Universidade Federal de Mato Grosso do Sul. O objetivo é realizar a engenharia reversa do banco de dados da API Web do Spotify, carregando dados obtidos da API em um banco de dados relacional PostgreSQL. O projeto inclui a criação de um script/programa que realiza a importação dos dados e a construção de um diagrama ER/EER para descrever o banco de dados.

## Integrantes do Grupo

- Diogo Felipe - Téc. em Análise e Desenvolvimento de Sistemas - UFMS

## Tecnologias Utilizadas

- PostgreSQL 12+
- Python 3.8+
- Biblioteca Requests para Python
- JSON
- Ferramenta CURL

## Estrutura do Projeto

- `diagram/`: Contém o diagrama ER/EER em formato PDF.
- `scripts/`: Contém o script/programa para importar os dados da API para o banco de dados PostgreSQL.
- `scripts/IDs`: Contém os IDs únicos de cada usuário. 
- `database/`: Contém o dump do banco de dados (.sql) com dados e estrutura.
- `README.md`: Este arquivo, contendo instruções detalhadas sobre o projeto.

   - `project_folder/`
   -   `│`
   -   `├── script/`
   -   `│   ├── menu.py`
   -   `│   ├── import_data.py`
   -   `│   └── IDs/`
   -   `│       ├── client_id.txt`
   -   `│       └── client_secret.txt`
   -   `└── database/`
   -   `    ├── schema.sql`
   -   `    └── db_config.py`
   -   `└── diagram/`
   -   `    └── diagram.png`

## Pré-requisitos

1. **Conta Spotify**: Você precisará de uma conta Spotify para interagir com a API.
2. **Token de Acesso**: Gere um Access Token seguindo as instruções [aqui](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#request-an-access-token).

## Configuração do Ambiente

1. **Clone o Repositório**
    ```bash
    git clone https://github.com/diogof651/API-Web-do-Spotify.git
    cd API-Web-do-Spotify
    ```

2. **Instale as Dependências**
    - Python: Instale as bibliotecas necessárias
    ```bash
    pip install requests
    ```

3. **Configurar PostgreSQL**
    - Certifique-se de ter o PostgreSQL 12 ou superior instalado.
    - Crie um banco de dados para o projeto.
    ```sql
    CREATE DATABASE spotify_db;
    ```

## Executando o Script de Importação

1. **Obtenha o Access Token**
    - Siga as instruções fornecidas [aqui](https://developer.spotify.com/documentation/web-api/tutorials/getting-started#request-an-access-token) para obter um Access Token válido.

2. **Edite o Script com Suas Credenciais**
    - Abra o arquivo `scripts/import_data.py` e insira o Access Token obtido.

3. **Execute o Script**
    ```bash
    python scripts/import_data.py
    ```

## Estrutura do Banco de Dados

O banco de dados é composto pelas seguintes tabelas principais:
- **Album**: Informações sobre os álbuns.
- **Artist**: Informações sobre os artistas.
- **Track**: Informações sobre as faixas.
- **Playlist**: Informações sobre as playlists.
- **User**: Informações sobre os usuários.

Cada tabela é projetada para refletir a nomenclatura e estrutura dos dados retornados pela API do Spotify.

## Dump do Banco de Dados

O dump do banco de dados, contendo a estrutura e os dados, pode ser encontrado no diretório `database/` e pode ser importado para o PostgreSQL com o seguinte comando:
```bash
psql -U seu_usuario -d spotify_db -f database/dump.sql
