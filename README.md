# Catálogo de Filmes

Projeto desenvolvido em Django para gerenciar um catálogo de filmes com avaliações, gêneros, diretores, trailers e favoritos.

## Tecnologias utilizadas

- Python 3.13
- Django 5.2.4
- SQLite (banco de dados padrão)
- HTML, CSS para os templates

## Funcionalidades

- Cadastro, edição, exclusão e listagem de filmes, gêneros, diretores, avaliações, trailers e favoritos
- Visualização da média de avaliações de cada filme
- Usuários podem avaliar e favoritar filmes
- Tela de dashboard para resumo dos dados

## Como rodar o projeto

1. Clone este repositório:

```bash
git clone https://github.com/Douglas-Tadeu/filmes.git
cd filmes

## Crie e ative um ambiente virtual:

python -m venv venv
# Windows
venv\Scripts\activate
# Linux / MacOS
source venv/bin/activate

## Instale as dependências:

pip install -r requirements.txt

## Faça as migrações do banco:

python manage.py migrate

## Execute o servidor de desenvolvimento:

python manage.py runserver

## Acesse no navegador:

http://127.0.0.1:8000/
