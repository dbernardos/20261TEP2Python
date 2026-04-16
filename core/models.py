from django.db import models

class Produto(models.Model):
    nome = models.CharField(max_length=50)
    preco = models.DecimalField(decimal_places=2, max_digits=8)
    descricao = models.TextField()
    qtde = models.PositiveIntegerField(default=0)
    data_de_validade = models.DateField(auto_now_add=True)
    imagem = models.ImageField(upload_to='produtos/', null=True, blank=True)
    def __str__(self):
        return self.nome

class Cliente(models.Model):
    nome = models.CharField(max_length=200)
    sobrenome = models.CharField(max_length=200, null=True, blank=True)
    data_nascimento = models.DateField(null=True, blank=True)
    cpf = models.CharField(max_length=22, null=True, blank=True)
    telefone = models.CharField(max_length=30, null=True, blank=True)
    email = models.EmailField(max_length=100, null=True, blank=True)

class Avaliacao(models.Model):
    id_evaluation = models.CharField(max_length=255, null=True, blank=True)
    title = models.CharField(max_length=255, null=True, blank=True)
    price = models.FloatField(null=True, blank=True)
    user_id = models.CharField(max_length=100, null=True, blank=True)
    profile_name = models.CharField(max_length=255, null=True, blank=True)
    review_helpfulness = models.CharField(max_length=20, null=True, blank=True)
    review_score= models.FloatField()
    review_time = models.IntegerField()
    review_summary = models.CharField(max_length=255, null=True, blank=True)
    review_text = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.title} - Score: {self.review_score}"