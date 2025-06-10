import cv2
import time
import face_recognition
import os
import sqlite3
import datetime

# --- DATABASE CONFIGURATION ---
# Get the directory of the current script (where db.sqlite3 is also located)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_NAME = os.path.join(BASE_DIR, 'db.sqlite3')

print(f"🔄 Conectando ao banco de dados em: {DB_NAME}") # For initial debugging

def get_db_connection():
    """Establishes a connection to the SQLite database and sets row_factory."""
    try:
        conn = sqlite3.connect(DB_NAME)
        conn.row_factory = sqlite3.Row # Allows accessing columns by name
        return conn
    except sqlite3.Error as e:
        print(f"❌ ERRO CRÍTICO: Não foi possível conectar ao banco de dados em '{DB_NAME}': {e}")
        print("Certifique-se de que o arquivo 'db.sqlite3' existe e está no mesmo diretório do script.")
        exit() # Exits the program if it cannot connect to the DB

# --- DIRECTORY CONFIGURATION ---
# 'media' will be created as a subdirectory in the same location as the script
output_dir = os.path.join(BASE_DIR, "media", "fotos")
banco_faces_dir = os.path.join(BASE_DIR, "media", "fotos_usuarios")

os.makedirs(output_dir, exist_ok=True)
os.makedirs(banco_faces_dir, exist_ok=True) # Ensures the user photos folder also exists

print(f"📁 Pasta de fotos salvas: {output_dir}")
print(f"📁 Pasta de rostos autorizados: {banco_faces_dir}")

# --- HELPER FUNCTIONS ---

# ID for unknown/error users (YOU MUST CREATE THIS USER IN THE 'cadastro_face_usuario' TABLE)
# For example, a record with id=1 and nome='DESCONHECIDO'
ID_USUARIO_DESCONHECIDO_OU_ERRO = 1 # <--- ADJUST THIS ID TO YOUR WILDCARD USER ID

def get_usuario_id_by_name(nome_usuario_completo):
    """
    Retrieves the user ID and curso_id from the 'cadastro_face_usuario' table based on the user's name.
    Adjusts the name to remove common suffixes like '_foto' before querying.
    
    Args:
        nome_usuario_completo (str): The full name from the recognized photo (e.g., 'Gustavo_Cerqueira_foto').
        
    Returns:
        tuple: A tuple containing (user_id, curso_id) if found, (None, None) otherwise.
    """
    conn = None
    usuario_id = None
    curso_id = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        nome_para_busca = nome_usuario_completo.replace('_foto', '')
        
        cursor.execute("SELECT id, curso_id FROM cadastro_face_usuario WHERE nome = ?", (nome_para_busca,))
        result = cursor.fetchone()
        if result:
            usuario_id = result['id']
            curso_id = result['curso_id']
    except sqlite3.Error as e:
        print(f"❌ Erro ao buscar ID e curso_id do usuário na tabela 'cadastro_face_usuario': {e}")
    finally:
        if conn:
            conn.close()
    return usuario_id, curso_id

def dia_semana():
    data_atual = datetime.datetime.now()
    dia_da_semana_numero = data_atual.weekday()

    dias_da_semana = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
    nome_dia_da_semana = dias_da_semana[dia_da_semana_numero]
    
    # DEBUG PRINT: Verify the day of the week
    print(f"DEBUG: dia_semana() retornou: '{nome_dia_da_semana}'") 
    
    return nome_dia_da_semana

def busca_sala(curso_id):
    """
    Busca a sala e o horário na tabela gestor_gradehoraria para um dado curso_id e dia da semana.
    Retorna APENAS a sala.
    """
    if curso_id is None:
        print("DEBUG: busca_sala chamada com curso_id=None.")
        return "Funcionario"

    sala = 'N/A' # Valor padrão caso não encontre
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        dia_da_semana = dia_semana() # Get the day of the week

        sql = """
            SELECT sala
            FROM gestor_gradehoraria 
            WHERE curso_id = ? AND dia_semana = ?
        """
        # DEBUG PRINT: Verify parameters before execution
        print(f"DEBUG: Executando busca_sala com: curso_id={curso_id}, dia_semana='{dia_da_semana}'")
        
        cursor.execute(sql, (curso_id, dia_da_semana))
        result = cursor.fetchone()
        
        if result:
            sala = result['sala']
            print(f"DEBUG: Sala encontrada: {sala}")
        else:
            print(f"⚠️ Nenhuma sala encontrada para curso ID {curso_id} no dia {dia_da_semana}.")

    except sqlite3.Error as e:
        print(f"❌ Erro ao buscar sala na grade horária: {e}")
    finally:
        if conn:
            conn.close()

    return sala
    

def inserir_registro_acesso_db(nome_reconhecido, status_acesso_bool, usuario_id, sala_atual="N/A"):
    """
    Inserts an access record into the 'gestor_registroacesso' table.
    
    Args:
        nome_reconhecido (str): The name of the person recognized (or 'DESCONHECIDO', 'ERRO_DETECCAO').
        status_acesso_bool (bool): True for granted access (entry), False for denied/error.
        usuario_id (int): The ID of the user (must be an integer, including the ID_USUARIO_DESCONHECIDO_OU_ERRO).
        sala_atual (str): The room associated with the access. Defaults to "N/A".
    """
    conn = None
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        
        sql = """
            INSERT INTO gestor_registroacesso 
            (usuario_id, sala, horario_entrada, status) 
            VALUES (?, ?, DATETIME('now', 'localtime'), ?) 
        """
        
        cursor.execute(sql, (usuario_id, sala_atual, status_acesso_bool))
        conn.commit()
        print(f"✅ Registro de acesso para '{nome_reconhecido}' (ID: {usuario_id}) com status '{status_acesso_bool}' na sala '{sala_atual}' inserido na tabela 'gestor_registroacesso'.")
    except sqlite3.Error as e:
        print(f"❌ Erro ao inserir registro de acesso na tabela 'gestor_registroacesso': {e}")
    finally:
        if conn:
            conn.close()

def carregar_rostos_autorizados(diretorio):
    """
    Loads known face encodings and names from the specified directory.
    
    Args:
        diretorio (str): Path to the directory containing authorized face images.
        
    Returns:
        tuple: A tuple containing a list of face encodings and a list of corresponding names.
    """
    encodings = []
    nomes = []
    print(f"🔄 Tentando carregar rostos autorizados de: {diretorio}")
    if not os.path.exists(diretorio):
        print(f"❌ Diretório de rostos autorizados não encontrado: {diretorio}")
        return encodings, nomes
        
    for nome_arquivo in os.listdir(diretorio):
        caminho = os.path.join(diretorio, nome_arquivo)
        if not os.path.isfile(caminho): # Skip if it's not a file
            continue
        try:
            imagem = face_recognition.load_image_file(caminho)
            encodings_na_imagem = face_recognition.face_encodings(imagem)
            if encodings_na_imagem:
                encoding = encodings_na_imagem[0] # Get the first face encoding
                encodings.append(encoding)
                nomes.append(os.path.splitext(nome_arquivo)[0]) # Get name without extension (e.g., 'Gustavo_Cerqueira_foto')
                print(f"✅ Carregado: {nome_arquivo}")
            else:
                print(f"⚠️ Nenhum rosto encontrado em {nome_arquivo} para encoding, ignorando.")
        except Exception as e:
            print(f"⚠️ Erro ao carregar ou processar '{nome_arquivo}': {e}")
    print(f"ℹ️ Total de rostos autorizados carregados: {len(nomes)}")
    return encodings, nomes

# --- INITIALIZATION ---

# Load authorized faces from the specified directory
rostos_autorizados, nomes_autorizados = carregar_rostos_autorizados(banco_faces_dir)

# Initialize OpenCV's Haar Cascade classifier for face detection
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
# Open the default camera (usually index 0)
video_capture = cv2.VideoCapture(0)

# --- NEW: Set window to fullscreen and hide toolbar ---
# Define o nome da janela antes de mostrar (importante para setWindowProperty)
window_name = "Reconhecimento Facial - Pressione 'q' para sair"
cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
# Define a propriedade da janela para fullscreen
cv2.setWindowProperty(window_name, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
# Define a propriedade para esconder a barra de ferramentas/bordas (opcional, mas recomendado para fullscreen)
cv2.setWindowProperty(window_name, cv2.WND_PROP_AUTOSIZE, cv2.WINDOW_AUTOSIZE)
# --- END NEW ---


def detect_bounding_box(vid):
    """
    Detects faces in a given video frame using the Haar Cascade classifier.
    
    Args:
        vid (numpy.ndarray): The video frame (image).
        
    Returns:
        list: A list of bounding boxes for detected faces (x, y, w, h).
    """
    gray_image = cv2.cvtColor(vid, cv2.COLOR_BGR2GRAY)
    faces = face_classifier.detectMultiScale(gray_image, 1.1, 5, minSize=(40, 40))
    return faces

# --- STATE VARIABLES FOR LOGIC CONTROL ---
tem_face = None          
tirou_foto = False       
mensagem = ""            
mensagem_mostrada_em = 0 
tempo_mensagem = 6       

# --- MAIN LOOP ---
while True:
    resultado, janela = video_capture.read()
    if resultado is False:
        print("❌ Não foi possível ler o frame da câmera. Verifique a conexão da câmera.")
        break

    faces = detect_bounding_box(janela)

    if len(faces) > 0:
        if tem_face is None:
            tem_face = time.time()
        else:
            elapsed_time = time.time() - tem_face
            if elapsed_time >= 5 and not tirou_foto:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename_local = f"foto_{timestamp}.jpg"
                caminho_completo_foto_salva = os.path.join(output_dir, filename_local)
                
                caminho_foto_para_db = os.path.join("fotos", filename_local) 

                cv2.imwrite(caminho_completo_foto_salva, janela)
                print(f"Foto salva em: {caminho_completo_foto_salva}")
                tirou_foto = True

                try:
                    img = face_recognition.load_image_file(caminho_completo_foto_salva)
                    encodings_na_img = face_recognition.face_encodings(img)

                    if encodings_na_img:
                        encoding_img = encodings_na_img[0]
                        resultados = face_recognition.compare_faces(rostos_autorizados, encoding_img)
                        print("Resultado da comparação: ", resultados)

                        if True in resultados:
                            index = resultados.index(True)
                            nome_pessoa_foto = nomes_autorizados[index] # Name as it is in the file (e.g., 'Gustavo_Cerqueira_foto')
                            
                            # Tenta obter o ID do usuário E o curso_id
                            usuario_id, curso_id = get_usuario_id_by_name(nome_pessoa_foto)
                            
                            print(f"DEBUG: Após get_usuario_id_by_name: usuario_id={usuario_id}, curso_id={curso_id}")
                            
                            if usuario_id is not None: # Verifica se o ID foi encontrado no DB
                                sala_do_acesso = busca_sala(curso_id) # Passa o curso_id para busca_sala
                                mensagem = f"BEM VINDO: {nome_pessoa_foto.upper().replace('_FOTO', '')} - {sala_do_acesso}"
                                inserir_registro_acesso_db(
                                    nome_reconhecido=nome_pessoa_foto.replace('_foto', ''),
                                    status_acesso_bool=True,
                                    usuario_id=usuario_id,
                                    sala_atual=sala_do_acesso
                                )
                            else:
                                print(f"⚠️ Usuário '{nome_pessoa_foto}' reconhecido, mas ID não encontrado na tabela 'cadastro_face_usuario'. Usando ID curinga.")
                                mensagem = f"⚠️ ACESSO LIBERADO ({nome_pessoa_foto.upper().replace('_FOTO', '')}, ID NÃO ENCONTRADO)"
                                sala_do_acesso = busca_sala(None) # Passa None se o curso_id não foi encontrado
                                inserir_registro_acesso_db(
                                    nome_reconhecido=nome_pessoa_foto.replace('_foto', ''),
                                    status_acesso_bool=True, # Still true if face recognized and access granted
                                    usuario_id=ID_USUARIO_DESCONHECIDO_OU_ERRO,
                                    sala_atual="N/A (ID não encontrado)"
                                )

                        else: # Face not recognized
                            mensagem = "⛔ ACESSO NEGADO"
                            inserir_registro_acesso_db(
                                nome_reconhecido="DESCONHECIDO",
                                status_acesso_bool=False,
                                usuario_id=ID_USUARIO_DESCONHECIDO_OU_ERRO,
                                sala_atual="N/A (Acesso Negado)"
                            )
                    else: # No faces in the newly captured image for recognition
                        print("Erro: Nenhum rosto para reconhecimento na imagem recém-tirada.")
                        mensagem = "⛔ FACE NÃO DETECTADA PARA RECONHECIMENTO"
                        inserir_registro_acesso_db(
                            nome_reconhecido="ERRO_DETECCAO",
                            status_acesso_bool=False,
                            usuario_id=ID_USUARIO_DESCONHECIDO_OU_ERRO,
                            sala_atual="N/A (Erro de Detecção)"
                        )

                except Exception as e:
                    print(f"Erro inesperado durante o reconhecimento: {e}")
                    mensagem = "⛔ ERRO NO RECONHECIMENTO"
                    inserir_registro_acesso_db(
                        nome_reconhecido="ERRO_INESPERADO",
                        status_acesso_bool=False,
                        usuario_id=ID_USUARIO_DESCONHECIDO_OU_ERRO,
                        sala_atual="N/A (Erro Inesperado)"
                    )

                mensagem_mostrada_em = time.time()

    else: # No face detected in the camera window
        tem_face = None
        if mensagem and (time.time() - mensagem_mostrada_em >= tempo_mensagem):
            mensagem = ""
            tirou_foto = False

    # Display the message on the screen
    if mensagem:
        tempo_exibido = time.time() - mensagem_mostrada_em
        if tempo_exibido < tempo_mensagem:
            cor = (0, 255, 0) if "BEM VINDO" in mensagem or "ACESSO LIBERADO" in mensagem else (0, 0, 255)
            
            # --- NEW: Calculate text position for centering and draw background ---
            text_size = cv2.getTextSize(mensagem, cv2.FONT_HERSHEY_SIMPLEX, 1, 3)[0]
            # Center horizontally, position at bottom with 50 pixels margin
            text_x = (janela.shape[1] - text_size[0]) // 2 
            text_y = janela.shape[0] - 50 
            
            # Draw a black rectangle as background for the message
            cv2.rectangle(janela, 
                          (text_x - 10, text_y - text_size[1] - 10), 
                          (text_x + text_size[0] + 10, text_y + 10), 
                          (0, 0, 0), # Black color
                          cv2.FILLED) # Fill the rectangle
            # --- END NEW ---

            cv2.putText(
                janela,
                mensagem,
                (text_x, text_y), # Use calculated position
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                cor,
                3,
            )
        else: # Clear the message after tempo_mensagem
            mensagem = ""
            tem_face = None
            tirou_foto = False

    # Draw rectangles around detected faces
    for (x, y, w, h) in faces:
        cv2.rectangle(janela, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow(window_name, janela) # Use the named window

    # Check if 'q' key was pressed to exit
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# --- CLEANUP ---
video_capture.release()
cv2.destroyAllWindows()