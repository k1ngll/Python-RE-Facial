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

💻 Compatibilidade e Como Rodar o Sistema
O sistema SchoolPass é projetado para operar em ambientes Windows. Para utilizá-lo, siga os passos abaixo:

Inicie o Backend Django:
Para acessar o painel administrativo e gerenciar usuários/grades horárias, navegue até o diretório raiz do seu projeto Django (ex: reconhecimento_facial/ ou onde está seu manage.py) no terminal e execute:

python manage.py runserver

Acesse http://127.0.0.1:8000/admin/ no seu navegador e faça login com as credenciais do superusuário que você criou previamente.

Inicie a Aplicação da Catraca:
Abra um novo terminal e navegue até o diretório onde o script interface padrao.py está localizado. Execute o script diretamente:

python "interface padrao.py"

A aplicação da catraca abrirá uma janela exibindo o feed da câmera e as mensagens de status. Pressione a tecla 'q' para sair da aplicação da catraca.

🤝 Contribuição
Contribuições são bem-vindas! Sinta-se à vontade para fazer um fork, criar branches e submeter pull requests.

📄 Licença
Este projeto está licenciado sob a licença MIT.

📞 Contato
Para mais informações, entre em contato com [Seu Nome/Nome da Equipe] através do GitHub.