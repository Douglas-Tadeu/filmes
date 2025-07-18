## Catálogo de Filmes
Projeto desenvolvido em Django para gerenciar um catálogo de filmes com avaliações, gêneros, diretores, trailers e favoritos.

## Tecnologias utilizadas
Python 3.13
Django 5.2.4
SQLite (banco de dados padrão)
HTML, CSS para modelos
Funcionalidades
Cadastro, edição, exclusão e listagem de filmes, gêneros, diretores, avaliações, trailers e favoritos
Visualização da mídia de avaliação de cada filme
Os usuários podem avaliar e favoritar filmes
Tela do painel para resumo dos dados
Como rodar o projeto
Clonar este repositório:
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


## Frase motivacional (Não sei se é para mim ou para o senhor)
*Se Deus é por nós, quem será contra nozes!*
