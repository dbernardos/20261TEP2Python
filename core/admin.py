from django.contrib import admin

from .models import Produto

class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'descricao', 'qtde', 'data_de_validade')

admin.site.register(Produto, ProdutoAdm)
