from django.shortcuts import render, redirect
from .models import Produto, Cliente, Avaliacao
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import ProdutoForm

import io
import urllib, base64
import matplotlib
matplotlib.use('Agg')

import pandas as pd
import matplotlib.pyplot as plt

def dashboard(request):
    df = get_dataframe()
    grafico_distribuicao_notas = distribuicao_das_notas_view(df)
    grafico_top_livros, tam = livros_mais_avaliados_view(df)
    grafico_usuarios_mais_ativos = usuarios_mais_ativos_view(df)
    grafico_evolucao_reviews = evolucao_reviews_view(df)
    grafico_preco_score = preco_vs_score_view(df)
    grafico_sentimento_reviews = sentimento_reviews_view(df)

    context = {
        'grafico_distribuicao_notas': grafico_distribuicao_notas,
        'grafico_top_livros': grafico_top_livros,
        'total_avaliacoes': tam,
        'grafico_usuarios_mais_ativos': grafico_usuarios_mais_ativos,
        'grafico_evolucao_reviews': grafico_evolucao_reviews,
        'grafico_preco_score': grafico_preco_score,
        'grafico_sentimento_reviews': grafico_sentimento_reviews,
    }

    return render(request, 'dashboard.html', context)


# -------------------------------------------- #
def sentimento_reviews_view(df):
    # boas = ['good', 'great', 'excellent', 'I loved', 'I recommend']
    # ruins = ['bad', 'terrible', 'disappointing', 'I didn\'t like it', 'terrible']
    ruins01 = ['annoyed', 'displeased', 'uneasy', 'bothered', 'disappointed', 'unsettled', 'dissatisfied', 'discouraged', 'concerned', 'worried', 'upset', 'troubled', 'disheartened', 'discontent', 'irritated', 'vexed', 'perturbed', 'distressed', 'dismayed', 'disgruntled']
    ruins02 = ['angry', 'frustrated', 'anxious', 'resentful', 'bitter', 'hostile', 'agitated', 'disturbed', 'offended', 'indignant', 'exasperated', 'aggrieved', 'disgusted', 'repelled', 'appalled', 'outraged', 'fearful', 'despondent', 'miserable', 'gloomy']
    ruins03 = ['furious', 'enraged', 'livid', 'incensed', 'wrathful', 'seething', 'berserk', 'devastated', 'heartbroken', 'despairing', 'hopeless', 'horrified', 'aghast', 'traumatized', 'shattered', 'broken', 'tormented', 'anguished', 'vengeful', 'hatred']

    boas01 = ['pleased', 'content', 'glad', 'happy', 'satisfied', 'comfortable', 'relieved', 'hopeful', 'cheerful', 'optimistic', 'grateful', 'appreciative', 'calm', 'peaceful', 'interested', 'curious', 'encouraged', 'confident', 'proud', 'amused']
    boas02 = ['joyful', 'delighted', 'excited', 'enthusiastic', 'thrilled', 'elated', 'inspired', 'motivated', 'passionate', 'fond', 'affectionate', 'charmed', 'impressed', 'admiring', 'thankful', 'blessed', 'uplifted', 'rejoicing', 'vibrant', 'radiant']
    boas03 = ['ecstatic', 'euphoric', 'overjoyed', 'blissful', 'jubilant', 'exhilarated', 'elated', 'rapturous', 'transcendent', 'serene', 'fulfilled', 'empowered', 'triumphant', 'glorified', 'exalted', 'enchanted', 'mesmerized', 'awestruck', 'reverent', 'love']

    def classificar(texto):
        texto = str(texto).lower()
        if any(p in texto for p in boas01): return 'Bom'
        if any(p in texto for p in boas02): return 'Muito Bom'
        if any(p in texto for p in boas03): return 'Excelente'
        if any(p in texto for p in ruins01): return 'Ruim'
        if any(p in texto for p in ruins02): return 'Muito Ruim'
        if any(p in texto for p in ruins03): return 'Péssimo'
        return 'Neutro'

    df['sentimento'] = df['review_text'].fillna('').apply(classificar)
    contagem = df['sentimento'].value_counts()
    cores = ['lightgreen', 'mediumseagreen', 'green', 'lightcoral', 'lightsalmon', 'red', 'lightskyblue']
    rotulos = ['Bom', 'Muito Bom', 'Excelente', 'Ruim', 'Muito Ruim', 'Péssimo', 'Neutro']

    plt.figure(figsize=(10, 6))
    plt.pie(contagem, autopct='%1.1f%%', colors=cores, labels=rotulos)
    plt.title('Distribuição de Sentimentos nos Sumários das Avaliações')
    plt.tight_layout()
    grafico_sentimento = plot_to_base64(plt.gcf())
    plt.close()

    return grafico_sentimento
    

def preco_vs_score_view(df):
    df_preco = df[df['price'] > 0]
    df_preco = df_preco.sample(n=1000)

    plt.figure(figsize=(10, 6))
    plt.scatter(df_preco['price'], df_preco['review_score'], alpha=0.3, color='green')
    plt.title('Correlação entre Preço e Nota da Avaliação')
    plt.xlabel('Preço (R$)')
    plt.ylabel('Score da avaliação')
    plt.tight_layout()
    grafico_preco_score = plot_to_base64(plt.gcf())
    plt.close()

    return grafico_preco_score


def evolucao_reviews_view(df):
    df['data_ptbr'] = pd.to_datetime(df['review_time'], unit='s')
    df['ano'] = df['data_ptbr'].dt.year
    avaliacoes_por_ano = df.groupby('ano').size()

    plt.figure(figsize=(10, 6))
    avaliacoes_por_ano.plot(kind='line', marker='o', color='red')
    plt.title('Evolução do Número de Avaliações por Ano')
    plt.xlabel('Ano')
    plt.ylabel('Quantidade de avaliações')
    plt.tight_layout()
    grafico_evolucao_reviews = plot_to_base64(plt.gcf())
    plt.close()

    return grafico_evolucao_reviews

def usuarios_mais_ativos_view(df):
    mais_ativos = df['profile_name'].value_counts().nlargest(15)
    plt.figure(figsize=(10, 6))
    mais_ativos.sort_values().plot(kind='barh', color='blue')
    plt.title('Top 15 Usuários Mais Ativos')
    plt.xlabel('Número de Avaliações')
    plt.ylabel('Usuário')
    plt.tight_layout()
    grafico_usuarios_mais_ativos = plot_to_base64(plt.gcf())
    plt.close()

    return grafico_usuarios_mais_ativos

def livros_mais_avaliados_view(df):
    top_10_livros = df['title'].value_counts().nlargest(10)
    plt.figure(figsize=(12, 8))
    top_10_livros.sort_values().plot(kind='barh', color='coral')
    plt.title('Top 10 Livros com Mais Avaliações')
    plt.xlabel('Número de Avaliações')
    plt.ylabel('Título do Livro')
    plt.tight_layout()
    grafico_top_livros = plot_to_base64(plt.gcf())
    plt.close()

    return grafico_top_livros, len(df)

def distribuicao_das_notas_view(df):
    plt.figure(figsize=(10, 6))
    df['review_score'].value_counts().sort_index().plot(kind='bar', color='skyblue')
    plt.title('Distribuição das Notas das Avaliações')
    plt.xlabel('Nota (Score)')
    plt.ylabel('Quantidade de Avaliações')
    plt.grid(axis='y', linestyle='--')
    plt.tight_layout()
    grafico_distribuicao_notas = plot_to_base64(plt.gcf())
    plt.close()

    return grafico_distribuicao_notas

def get_dataframe():
    # Busca todos os dados do banco e retorna um DataFrame do Pandas
    avaliacoes = Avaliacao.objects.all().values()
    df = pd.DataFrame(list(avaliacoes))
    return df

def plot_to_base64(fig):
    # Converte uma figura Matplotlib para uma string base64 para ser usada no HTML
    buf = io.BytesIO()
    fig.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    return urllib.parse.quote(string)
# -------------------------------------------- # 
def index(request):
    produtos = Produto.objects.all()
    context = {'produtos': produtos}
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
    context = {'produtos': produtos}
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

def salvarProdutos(request):
    if request.method == 'GET':
        form = ProdutoForm()
        return render(request, 'salvarProdutos.html', {'form': form})
    else:
        form = ProdutoForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('urlprodutos')

def editarProdutos(request, id):
    produto = Produto.objects.get(id=id)
    if request.method == 'GET':
        form = ProdutoForm(instance=produto)
        return render(request, 'editarProdutos.html', {'form': form})
    else:
        form = ProdutoForm(request.POST, request.FILES, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('urlprodutos')