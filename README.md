🏫 SchoolPass: Sistema de Catraca Inteligente com Reconhecimento Facial
🚀 Sobre o Projeto
O SchoolPass é um sistema de catraca inteligente que utiliza reconhecimento facial para controlar o acesso de alunos e funcionários em instituições de ensino. Ele visa otimizar a segurança e a logística, oferecendo um controle de entrada rápido e eficiente, além de um painel para gestão de acessos e grades horárias.

✨ Funcionalidades Principais
Reconhecimento Facial: Identifica usuários para liberação de acesso e registra entradas/saídas.

Cadastro Simplificado: Permite o registro de alunos e funcionários com foto.

Gestão de Grade Horária: Atualiza automaticamente as matérias e salas via planilha, facilitando a alocação de espaços.

Painel de Gestão: Oferece uma visão geral dos acessos, incluindo registros de entrada/saída e status (liberado/negado).

Interface Intuitiva: Exibe informações claras para o usuário (nome, sala/matéria) e feedback visual.

🛠️ Tecnologias Utilizadas
Python: Linguagem principal.

Django: Framework web para backend e banco de dados.

SQLite3: Banco de dados.

OpenCV (cv2) & face_recognition: Para visão computacional e reconhecimento facial.

PyInstaller: Para criar o executável desktop (.exe).

💻 Como Rodar o Executável da Catraca
Para utilizar o sistema SchoolPass como um aplicativo de desktop:

Gere o Executável: Navegue até o diretório do seu script interfaceFullscreen.py no terminal e execute o comando PyInstaller:

pyinstaller --name "CatracaFacial" --onefile --windowed --add-data="C:\Users\anton\AppData\Local\Programs\Python\Python313\Lib\site-packages\cv2\data;cv2/data" --add-data="C:\Users\anton\Documents\Python RAD\Projeto SchoolPass\Definitivo PROJETO RECONHECIMENTO\Projeto Reconhecimento Facial\reconhecimento_facial\media\fotos_usuarios;media/fotos_usuarios" --add-data="C:\Users\anton\AppData\Local\Programs\Python\Python313\Lib\site-packages\face_recognition_models\models;face_recognition_models/models" interfaceFullscreen.py

(Lembre-se de substituir os caminhos pelos seus caminhos reais).

Configure os Arquivos:

Copie o CatracaFacial.exe (encontrado na pasta dist/) para a pasta raiz do seu projeto.

Garanta que o arquivo db.sqlite3 esteja na mesma pasta do CatracaFacial.exe.

As pastas media/fotos_usuarios (com as fotos de referência) e media/fotos (para salvar novas fotos) também devem estar na mesma pasta do executável.

Execute: Dê um duplo clique em CatracaFacial.exe.
