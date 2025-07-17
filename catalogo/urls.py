from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.lista_filmes, name='home'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('filme/<int:filme_id>/', views.detalhe_filme, name='detalhe_filme'),
    path('filme/<int:filme_id>/favoritar/', views.toggle_favorito, name='toggle_favorito'),
    path('login/', auth_views.LoginView.as_view(template_name='catalogo/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),

    # CRUD de Filme
    path('filmes/', views.lista_filmes, name='lista_filmes'),
    path('filmes/novo/', views.criar_filme, name='criar_filme'),
    path('filmes/<int:pk>/editar/', views.editar_filme, name='editar_filme'),
    path('filmes/<int:pk>/excluir/', views.excluir_filme, name='excluir_filme'),

    # Gênero
    path('generos/', views.listar_generos, name='listar_generos'),
    path('generos/novo/', views.criar_genero, name='criar_genero'),
    path('generos/<int:pk>/editar/', views.editar_genero, name='editar_genero'),
    path('generos/<int:pk>/excluir/', views.deletar_genero, name='deletar_genero'),

    # Diretor
    path('diretores/', views.listar_diretores, name='listar_diretores'),
    path('diretores/novo/', views.adicionar_diretor, name='adicionar_diretor'),
    path('diretores/<int:pk>/editar/', views.editar_diretor, name='editar_diretor'),
    path('diretores/<int:pk>/excluir/', views.excluir_diretor, name='excluir_diretor'),
]
