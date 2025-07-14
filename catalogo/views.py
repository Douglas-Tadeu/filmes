from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Avg
from .models import Filme, Usuario, Favorito, Avaliacao
from .forms import AvaliacaoForm, RegistroForm
from django.contrib.auth.models import User
from django.db import models

def home(request):
    filmes = Filme.objects.annotate(media_avaliacao=Avg('avaliacoes__nota'))  # <-- corrigido aqui

    favoritos = []

    if request.user.is_authenticated:
        usuario, _ = Usuario.objects.get_or_create(user=request.user)
        favoritos = Favorito.objects.filter(usuario=usuario).values_list('filme_id', flat=True)

        for filme in filmes:
            filme.ja_favorito = filme.id in favoritos
            filme.media_avaliacao = filme.media_avaliacao or 0
    else:
        for filme in filmes:
            filme.ja_favorito = False
            filme.media_avaliacao = filme.media_avaliacao or 0

    return render(request, 'catalogo/home.html', {'filmes': filmes})


def detalhe_filme(request, filme_id):
    filme = get_object_or_404(Filme, id=filme_id)

    media_avaliacao = Avaliacao.objects.filter(filme=filme).aggregate(avg_nota=models.Avg('nota'))['avg_nota'] or 0
    qtd_favoritos = Favorito.objects.filter(filme=filme).count()

    ja_favorito = False
    avaliacao_existente = None
    form = AvaliacaoForm()

    if request.user.is_authenticated:
        usuario = Usuario.objects.get(user=request.user)
        ja_favorito = Favorito.objects.filter(filme=filme, usuario=usuario).exists()
        avaliacao_existente = Avaliacao.objects.filter(filme=filme, usuario=usuario).first()

        if request.method == 'POST':
            form = AvaliacaoForm(request.POST, instance=avaliacao_existente)
            if form.is_valid():
                avaliacao = form.save(commit=False)
                avaliacao.filme = filme
                avaliacao.usuario = usuario
                avaliacao.save()
                return redirect('detalhe_filme', filme_id=filme.id)
        else:
            form = AvaliacaoForm(instance=avaliacao_existente)

    context = {
        'filme': filme,
        'media_avaliacao': media_avaliacao,
        'qtd_favoritos': qtd_favoritos,
        'ja_favorito': ja_favorito,
        'form': form,
        # lembre de passar as avaliações se quiser listar no template
        'avaliacoes': Avaliacao.objects.filter(filme=filme).select_related('usuario'),
    }
    return render(request, 'catalogo/detalhe_filme.html', context)

def lista_filmes(request):
    filmes = Filme.objects.annotate(media_avaliacao=Avg('avaliacoes__nota'))

    favoritos = []
    if request.user.is_authenticated:
        usuario, _ = Usuario.objects.get_or_create(user=request.user)
        favoritos = Favorito.objects.filter(usuario=usuario).values_list('filme_id', flat=True)

    for filme in filmes:
        filme.ja_favorito = filme.id in favoritos
        filme.media_avaliacao = filme.media_avaliacao or 0

    return render(request, 'catalogo/home.html', {'filmes': filmes})

@login_required
def toggle_favorito(request, filme_id):
    filme = get_object_or_404(Filme, id=filme_id)
    usuario = get_object_or_404(Usuario, user=request.user)
    favorito_qs = Favorito.objects.filter(usuario=usuario, filme=filme)

    if favorito_qs.exists():
        favorito_qs.delete()
    else:
        Favorito.objects.create(usuario=usuario, filme=filme)

    return redirect('detalhe_filme', filme_id=filme.id)

def register(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            Usuario.objects.create(user=user)  # cria perfil do usuário
            login(request, user)
            return redirect('home')
    else:
        form = RegistroForm()
    return render(request, 'catalogo/register.html', {'form': form})

@login_required
def favoritos(request):
    usuario = Usuario.objects.get(user=request.user)
    favoritos = Favorito.objects.filter(usuario=usuario).select_related('filme')
    return render(request, 'catalogo/favoritos.html', {'favoritos': favoritos})
