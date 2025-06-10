O sistema SchoolPass é uma solução inovadora para o controle de acesso em ambientes escolares, utilizando reconhecimento facial para gerenciar a entrada e saída de alunos e funcionários. Ele combina a robustez de uma aplicação desktop para a catraca com a flexibilidade de um backend web Django para a gestão de dados.

✨ Recursos
Reconhecimento Facial Preciso: Identificação rápida e eficiente de indivíduos.

Gestão Centralizada de Usuários: Cadastro e gerenciamento de alunos, funcionários e grades horárias via interface web.

Registros de Acesso Detalhados: Armazenamento de informações sobre cada entrada e saída, incluindo horário, sala e status.

Sistema Híbrido Flexível: Opera com uma aplicação de catraca autônoma e um painel de controle web.

Fácil Implantação: Utiliza SQLite3 como banco de dados local, simplificando a configuração inicial.

🚀 Como Funciona
O SchoolPass opera com dois componentes principais que interagem entre si:

Catraca (Aplicação Desktop): Um executável Python que utiliza a câmera para capturar imagens, realizar o reconhecimento facial e registrar os acessos diretamente no banco de dados local. Ele exibe mensagens de status em tempo real.

Backend Django (Aplicação Web): Um painel administrativo acessível via navegador, responsável por:

Cadastrar e gerenciar usuários (alunos e funcionários).

Definir e consultar a grade horária das turmas.

Visualizar o histórico de registros de acesso.

Ambos os componentes compartilham o mesmo arquivo db.sqlite3, garantindo a sincronização dos dados.

🖥️ Arquitetura do Projeto
O projeto é estruturado para separar as responsabilidades da catraca e da gestão, enquanto mantêm um banco de dados unificado.

.
├── manage.py
├── db.sqlite3
├── README.md
├── haarcascade_frontalface_default.xml # Classificador Haar Cascade do OpenCV
├── interface padrao.py                 # Script da interface padrão da catraca
├── interfaceFullscreen.py              # Script da interface de catraca em tela cheia
├── media/
│   ├── fotos/                  # Fotos capturadas pela catraca
│   └── fotos_usuarios/         # Fotos dos usuários autorizados para reconhecimento
├── reconhecimento_facial/      # Pasta raiz do projeto Django (settings.py, urls.py, etc.)
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
├── cadastro_face/              # App Django de cadastro de faces/usuários
│   ├── migrations/
│   ├── __init__.py
│   ├── admin.py
│   ├── apps.py
│   ├── models.py               # Modelo CadastroFaceUsuario
│   ├── tests.py
│   └── views.py
└── gestor/                     # App Django de gestão (registros de acesso, grade horária)
    ├── migrations/
    ├── __init__.py
    ├── admin.py
    ├── apps.py
    ├── models.py               # Modelos GestorRegistroAcesso, GestorGradeHoraria
    ├── tests.py
    └── views.py

Componentes Essenciais
interfaceFullscreen.py / interface padrao.py: Scripts Python responsáveis pela lógica da catraca (captura de imagem, detecção/reconhecimento facial, interação com o DB).

cadastro_face/: Aplicação Django para o gerenciamento de usuários, incluindo o modelo CadastroFaceUsuario que armazena dados como nome, tipo, matrícula e o caminho para a foto do usuário.

gestor/: Aplicação Django para a gestão de registros de acesso (GestorRegistroAcesso) e grade horária (GestorGradeHoraria).

db.sqlite3: O banco de dados SQLite local que armazena todas as informações do sistema.

media/fotos_usuarios/: Diretório que armazena as fotos dos usuários autorizados, utilizadas pelo algoritmo de reconhecimento facial.

🛠️ Instalação e Configuração
Para configurar e executar o SchoolPass, siga os passos abaixo:

Clone o Repositório:

git clone [URL_DO_SEU_REPOSITORIO]
cd SchoolPass

Crie e Ative um Ambiente Virtual:
É altamente recomendável usar um ambiente virtual para gerenciar as dependências do projeto.

python -m venv venv
# No Windows
venv\Scripts\activate
# No macOS/Linux
source venv/bin/activate

Instale as Dependências do Python:
Você precisará instalar as bibliotecas necessárias para o Django e as operações de visão computacional.

pip install django opencv-python face-recognition numpy

Nota: Se encontrar problemas com face-recognition, pode ser necessário instalar as bibliotecas C++ de compilação ou usar uma versão pré-compilada do OpenCV.

Configurações do Django:
Navegue até o diretório raiz do projeto Django (reconhecimento_facial) e certifique-se de que as configurações estão corretas em settings.py.

Aplique as Migrações do Banco de Dados:
Isso criará as tabelas necessárias no seu db.sqlite3.

python manage.py makemigrations
python manage.py migrate

Crie um Superusuário (para o Django Admin):

python manage.py createsuperuser

Siga as instruções para criar seu nome de usuário e senha.

Adicione Fotos de Usuários Autorizados:
Coloque as fotos dos usuários que devem ser reconhecidos na pasta media/fotos_usuarios/. Os nomes dos arquivos devem ser claros (ex: Nome Sobrenome_foto.jpg). O sistema irá carregar as codificações faciais dessas imagens.

🚀 Executando o Sistema
1. Iniciar o Backend Django
Para acessar o painel administrativo e gerenciar usuários/grades horárias:

python manage.py runserver

Acesse http://127.0.0.1:8000/admin/ no seu navegador e faça login com as credenciais do superusuário que você criou.

2. Iniciar a Aplicação da Catraca
Você pode executar a catraca usando um dos scripts Python:

Interface Padrão:

python "interface padrao.py"

Interface em Tela Cheia:

python interfaceFullscreen.py

A aplicação da catraca abrirá uma janela exibindo o feed da câmera e as mensagens de status. Pressione 'q' para sair.

📦 Empacotamento para Executável (Opcional)
Para criar um executável autônomo da aplicação da catraca (ex: CatracaFacial.exe), você pode usar o PyInstaller.

Instale o PyInstaller:

pip install pyinstaller

Crie o Executável:
Navegue até o diretório onde interfaceFullscreen.py ou interface padrao.py está localizado e execute:

pyinstaller --onefile --add-data "db.sqlite3;." --add-data "haarcascade_frontalface_default.xml;." --add-data "media/fotos_usuarios;media/fotos_usuarios" interfaceFullscreen.py

A flag --onefile cria um único executável.

--add-data é crucial para incluir o banco de dados, o classificador Haar Cascade e as fotos dos usuários dentro do pacote ou em um diretório acessível pelo executável.

O executável será gerado na pasta dist/.

⚠️ Considerações Importantes
Sincronização de Fotos: As fotos em media/fotos_usuarios e os registros na tabela cadastro_face_usuario devem ser mantidos sincronizados. Se você adicionar ou remover usuários no Django Admin, a pasta media/fotos_usuarios deve ser atualizada manualmente ou um mecanismo de sincronização automática deve ser implementado. Se você empacotar o executável, ele precisará ser reconstruído com as novas fotos.

Escalabilidade: Para implantações maiores ou ambientes com múltiplos acessos simultâneos, considere migrar o banco de dados de SQLite3 para um SGBD mais robusto como PostgreSQL ou MySQL.

Segurança: Em um ambiente de produção, medidas de segurança adicionais (como senhas mais robustas, proteção contra adulteração de arquivos e segurança de rede) devem ser implementadas.

💡 Melhorias Futuras Potenciais
Interface Web da Catraca: Desenvolver uma interface web (frontend JavaScript) que envie frames para uma API Django para reconhecimento, permitindo o uso via navegador.

Sincronização Automática de Fotos: Implementar um mecanismo para que a aplicação da catraca possa sincronizar as fotos dos usuários autorizados diretamente do backend Django, eliminando a necessidade de reconstruir o executável a cada nova foto.

Controle da Catraca Física: Integração com hardware de catraca real para liberação automática (saída de sinal).

Relatórios Avançados: Geração de relatórios mais complexos no painel do gestor (ex: presença por turma, pico de acessos).

Detecção de Vida (Liveness Detection): Incorporar um módulo para prevenir fraudes com fotos ou vídeos.