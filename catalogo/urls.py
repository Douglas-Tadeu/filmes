from django.urls import path
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    path('', views.lista_filmes, name='home'),
    #path('', views.lista_filmes, name='lista_filmes'),
    path('favoritos/', views.favoritos, name='favoritos'),
    path('filme/<int:filme_id>/', views.detalhe_filme, name='detalhe_filme'),
    path('filme/<int:filme_id>/favoritar/', views.toggle_favorito, name='toggle_favorito'),
    #path('filme/<int:filme_id>/avaliar/', views.avaliar_filme, name='avaliar_filme'),
    path('login/', auth_views.LoginView.as_view(template_name='catalogo/login.html', redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', views.register, name='register'),
]
