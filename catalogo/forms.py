from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Avaliacao, Filme, Genero, Diretor

class AvaliacaoForm(forms.ModelForm):
    class Meta:
        model = Avaliacao
        fields = ['nota', 'comentario']
        widgets = {
            'nota': forms.NumberInput(attrs={'min': 1, 'max': 10}),
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
