from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    #path('filmes/<int:filme_id>/avaliar/', views.avaliar_filme, name='avaliar_filme'),
    path('avaliacoes/dashboard/criar/', views.criar_avaliacao_dashboard, name='criar_avaliacao_dashboard'),
    path('favoritos/', views.listar_favoritos, name='listar_favoritos'),
    path('filme/<int:filme_id>/', views.detalhe_filme, name='detalhe_filme'),
    path('filme/<int:filme_id>/favoritar/', views.toggle_favorito, name='toggle_favorito'),
    path('login/', auth_views.LoginView.as_view(template_name='catalogo/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('dashboard/avaliar/', views.criar_avaliacao_dashboard, name='criar_avaliacao_dashboard'),

    # CRUD de Filme
    path('filmes/', views.lista_filmes, name='lista_filmes'),
    path('filmes/novo/', views.criar_filme, name='criar_filme'),
    path('filmes/<int:pk>/editar/', views.editar_filme, name='editar_filme'),
    path('filmes/<int:pk>/excluir/', views.excluir_filme, name='excluir_filme'),

    # CRUD de Gênero
    path('generos/', views.listar_generos, name='listar_generos'),
    path('generos/criar/', views.criar_genero, name='criar_genero'),
    path('generos/editar/<int:genero_id>/', views.editar_genero, name='editar_genero'),
    path('generos/deletar/<int:genero_id>/', views.deletar_genero, name='deletar_genero'),

    # CRUD de Diretor
    path('diretores/', views.listar_diretores, name='listar_diretores'),
    path('diretores/novo/', views.adicionar_diretor, name='adicionar_diretor'),
    path('diretores/<int:pk>/editar/', views.editar_diretor, name='editar_diretor'),
    path('diretores/<int:pk>/excluir/', views.excluir_diretor, name='excluir_diretor'),

    # CRUD de Avaliações
    path('avaliacoes/', views.listar_avaliacoes, name='listar_avaliacoes'),
    path('avaliacoes/dashboard/criar/', views.criar_avaliacao_dashboard, name='criar_avaliacao_dashboard'),
    path('avaliacoes/novo/<int:filme_id>/', views.criar_avaliacao, name='criar_avaliacao'),
    path('avaliacoes/<int:pk>/editar/', views.editar_avaliacao, name='editar_avaliacao'),
    path('avaliacao/<int:avaliacao_id>/excluir/', views.excluir_avaliacao, name='excluir_avaliacao'), 

    # CRUD de Atores
    path('atores/', views.listar_atores, name='listar_atores'),
    path('atores/novo/', views.criar_ator, name='criar_ator'),
    path('atores/<int:id>/editar/', views.editar_ator, name='editar_ator'),
    path('atores/<int:id>/excluir/', views.excluir_ator, name='excluir_ator'),

    # CRUD de Elenco
    path('elencos/', views.listar_elencos, name='listar_elencos'),
    path('elencos/novo/', views.criar_elenco, name='criar_elenco'),
    path('elencos/<int:pk>/editar/', views.editar_elenco, name='editar_elenco'),
    path('elencos/<int:pk>/deletar/', views.deletar_elenco, name='deletar_elenco'),

    # CRUD de Trailer
    path('trailers/', views.listar_trailers, name='listar_trailers'),
    path('trailers/novo/', views.criar_trailer, name='criar_trailer'),
    path('trailers/<int:pk>/editar/', views.editar_trailer, name='editar_trailer'),
    path('trailers/<int:pk>/deletar/', views.deletar_trailer, name='deletar_trailer'),

    # CRUD de Classificação
    path('classificacoes/', views.listar_classificacoes, name='listar_classificacoes'),
    path('classificacoes/criar/', views.criar_classificacao, name='criar_classificacao'),
    path('classificacoes/<int:pk>/editar/', views.editar_classificacao, name='editar_classificacao'),
    path('classificacoes/<int:pk>/deletar/', views.deletar_classificacao, name='deletar_classificacao'),

    # CRUD de Favorito
    path('favoritos/', views.listar_favoritos, name='listar_favoritos'),
    path('favoritos/novo/', views.adicionar_favorito, name='adicionar_favorito'),
    path('favoritos/<int:pk>/excluir/', views.excluir_favorito, name='excluir_favorito'),
]
