from django.contrib import admin

from .models import Produto, Cliente

class ProdutoAdm(admin.ModelAdmin):
    list_display = ('nome', 'preco', 'descricao', 'qtde', 'data_de_validade')

class ClienteAdm(admin.ModelAdmin):
    list_display = ('nome', 'sobrenome', 'data_nascimento', 'telefone', 'email')


admin.site.register(Produto, ProdutoAdm)
admin.site.register(Cliente, ClienteAdm)
