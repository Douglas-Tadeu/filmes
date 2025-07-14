from django.db import models
from django.contrib.auth.models import User

class Usuario(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.user.username

class Genero(models.Model):
    nome = models.CharField(max_length=100)

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
    codigo = models.CharField(max_length=10, unique=True)  # ex: "18+", "L", "12"
    descricao = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.codigo} - {self.descricao}"

class Filme(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField(blank=True)
    ano = models.PositiveIntegerField(null=True, blank=True)
    genero = models.ForeignKey(Genero, on_delete=models.SET_NULL, null=True)
    diretor = models.ForeignKey(Diretor, on_delete=models.SET_NULL, null=True)
    classificacao = models.ForeignKey(Classificacao, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titulo

class Elenco(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='elenco')
    ator = models.ForeignKey(Ator, on_delete=models.CASCADE)
    papel = models.CharField(max_length=100, blank=True)  # papel do ator no filme

    def __str__(self):
        return f"{self.ator.nome} em {self.filme.titulo}"

class Trailer(models.Model):
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE, related_name='trailers')
    url = models.URLField()
    descricao = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return f"Trailer de {self.filme.titulo}"

class Favorito(models.Model):
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    filme = models.ForeignKey(Filme, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'filme')

    def __str__(self):
        return f"{self.usuario} favoritou {self.filme}"

class Avaliacao(models.Model):
    filme = models.ForeignKey(Filme, related_name='avaliacoes', on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    nota = models.IntegerField()
    comentario = models.TextField(blank=True)
    data = models.DateTimeField(auto_now_add=True)
