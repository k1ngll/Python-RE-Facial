from django.shortcuts import render, redirect, get_object_or_404
from .forms import UploadPlanilhaForm
from .models import GradeHoraria, RegistroAcesso, Curso
import pandas as pd
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.urls import reverse
from django.core.validators import EmailValidator
from django.core.exceptions import ValidationError
from django.core.mail import send_mail
from django.db.models import Case, When, IntegerField

def tela_gestor(request):
    if request.method == 'POST':
        form = UploadPlanilhaForm(request.POST, request.FILES)
        if form.is_valid():
            arquivo = request.FILES['arquivo']
            nome_arquivo = arquivo.name.lower()

            try:
                if nome_arquivo.endswith('.csv'):
                    df = pd.read_csv(arquivo,sep=';')
                elif nome_arquivo.endswith('.xlsx'):
                    df = pd.read_excel(arquivo, engine='openpyxl')
                else:
                    messages.error(request, "Formato de arquivo não suportado. Use .csv ou .xlsx.")
                    return redirect('gestor:tela_gestor')
            except Exception as e:
                messages.error(request, f"Erro ao ler o arquivo: {e}")
                return redirect('gestor:tela_gestor')

            # Verificar se as colunas esperadas existem
            colunas_esperadas = ['Curso','Disciplina', 'Dia da Semana', 'Horario', 'Sala']
            if not all(coluna in df.columns for coluna in colunas_esperadas):
                messages.error(request, "A planilha está com colunas incorretas ou ausentes.")
                return redirect('gestor:tela_gestor')

            erros = 0
            for _, linha in df.iterrows():
                try:
                    nome_do_curso = int(str(linha['Curso']).strip())
                    nome_disciplina = str(linha['Disciplina']).strip()
                    dia = str(linha['Dia da Semana']).strip()
                    horario_raw = linha['Horario']
                    sala = str(linha['Sala']).strip()

                    # Verificação de campos vazios
                    if pd.isnull(nome_do_curso) or pd.isnull(nome_disciplina) or pd.isnull(dia) or pd.isnull(horario_raw) or pd.isnull(sala):
                        erros += 1
                        continue
            
                    #curso, _ = Curso.objects.get_or_create(nome_curso=nome_do_curso)

                    GradeHoraria.objects.get_or_create(
                        curso_id=nome_do_curso,
                        disciplina=nome_disciplina,
                        dia_semana=dia,
                        horario=horario_raw,
                        sala=sala,
                    )

                except Exception as e:
                    print(e)
                    erros += 1
                    continue

            if erros > 0:
                messages.warning(request, f"Importação concluída com {erros} linha(s) ignorada(s) por erro de formato.")
            else:
                messages.success(request, "Importação concluída com sucesso.")

            return redirect('gestor:tela_gestor')
    else:
        form = UploadPlanilhaForm()

    logs = RegistroAcesso.objects.order_by('-horario_entrada')[:50]
    return render(request, 'tela_gestor.html', {'form': form, 'logs': logs})

def editar_grade(request):
    cursos = Curso.objects.all()
    curso_id = request.GET.get('curso')

    limite_tempo = timezone.now() - timedelta(hours=2)

    dias_ordem = Case(
        When(dia_semana='Segunda', then=1),
        When(dia_semana='Terça', then=2),
        When(dia_semana='Quarta', then=3),
        When(dia_semana='Quinta', then=4),
        When(dia_semana='Sexta', then=5),
        output_field=IntegerField()
    )

    if curso_id:
        grade = GradeHoraria.objects.filter(
            curso_id=curso_id,
            data_criacao__gte=limite_tempo
        ).select_related('curso').annotate(
            dia_ordem=dias_ordem
        ).order_by('dia_ordem', 'horario')
    else:
        grade = GradeHoraria.objects.filter(
            data_criacao__gte=limite_tempo
        ).select_related('curso').annotate(
            dia_ordem=dias_ordem
        ).order_by('curso', 'dia_ordem', 'horario')

    if request.method == 'POST':
        for key, value in request.POST.items():
            if key.startswith('sala_'):
                grade_id = key.split('_')[1]
                nova_sala = value.strip()
                grade_obj = get_object_or_404(GradeHoraria, id=grade_id)
                if grade_obj.sala != nova_sala:
                    grade_obj.sala = nova_sala
                    grade_obj.save()
        messages.success(request, 'Salas atualizadas com sucesso.')
        return redirect('gestor:editar_grade')

    return render(request, 'editar_grade.html', {
        'grade': grade,
        'cursos': cursos,
        'curso_id': curso_id
    })


# Página inicial
def home(request):
    return render(request, 'home.html')


# Redirecionamento para home após login
def login_gestor(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        senha = request.POST.get('password')

        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            return redirect('gestor/home')
        else:
            messages.error(request, "Usuário ou senha inválidos.")

    return render(request, 'login.html')



def cadastro_gestor(request):
    if request.method == "POST":
        email = request.POST.get('email')
        senha = request.POST.get('senha')

        # Validações básicas
        if not email or not senha:
            messages.error(request, "Preencha todos os campos.")
            return render(request, 'cadastro_gestor.html')

        # Validação de e-mail
        validator = EmailValidator()
        try:
            validator(email)
        except ValidationError:
            messages.error(request, "Digite um e-mail válido.")
            return render(request, 'cadastro_gestor.html')

        if User.objects.filter(username=email).exists():
            messages.error(request, "Este e-mail já está cadastrado.")
            return render(request, 'cadastro_gestor.html')

        # Cria o usuário
        User.objects.create_user(username=email, email=email, password=senha)

        # Envia o e-mail com a senha
        try:
            send_mail(
                subject="Cadastro de Gestor - SchoolPass",
                message=f"Olá, você foi cadastrado como gestor no sistema SchoolPass.\n\nSeu e-mail: {email}\nSua senha: {senha}\n",
                from_email='schoolpassrec@gmail.com',
                recipient_list=[email],
                fail_silently=False,
            )
            messages.success(request, "Gestor cadastrado! Um e-mail com a senha foi enviado.")
            return redirect(reverse('gestor:home'))
        except Exception as e:
            messages.warning(request, f"Gestor cadastrado, mas houve um erro ao enviar o e-mail: {e}")

    return render(request, 'cadastro_gestor.html')


def sair_conta(request):
    logout(request)  
    return redirect('login')