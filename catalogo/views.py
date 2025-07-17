from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Avg
from .models import Filme, Usuario, Favorito, Avaliacao, Genero, Diretor
from .forms import AvaliacaoForm, RegistroForm, FilmeForm, GeneroForm, DiretorForm


def home(request):
    filmes = Filme.objects.annotate(media_avaliacao=Avg('avaliacoes__nota'))

    favoritos = []
    if request.user.is_authenticated:
        usuario, _ = Usuario.objects.get_or_create(user=request.user)
        favoritos = Favorito.objects.filter(usuario=usuario).values_list('filme_id', flat=True)

    for filme in filmes:
        filme.ja_favorito = filme.id in favoritos
        filme.media_avaliacao = filme.media_avaliacao or 0

    return render(request, 'catalogo/home.html', {'filmes': filmes})


def lista_filmes(request):
    filmes = Filme.objects.annotate(media_avaliacao=Avg('avaliacoes__nota'))

    favoritos = []
    if request.user.is_authenticated:
        usuario, _ = Usuario.objects.get_or_create(user=request.user)
        favoritos = Favorito.objects.filter(usuario=usuario).values_list('filme_id', flat=True)

    for filme in filmes:
        filme.ja_favorito = filme.id in favoritos
        filme.media_avaliacao = filme.media_avaliacao or 0

    return render(request, 'catalogo/filme/list.html', {'filmes': filmes})


def criar_filme(request):
    if request.method == 'POST':
        form = FilmeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_filmes')
    else:
        form = FilmeForm()
    return render(request, 'catalogo/filme/form.html', {'form': form})


def editar_filme(request, pk):
    filme = get_object_or_404(Filme, pk=pk)
    if request.method == 'POST':
        form = FilmeForm(request.POST, instance=filme)
        if form.is_valid():
            form.save()
            return redirect('lista_filmes')
    else:
        form = FilmeForm(instance=filme)
    return render(request, 'catalogo/filme/form.html', {'form': form})


def excluir_filme(request, pk):
    filme = get_object_or_404(Filme, pk=pk)
    if request.method == 'POST':
        filme.delete()
        return redirect('lista_filmes')
    return render(request, 'catalogo/filme/confirm_delete.html', {'filme': filme})


def detalhe_filme(request, filme_id):
    filme = get_object_or_404(Filme, id=filme_id)

    media_avaliacao = Avaliacao.objects.filter(filme=filme).aggregate(avg_nota=Avg('nota'))['avg_nota'] or 0
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
        'avaliacoes': Avaliacao.objects.filter(filme=filme).select_related('usuario'),
    }
    return render(request, 'catalogo/detalhe_filme.html', context)

def listar_generos(request):
    generos = Genero.objects.all()
    return render(request, 'catalogo/genero/lista.html', {'generos': generos})

def criar_genero(request):
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_generos')
    else:
        form = GeneroForm()
    return render(request, 'catalogo/genero/form.html', {'form': form, 'acao': 'Criar'})

def editar_genero(request, genero_id):
    genero = get_object_or_404(Genero, id=genero_id)
    if request.method == 'POST':
        form = GeneroForm(request.POST, instance=genero)
        if form.is_valid():
            form.save()
            return redirect('lista_generos')
    else:
        form = GeneroForm(instance=genero)
    return render(request, 'catalogo/genero/form.html', {'form': form, 'acao': 'Editar'})

def deletar_genero(request, genero_id):
    genero = get_object_or_404(Genero, id=genero_id)
    if request.method == 'POST':
        genero.delete()
        return redirect('lista_generos')
    return render(request, 'catalogo/genero/confirmar_delete.html', {'genero': genero})

def listar_diretores(request):
    diretores = Diretor.objects.all()
    return render(request, 'catalogo/diretor/listar.html', {'diretores': diretores})

def adicionar_diretor(request):
    if request.method == 'POST':
        form = DiretorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_diretores')
    else:
        form = DiretorForm()
    return render(request, 'catalogo/diretor/form.html', {'form': form, 'titulo': 'Adicionar Diretor'})

def editar_diretor(request, pk):
    diretor = get_object_or_404(Diretor, pk=pk)
    if request.method == 'POST':
        form = DiretorForm(request.POST, instance=diretor)
        if form.is_valid():
            form.save()
            return redirect('listar_diretores')
    else:
        form = DiretorForm(instance=diretor)
    return render(request, 'catalogo/diretor/form.html', {'form': form, 'titulo': 'Editar Diretor'})

def excluir_diretor(request, diretor_id):
    diretor = get_object_or_404(Diretor, pk=diretor_id)
    if request.method == 'POST':
        diretor.delete()
        return redirect('listar_diretores')
    return render(request, 'catalogo/diretor/confirmar_exclusao.html', {'diretor': diretor})

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
            Usuario.objects.create(user=user)
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
