🏫 SchoolPass: Sistema de Catraca Inteligente com Reconhecimento Facial
🚀 Sobre o Projeto
O SchoolPass é um sistema inovador de catraca inteligente desenvolvido para otimizar o controle de acesso de alunos e funcionários em instituições de ensino. Utilizando reconhecimento facial avançado, o sistema garante uma entrada rápida, segura e eficiente, eliminando a necessidade de cartões ou biometrias tradicionais.

Além do controle de acesso, o SchoolPass oferece um painel de gestão completo que permite aos administradores monitorar o fluxo de pessoas, registrar eventos e até mesmo automatizar a exibição da grade de matérias do dia para os alunos, otimizando a alocação de salas.

Este projeto visa aprimorar a segurança, a logística e a experiência diária na faculdade, proporcionando mais agilidade para alunos e professores.

✨ Funcionalidades Principais
Controle de Acesso por Reconhecimento Facial:

Identificação automática de alunos e funcionários cadastrados.

Liberação de acesso rápida e sem contato.

Registro de acessos (entrada/saída) com data e hora.

Cadastro de Usuários:

Tela de cadastro para alunos e funcionários (nome, matrícula, curso/departamento).

Associação de fotos para reconhecimento facial.

Gestão de Grade Horária Inteligente:

Atualização automática e rápida da grade de matérias por meio de importação de planilhas (CSV/Excel).

Associação da matéria e sala do dia de acordo com o curso e semestre do aluno.

Reuniões/Eventos: Possibilidade de realocar salas de acordo com necessidades específicas, otimizando o uso do espaço da faculdade.

Painel do Gestor (Dashboard):

Visão geral e detalhada de todos os eventos da catraca: quem entrou, quem saiu, horários.

Registro de acessos liberados ou negados.

Alertas e relatórios para auditoria e acompanhamento.

Interface Amigável:

Exibição clara do nome do aluno e da matéria/sala do dia após o reconhecimento.

Feedback visual de acesso (liberado/negado).

Interface de câmera configurável (redimensionável, sem tela cheia padrão).

🛠️ Tecnologias Utilizadas
Backend:

Python: Linguagem principal de desenvolvimento.

Django: Framework web para o backend, gestão de banco de dados (ORM) e painel administrativo.

SQLite3: Banco de dados padrão do Django (para desenvolvimento e teste).

OpenCV (cv2): Biblioteca para processamento de imagem e acesso à câmera.

face_recognition: Biblioteca de reconhecimento facial de alto nível.

numpy: Para operações numéricas de arrays de imagem.

Pillow: (Provavelmente uma dependência) para manipulação de imagens.

Deployment (Executável Desktop):

PyInstaller: Ferramenta para empacotar o aplicativo Python em um executável (.exe) autônomo para Windows.

⚙️ Configuração e Instalação (Ambiente de Desenvolvimento)
Para configurar o ambiente de desenvolvimento e rodar o projeto, siga os passos abaixo:

Clone o Repositório:

git clone https://github.com/seu-usuario/SchoolPass.git
cd SchoolPass

Crie e Ative um Ambiente Virtual:

python -m venv venv
# No Windows:
.\venv\Scripts\activate
# No macOS/Linux:
source venv/bin/activate

Instale as Dependências:

pip install -r requirements.txt # (Crie este arquivo com todas as suas libs)
# Se não tiver requirements.txt, instale manualmente:
# pip install django opencv-python face-recognition numpy Pillow pyinstaller

Configurações do Django:

Navegue até o diretório raiz do seu projeto Django (onde está o manage.py). Ex: cd reconhecimento_facial (se esse for o nome da pasta do seu projeto).

Certifique-se de que seus apps (cadastro_face, gestor, catraca_web ou similar) estão listados em INSTALLED_APPS no settings.py.

Mídia: Configure MEDIA_ROOT e MEDIA_URL no seu settings.py para gerenciar as fotos.

# settings.py
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

Inclua as URLs dos seus apps no urls.py principal do projeto.

# reconhecimento_facial/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('cadastro/', include('cadastro_face.urls')), # Exemplo
    path('gestao/', include('gestor.urls')),         # Exemplo
    path('catraca/', include('catraca_web.urls')),   # Exemplo
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

Configuração do Banco de Dados e Migrações:

Execute as migrações para criar as tabelas no seu db.sqlite3:

python manage.py makemigrations
python manage.py migrate

Crie um superusuário Django para acessar o painel administrativo:

python manage.py createsuperuser

Crie o Usuário "Curinga" no DB: Adicione um registro na tabela cadastro_face_usuario com o ID que você definiu para ID_USUARIO_DESCONHECIDO_OU_ERRO (ex: ID 1 e nome "DESCONHECIDO"). Você pode fazer isso via Django Admin ou diretamente no SQLite.

Pastas de Mídia:

Crie as pastas media/fotos e media/fotos_usuarios na raiz do seu projeto (no mesmo nível do manage.py).

Adicione as imagens dos rostos dos usuários autorizados na pasta media/fotos_usuarios. Certifique-se de que o nome do arquivo da imagem seja NOME_DO_ALUNO_foto.png (ex: Gustavo_Cerqueira_foto.png).

Inicie o Servidor Django (para testar o Admin e as APIs):

python manage.py runserver

Acesse http://127.0.0.1:8000/admin/ para o painel de gestão.

💻 Como Rodar o Executável da Catraca
Para rodar a catraca autônoma via webcam, você precisará do executável.

Altere o Código (interfaceFullscreen.py):

Certifique-se de que o seu script interfaceFullscreen.py contém a lógica de BASE_DIR para executáveis (usando sys.executable) e o restante do código que você desenvolveu (conexão ao DB, reconhecimento facial, busca de sala, etc.).

Ajuste a linha video_capture = cv2.VideoCapture(0) para video_capture = cv2.VideoCapture(1) se sua webcam externa for o índice 1. Teste outros índices (2, 3, etc.) se necessário.

Gere o Executável com PyInstaller:

Navegue no seu terminal até o diretório onde o arquivo interfaceFullscreen.py está localizado.

Execute o comando PyInstaller em uma única linha (substituindo os caminhos conforme o seu sistema):

pyinstaller --name "CatracaFacial" --onefile --windowed --add-data="C:\Users\anton\AppData\Local\Programs\Python\Python313\Lib\site-packages\cv2\data;cv2/data" --add-data="C:\Users\anton\Documents\Python RAD\Projeto SchoolPass\Definitivo PROJETO RECONHECIMENTO\Projeto Reconhecimento Facial\reconhecimento_facial\media\fotos_usuarios;media/fotos_usuarios" --add-data="C:\Users\anton\AppData\Local\Programs\Python\Python313\Lib\site-packages\face_recognition_models\models;face_recognition_models/models" interfaceFullscreen.py

O executável CatracaFacial.exe será gerado na pasta dist/.

Configuração do Executável para Uso:

Copie o CatracaFacial.exe para a pasta raiz do seu projeto Django (onde o manage.py e o db.sqlite3 estão).

Certifique-se de que o arquivo db.sqlite3 esteja na mesma pasta do CatracaFacial.exe.

Certifique-se de que as pastas media/fotos_usuarios (com as fotos de referência) e media/fotos (para salvar novas fotos) estejam na mesma pasta do CatracaFacial.exe.

Execute o SchoolPass:

Dê um duplo clique em CatracaFacial.exe. A janela da câmera deverá abrir.

Posicione um rosto na frente da câmera para testar o reconhecimento e o registro de acesso.

🤝 Contribuição
Contribuições são muito bem-vindas! Se você tiver ideias para melhorias, novas funcionalidades ou encontrar algum bug, sinta-se à vontade para:

Fazer um "fork" do repositório.

Criar uma nova "branch" (git checkout -b feature/sua-feature ou fix/seu-bug).

Fazer suas alterações.

Submeter um "pull request" detalhado.

📄 Licença
Este projeto está licenciado sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

📞 Contato
Para mais informações, entre em contato com [Seu Nome/Nome da Equipe] através do GitHub.
