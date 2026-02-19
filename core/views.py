from django.shortcuts import render, redirect
from .models import Produto, Cliente
from django.http import HttpResponse

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

def clientes(request):
    clientes = Cliente.objects.all()
    context = {'cli': clientes}
    return render(request, 'clientes.html', context)

def cadastraClientes(request):
    return render(request, 'cadastraClientes.html')

def salvarClientes(request):
    thisnome = request.POST.get('nome')
    thissobrenome = request.POST.get('sobrenome')
    thisemail = request.POST.get('email')
    thistelefone = request.POST.get('telefone')
    thiscpf = request.POST.get('cpf')
    cliente = Cliente(
        nome = thisnome,
        sobrenome = thissobrenome,
        email = thisemail,
        telefone = thistelefone,
        cpf = thiscpf
    )
    cliente.save()

    return redirect("urlclientes")