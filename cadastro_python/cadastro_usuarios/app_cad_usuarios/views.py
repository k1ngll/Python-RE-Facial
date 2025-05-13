from django.shortcuts import render
from .forms import UsuarioForm
from django.contrib import messages
import base64
from django.core.files.base import ContentFile

#Método para enviar os dados do formulário para o banco de dados

def cadastrar_usuario(request):

    #Verifica se o método do formulário é POST.
    if request.method == "POST":
        form = UsuarioForm(request.POST) 

        #Verifica se os dados são válidos
        if form.is_valid():
            usuario = form.save(commit=False)

            imagem_base64 = request.POST.get('foto')
            if imagem_base64:
                try:
                    format, imgstr = imagem_base64.split(';base64,') 
                    ext = format.split('/')[-1]
                    nome_arquivo = f"{usuario.nome}_foto.{ext}"

                    usuario.foto = ContentFile(base64.b64decode(imgstr), name=nome_arquivo)
                except Exception as e:
                    messages.error(request, f"Erro ao processar a imagem: {e}")

            usuario.save()
            messages.success(request, "Cadastro realizado com sucesso!")
            form = UsuarioForm()  

    else:
        form = UsuarioForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})

def demonstracao(request):
    return render(request, 'demonstracao.html')
