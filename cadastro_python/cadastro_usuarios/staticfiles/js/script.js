var contador = 0;

function abrirWebcam() {
    navigator.mediaDevices.getUserMedia({ video: true })
        .then(function(stream) {
            let video = document.getElementById('video');
            video.srcObject = stream;

            document.getElementById('capturar_Foto').disabled = false;
        })
        .catch(function(error) {
            console.log("Erro ao acessar webcam: ", error);
        });
}

function capturarFoto() {
    let video = document.getElementById('video');
    let canvas = document.getElementById('canvas');
    let contexto = canvas.getContext('2d');

    contador += 1;
    let timestamp = new Date().getTime(); 


    contexto.drawImage(video, 0, 0, canvas.width, canvas.height);

    canvas.toBlob(function(blob) {
        let fileName = "foto_" + contador + "_" + timestamp + ".png"; 
        let file = new File([blob], fileName, { type: "image/png" });

        let dataTransfer = new DataTransfer();
        dataTransfer.items.add(file);

        document.getElementById('id_foto').files = dataTransfer.files;
    }, "image/png");
}