from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.db.models import Avg
from .models import Filme, Usuario, Favorito, Avaliacao, Genero, Diretor, Ator, Elenco, Trailer, Classificacao
from .forms import AvaliacaoForm, RegistroForm, FilmeForm, GeneroForm, DiretorForm, AtorForm, ElencoForm, TrailerForm, ClassificacaoForm, FavoritoForm


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
    return render(request, 'catalogo/genero/listar.html', {'generos': generos})

@login_required
def criar_genero(request):
    if request.method == 'POST':
        form = GeneroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_generos')
    else:
        form = GeneroForm()
    return render(request, 'catalogo/genero/form.html', {'form': form})

@login_required
def editar_genero(request, genero_id):
    genero = get_object_or_404(Genero, id=genero_id)
    if request.method == 'POST':
        form = GeneroForm(request.POST, instance=genero)
        if form.is_valid():
            form.save()
            return redirect('listar_generos')
    else:
        form = GeneroForm(instance=genero)
    return render(request, 'catalogo/genero/form.html', {'form': form})

@login_required
def deletar_genero(request, genero_id):
    genero = get_object_or_404(Genero, id=genero_id)
    if request.method == 'POST':
        genero.delete()
        return redirect('listar_generos')
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

def excluir_diretor(request, pk):
    diretor = get_object_or_404(Diretor, pk=pk)
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
def listar_avaliacoes(request):
    avaliacoes = Avaliacao.objects.all()
    return render(request, 'catalogo/avaliacao/lista.html', {'avaliacoes': avaliacoes})

@login_required
def criar_avaliacao(request, filme_id):
    filme = get_object_or_404(Filme, id=filme_id)
    usuario = Usuario.objects.get(user=request.user)

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST)
        if form.is_valid():
            avaliacao = form.save(commit=False)
            avaliacao.filme = filme
            avaliacao.usuario = usuario
            avaliacao.save()
            return redirect('detalhe_filme', filme_id=filme.id)
    else:
        form = AvaliacaoForm()
    return render(request, 'catalogo/avaliacao/form.html', {'form': form, 'filme': filme})

@login_required
def editar_avaliacao(request, avaliacao_id):
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id, usuario__user=request.user)

    if request.method == 'POST':
        form = AvaliacaoForm(request.POST, instance=avaliacao)
        if form.is_valid():
            form.save()
            return redirect('detalhe_filme', filme_id=avaliacao.filme.id)
    else:
        form = AvaliacaoForm(instance=avaliacao)

    return render(request, 'catalogo/avaliacao/form.html', {'form': form, 'acao': 'Editar Avaliação'})


@login_required
def excluir_avaliacao(request, avaliacao_id):
    avaliacao = get_object_or_404(Avaliacao, id=avaliacao_id, usuario__user=request.user)

    if request.method == 'POST':
        filme_id = avaliacao.filme.id
        avaliacao.delete()
        return redirect('detalhe_filme', filme_id=filme_id)

    return render(request, 'catalogo/avaliacao/confirmar_delete.html', {'avaliacao': avaliacao})

def listar_atores(request):
    atores = Ator.objects.all()
    return render(request, 'catalogo/atores/listar_atores.html', {'atores': atores})

def criar_ator(request):
    if request.method == 'POST':
        form = AtorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_atores')
    else:
        form = AtorForm()
    return render(request, 'catalogo/atores/form_ator.html', {'form': form, 'titulo': 'Novo Ator'})

def editar_ator(request, id):
    ator = get_object_or_404(Ator, pk=id)
    if request.method == 'POST':
        form = AtorForm(request.POST, instance=ator)
        if form.is_valid():
            form.save()
            return redirect('listar_atores')
    else:
        form = AtorForm(instance=ator)
    return render(request, 'catalogo/atores/form_ator.html', {'form': form, 'titulo': 'Editar Ator'})

def excluir_ator(request, id):
    ator = get_object_or_404(Ator, pk=id)
    if request.method == 'POST':
        ator.delete()
        return redirect('listar_atores')
    return render(request, 'catalogo/atores/confirma_exclusao.html', {'ator': ator})

def listar_elencos(request):
    elencos = Elenco.objects.all()
    return render(request, 'catalogo/elenco/listar.html', {'elencos': elencos})

def criar_elenco(request):
    if request.method == 'POST':
        form = ElencoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_elencos')
    else:
        form = ElencoForm()
    return render(request, 'catalogo/elenco/form.html', {'form': form})

def editar_elenco(request, pk):
    elenco = get_object_or_404(Elenco, pk=pk)
    if request.method == 'POST':
        form = ElencoForm(request.POST, instance=elenco)
        if form.is_valid():
            form.save()
            return redirect('listar_elencos')
    else:
        form = ElencoForm(instance=elenco)
    return render(request, 'catalogo/elenco/form.html', {'form': form})

def deletar_elenco(request, pk):
    elenco = get_object_or_404(Elenco, pk=pk)
    if request.method == 'POST':
        elenco.delete()
        return redirect('listar_elencos')
    return render(request, 'catalogo/elenco/confirmar_delete.html', {'elenco': elenco})

@login_required
def listar_trailers(request):
    trailers = Trailer.objects.all()
    return render(request, 'catalogo/trailer/listar.html', {'trailers': trailers})

@login_required
def criar_trailer(request):
    if request.method == 'POST':
        form = TrailerForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_trailers')
    else:
        form = TrailerForm()
    return render(request, 'catalogo/trailer/form.html', {'form': form})

@login_required
def editar_trailer(request, pk):
    trailer = get_object_or_404(Trailer, pk=pk)
    if request.method == 'POST':
        form = TrailerForm(request.POST, instance=trailer)
        if form.is_valid():
            form.save()
            return redirect('listar_trailers')
    else:
        form = TrailerForm(instance=trailer)
    return render(request, 'catalogo/trailer/form.html', {'form': form})

@login_required
def deletar_trailer(request, pk):
    trailer = get_object_or_404(Trailer, pk=pk)
    if request.method == 'POST':
        trailer.delete()
        return redirect('listar_trailers')
    return render(request, 'catalogo/trailer/confirmar_delete.html', {'trailer': trailer})

def listar_classificacoes(request):
    classificacoes = Classificacao.objects.all()
    return render(request, 'catalogo/classificacao/listar.html', {'classificacoes': classificacoes})

def criar_classificacao(request):
    if request.method == 'POST':
        form = ClassificacaoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('listar_classificacoes')
    else:
        form = ClassificacaoForm()
    return render(request, 'catalogo/classificacao/form.html', {'form': form})

def editar_classificacao(request, pk):
    classificacao = get_object_or_404(Classificacao, pk=pk)
    if request.method == 'POST':
        form = ClassificacaoForm(request.POST, instance=classificacao)
        if form.is_valid():
            form.save()
            return redirect('listar_classificacoes')
    else:
        form = ClassificacaoForm(instance=classificacao)
    return render(request, 'catalogo/classificacao/form.html', {'form': form})

def deletar_classificacao(request, pk):
    classificacao = get_object_or_404(Classificacao, pk=pk)
    if request.method == 'POST':
        classificacao.delete()
        return redirect('listar_classificacoes')
    return render(request, 'catalogo/classificacao/confirmar_delete.html', {'classificacao': classificacao})

@login_required
def listar_favoritos(request):
    usuario = get_object_or_404(Usuario, user=request.user)
    favoritos = Favorito.objects.filter(usuario=usuario)
    return render(request, 'catalogo/favorito/listar.html', {'favoritos': favoritos})

@login_required
def adicionar_favorito(request):
    if request.method == 'POST':
        form = FavoritoForm(request.POST)
        if form.is_valid():
            favorito = form.save(commit=False)
            favorito.usuario = Usuario.objects.get(user=request.user)
            favorito.save()
            return redirect('listar_favoritos')
    else:
        form = FavoritoForm()
    return render(request, 'catalogo/favorito/form.html', {'form': form})

@login_required
def excluir_favorito(request, pk):
    usuario = Usuario.objects.get(user=request.user)
    favorito = get_object_or_404(Favorito, pk=pk, usuario=usuario)
    
    if request.method == 'POST':
        favorito.delete()
        return redirect('listar_favoritos')  # ou outra URL que você queira
    
    # Se for GET, mostrar a página de confirmação
    return render(request, 'catalogo/favorito/confirmar_exclusao.html', {'favorito': favorito})

@login_required
def dashboard(request):
    usuario = Usuario.objects.get(user=request.user)
    filmes = Filme.objects.all()
    avaliacoes_qs = Avaliacao.objects.filter(usuario=usuario)

    # Criar um dicionário filme_id -> nota
    avaliacoes_dict = {avaliacao.filme.id: avaliacao.nota for avaliacao in avaliacoes_qs}

    # Adicionar atributo 'avaliacao' em cada filme para facilitar no template
    for filme in filmes:
        filme.avaliacao = avaliacoes_dict.get(filme.id, "-")

    context = {
        'filmes': filmes,
        # já não precisa enviar avaliacoes_dict pro template
    }
    return render(request, 'catalogo/dashboard.html', context)

@login_required
def criar_avaliacao_dashboard(request):
    if request.method == 'POST':
        usuario = Usuario.objects.get(user=request.user)
        filme_id = request.POST.get('filme_id')
        nota = request.POST.get('nota')

        try:
            filme = Filme.objects.get(id=filme_id)
            nota = int(nota)
            if nota < 1 or nota > 5:
                raise ValueError()
        except (Filme.DoesNotExist, ValueError):
            messages.error(request, "Dados inválidos.")
            return redirect('dashboard')

        Avaliacao.objects.update_or_create(
            usuario=usuario,
            filme=filme,
            defaults={'nota': nota}
        )

        messages.success(request, f'Avaliação salva para "{filme.titulo}".')
    return redirect('dashboard')

def raiz(request):
    return redirect('dashboard')