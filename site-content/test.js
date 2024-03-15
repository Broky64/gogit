const video = document.getElementById('video');

if (navigator.mediaDevices.getUserMedia) {
    navigator.mediaDevices.getUserMedia({ video: true })
    .then(function(stream) {
        // Associer le flux vidéo à l'élément <video>
        video.srcObject = stream;
    })
    .catch(function(err) {
        console.log("Une erreur est survenue : " + err);
    });
}
