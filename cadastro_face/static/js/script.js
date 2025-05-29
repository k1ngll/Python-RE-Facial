// Referência ao botão de capturar foto
var btnCapturarFoto = document.getElementById("capturar_Foto");

// Desativa o botão de captura inicialmente
btnCapturarFoto.disabled = true;

/**
 * Função para abrir a webcam e exibir o vídeo ao vivo
 */
function abrirWebcam() {
    // Solicita permissão para acessar a câmera
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            // Define o stream da webcam como fonte do elemento de vídeo
            let video = document.getElementById('video');
            video.srcObject = stream;

            // Ativa o botão de capturar foto após a webcam estar ativa
            btnCapturarFoto.disabled = false;
        })
        .catch(function(error) {
            // Caso ocorra um erro ao acessar a webcam
            console.log("Erro ao acessar webcam: ", error);
        });
}

/**
 * Função para capturar a imagem atual da webcam
 */
function capturarFoto() {
    // Referência ao vídeo e ao canvas
    const video = document.getElementById("video");
    const canvas = document.getElementById("canvas");
    const context = canvas.getContext("2d");

    // Define o tamanho do canvas com base na resolução do vídeo
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;

    // Desenha o frame atual do vídeo no canvas
    context.drawImage(video, 0, 0, canvas.width, canvas.height);

    // Converte o conteúdo do canvas em uma imagem codificada em Base64 (formato PNG)
    const dataURL = canvas.toDataURL("image/png");

    // Armazena o Base64 em um input oculto (útil para enviar ao backend)
    document.getElementById("foto").value = dataURL;

    // Exibe uma mensagem de status indicando que a foto foi capturada
    const statusDiv = document.getElementById("fotoStatus");
    statusDiv.style.display = "block";

    // Oculta a mensagem de status após 3 segundos
    setTimeout(() => {
        statusDiv.style.display = "none";
    }, 3000);
}
