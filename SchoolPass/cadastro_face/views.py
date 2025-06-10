from django.shortcuts import render
from .forms import UsuarioForm
from django.contrib import messages
import base64
from django.core.files.base import ContentFile


# Cadastro de usuários com imagem em base64
def cadastrar_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)

        if form.is_valid():
            imagem_base64 = request.POST.get('foto')
            
            if not imagem_base64:
                messages.error(request, "Por favor, tire uma foto antes de cadastrar.")
            else:
                try:
                    usuario = form.save(commit=False)

                    # Processar imagem base64
                    format, imgstr = imagem_base64.split(';base64,') 
                    ext = format.split('/')[-1]
                    nome_arquivo = f"{usuario.nome}_foto.{ext}"

                    usuario.foto = ContentFile(base64.b64decode(imgstr), name=nome_arquivo)
                    usuario.save()

                    messages.success(request, "Cadastro realizado com sucesso!")
                    form = UsuarioForm()  # Limpa o formulário
                except Exception as e:
                    messages.error(request, f"Erro ao processar a imagem: {e}")
        else:
            messages.error(request, "Por favor, preencha todos os campos obrigatórios.")

    else:
        form = UsuarioForm()

    return render(request, 'usuarios/cadastro.html', {'form': form})
