from django.db import models
from localflavor.br.models import BRCPFField

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(decimal_places=2, max_digits=8)
    descricao = models.CharField(max_length=200)
    qtde = models.PositiveIntegerField(default=0)
    data_de_validade = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = BRCPFField(unique=True, null=True, blank=True)
    telefone = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)