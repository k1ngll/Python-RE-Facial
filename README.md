# **Reconhecimento Facial para Catraca Universitária** 🎓🚀  

Este projeto permite o cadastro e autenticação de alunos via reconhecimento facial, e monstrando suas disponiveis do dia se houver.

---

## **1. Tecnologias Utilizadas**  
✅ Python 3.+
✅ Django + Django REST Framework  
✅ OpenCV + dlib + face_recognition  
✅ SQLITE (ou outro banco de dados)  
✅ HTML, CSS, JavaScript (para interface web)  

---

## **2. Estrutura do Projeto**  
📂 **reconhecimento-facial-catraca/**  
├── 📂 **backend/** *(código do Django)*  
│ ├── settings.py *(configuração do banco de dados, apps, etc.)*  
│ ├── models.py *(modelo do aluno com face codificada)*  
│ ├── views.py *(cadastro e autenticação facial)*  
│ ├── urls.py *(rotas da API)*  
│ └── serializers.py *(serialização dos dados para API)*  
├── 📂 **frontend/** *(página de cadastro e login)*  
│ ├── index.html *(interface do sistema)*  
│ ├── script.js *(chamadas para API)*  
│ └── styles.css *(estilização da interface)*  
├── 📂 **reconhecimento/** *(código de reconhecimento facial)*  
│ ├── capturar_face.py *(captura da imagem e extração de face encoding)*  
│ ├── autenticar.py *(verifica o rosto na base de dados e libera a catraca)*  
│ └── camera.py *(lê a imagem da webcam para reconhecimento em tempo real)*  
└── **README.md** *(documentação do projeto)*  

---

## **3. Passo a Passo do Projeto**  

### **3.1 Configuração do Ambiente**  
- Criar e ativar um ambiente virtual  
- Instalar dependências (`Django`, `OpenCV`, `face_recognition`, `dlib`)  

### **3.2 Criar a Aplicação Django**  
- Criar um novo projeto Django e configurar o banco de dados  
- Criar a API de cadastro de alunos (Django REST Framework)  
- Criar o modelo `Aluno` com nome, foto e codificação facial  

### **3.3 Criar Interface Web para Cadastro**  
- Criar página HTML para cadastro  
- Implementar upload de foto no formulário  
- Enviar a imagem para o backend e salvar no banco  

### **3.4 Implementar Reconhecimento Facial**  
- Criar script para capturar a imagem e extrair a face encoding  
- Criar verificação de rosto comparando com o banco de dados  
- Se a face for reconhecida, liberar a catraca  

### **3.5 Testar e Ajustar o Sistema**  
- Testar o cadastro de usuários  
- Testar o reconhecimento facial em tempo real  
- Ajustar precisão e velocidade do reconhecimento  

---

## **4. Melhorias Futuras** 🚀  9SUGESTÕES)
🔹 Criar integração com **RFID ou QR Code** para autenticação híbrida  
🔹 Implementar **dashboard de monitoramento** para visualização de acessos  
🔹 Otimizar o sistema para suportar maior número de usuários  

---

