from django.shortcuts import render, redirect
from .models import Produto, Cliente
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

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

@login_required(login_url='urlentrar')
def produtos(request):
    produtos = Produto.objects.all()
    context = {'prod': produtos}
    return render(request, 'produtos.html', context)

@login_required(login_url='urlentrar')
def clientes(request):
    clientes = Cliente.objects.all()
    context = {'cli': clientes}
    return render(request, 'clientes.html', context)

@login_required(login_url='urlentrar')
def salvarClientes(request):
    if request.method == 'POST':
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
    
    return render(request, "salvarClientes.html")

@login_required(login_url='urlentrar')
def editaCliente(request, id):
    cliente = Cliente.objects.get(id=id)

    if request.method == "GET":
        context = {'cliente': cliente}
        return render(request, 'editaCliente.html', context)

    cliente.nome = request.POST.get('nome')
    cliente.sobrenome = request.POST.get('sobrenome')
    cliente.telefone = request.POST.get('telefone')
    cliente.email = request.POST.get('email')
    cliente.cpf = request.POST.get('cpf')
    cliente.save()
    return redirect('urlclientes')

@login_required(login_url='urlentrar')
def apagaCliente(request, id):
    cliente = Cliente.objects.get(id=id)
    cliente.delete()
    return redirect('urlclientes')

def entrar(request):
    if request.method == "GET":
        return render(request, "entrar.html")
    
    elif request.method == "POST":
        usuario = request.POST.get("usuario")
        senha = request.POST.get("senha")
        user = authenticate(username=usuario, password=senha)

        if user is not None:
            login(request, user)
            return redirect('urlprodutos')
        else:
            messages.error(request, "Falha na autentição!")
            return render(request, 'entrar.html')

def sair(request):
    logout(request)
    return redirect('urlentrar')
    