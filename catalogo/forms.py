from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Avaliacao, Filme, Genero, Diretor, Ator, Elenco, Trailer, Classificacao, Favorito

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
        widgets = {
            'nota': forms.NumberInput(attrs={'min': 1, 'max': 5}),
            'comentario': forms.Textarea(attrs={'rows': 3}),
        }

class FilmeForm(forms.ModelForm):
    class Meta:
        model = Filme
        fields = '__all__'

class GeneroForm(forms.ModelForm):
    class Meta:
        model = Genero
        fields = ['nome']

class DiretorForm(forms.ModelForm):
    class Meta:
        model = Diretor
        fields = ['nome']

class RegistroForm(UserCreationForm):
    email = forms.EmailField(required=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

class AtorForm(forms.ModelForm):
    class Meta:
        model = Ator
        fields = ['nome', 'data_nascimento']
        widgets = {
            'data_nascimento': forms.DateInput(attrs={'type': 'date'}),
        }

class ElencoForm(forms.ModelForm):
    class Meta:
        model = Elenco
        fields = ['filme', 'ator', 'papel']

class TrailerForm(forms.ModelForm):
    class Meta:
        model = Trailer
        fields = ['filme', 'url', 'descricao']

class ClassificacaoForm(forms.ModelForm):
    class Meta:
        model = Classificacao
        fields = ['descricao', 'idade_minima']

class FavoritoForm(forms.ModelForm):
    class Meta:
        model = Favorito
        fields = ['filme']