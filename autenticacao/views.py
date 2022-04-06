from http.client import HTTPResponse
from multiprocessing import reduction
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.messages import constants
from django.contrib import auth

# Create your views here.

def cadastro(request):
    # return HttpResponse('Cadastro')
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/plataforma')
        return render(request, 'cadastro.html') # Por padrão o Django procura o arquivo dentro do app (autenticacao, nesse caso) na pasta "templates"
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('password')
        confirmar_senha = request.POST.get('confirm-password')
        
        ### Verificação se a senha é idêntica
        if not senha == confirmar_senha:
            messages.add_message(request, constants.ERROR, 'As Senhas não coincidem')
            return redirect('/auth/cadastro')

        ### Verifica se alguns dos campos estão vazios, e retira os espaços vazios
        if len(username.strip()) == 0 or len(senha.strip()) == 0:
            messages.add_message(request, constants.ERROR, 'Username e Senha não podem ficar vazios')
            return redirect('/auth/cadastro')
        
        ### Verifica se há um usuário lá dentro
        user = User.objects.filter(username = username)
        if user.exists():
            messages.add_message(request, constants.ERROR, 'Este usuário já existe')
            return redirect('/auth/cadastro')
        try:
            user = User.objects.create_user(username=username, password=senha)
            user.save()
            return redirect('/auth/logar')
        except:
            messages.add_message(request, constants.ERROR, 'Erro interno do sistema')
            return redirect('/auth/cadastro')


def logar(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/plataforma')
        return render(request, "logar.html")
    elif request.method == "POST":
        username = request.POST.get('username')
        senha = request.POST.get('password')
        
        # Vai no banco e verifica se existe esse usuário com essa senha
        usuario = auth.authenticate(username=username, password=senha)
        if not usuario:
            messages.add_message(request, constants.ERROR, 'Username ou senha inválida')
            return redirect('/auth/logar')
        else:
            auth.login(request, usuario)
            return redirect('/plataforma')

def sair(request):
    auth.logout(request)
    return redirect('/auth/logar/')