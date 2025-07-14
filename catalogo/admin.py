from django.contrib import admin
from .models import (
    Filme,
    Classificacao,
    Genero,
    Avaliacao,
    Favorito,
    Diretor,
    Ator,
    Elenco,
    Trailer,
    Usuario
)

admin.site.register(Filme)
admin.site.register(Classificacao)
admin.site.register(Genero)
admin.site.register(Avaliacao)
admin.site.register(Favorito)
admin.site.register(Diretor)
admin.site.register(Ator)
admin.site.register(Elenco)
admin.site.register(Trailer)
admin.site.register(Usuario)
