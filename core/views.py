from django.shortcuts import render
from .models import Produto

def index(request):
    context = {'curso': 'Desenvolvimento de Sistemas'}
    return render(request, 'index.html', context)

def contato(request):
    context = {
        'nome': 'IFSC',
        'telefone': '(47) 3333-5555',
        'email': 'contato@ifsc.edu.br'
    }
    return render(request, 'contato.html', context)

def produtos(request):
    produtos = Produto.objects.all()
    context = {'prod': produtos}
    return render(request, 'produtos.html', context)