from django.db import models
from django.db.models import Avg
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Genero(models.Model):
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome

class Diretor(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Ator(models.Model):
    nome = models.CharField(max_length=100)
    data_nascimento = models.DateField(null=True, blank=True)

    def __str__(self):
        return self.nome

class Classificacao(models.Model):
    descricao = models.CharField(max_length=50)
    idade_minima = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.descricao} ({self.idade_minima}+)"

class Filme(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    ano = models.PositiveIntegerField(null=True, blank=True)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True)
    diretor = models.ForeignKey(Diretor, on_delete=models.SET_NULL, null=True)
    classificacao = models.ForeignKey(Classificacao, on_delete=models.SET_NULL, null=True)
    trailer = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.titulo

    @property
    def media_avaliacoes(self):
        media = self.avaliacoes.aggregate(avg=Avg('nota'))['avg']
        return round(media, 1) if media else None

    @property
    def total_avaliacoes(self):
        return self.avaliacoes.count()

class Elenco(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='elenco')
    ator = models.ForeignKey(Ator, on_delete=models.CASCADE)
    papel = models.CharField(max_length=100, blank=True)  # papel do ator no filme

    def __str__(self):
        return f"{self.ator.nome} em {self.filme.titulo}"

class Trailer(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='trailers')
    url = models.URLField()
    descricao = models.CharField(max_length=255, blank=True)

    def __str__(self):
        return f"Trailer do filme {self.filme.titulo}"

class Avaliacao(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='avaliacoes')
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nota = models.IntegerField()
    comentario = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)

class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.usuario.user.username} favoritou {self.filme.titulo}'