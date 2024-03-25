// Fonction pour démarrer ou quitter la caméra
function toggleCamera() {
    const cameraFeed = document.getElementById('camera-feed');
    const video = document.getElementById('video');

    if (!cameraFeed.contains(video)) {
        // Demander l'autorisation à l'utilisateur d'accéder à la caméra
        navigator.mediaDevices.getUserMedia({ video: true })
            .then(function(stream) {
                // Autorisation accordée, démarrer la caméra
                cameraFeed.innerHTML = '<video id="video" width="400" height="300" autoplay></video>';
                video.srcObject = stream;
                // Afficher les boutons de capture et quitter la caméra
                document.getElementById('capture-photo-button').style.display = 'inline-block';
                document.getElementById('quit-camera-button').style.display = 'inline-block';
                // Cacher le bouton New Game
                document.querySelector('.new-game-button').style.display = 'none';
                // Charger les photos précédemment enregistrées
                loadLastGamePhotos();
            })
            .catch(function(err) {
                // L'utilisateur a refusé l'accès ou une erreur est survenue
                console.log("Impossible d'accéder à la caméra: " + err);
            });
    } else {
        // Arrêter la caméra
        const stream = video.srcObject;
        const tracks = stream.getTracks();

        tracks.forEach(function(track) {
            track.stop();
        });

        // Supprimer la vidéo de la zone de la caméra
        cameraFeed.innerHTML = '';

        // Cacher les boutons de capture et quitter la caméra
        document.getElementById('capture-photo-button').style.display = 'none';
        document.getElementById('quit-camera-button').style.display = 'none';
        // Afficher le bouton New Game
        document.querySelector('.new-game-button').style.display = 'inline-block';
    }
}

// Fonction pour capturer une photo
function capturePhoto() {
    const video = document.getElementById('video');
    const canvas = document.createElement('canvas');
    canvas.width = video.videoWidth;
    canvas.height = video.videoHeight;
    const context = canvas.getContext('2d');
    context.drawImage(video, 0, 0, canvas.width, canvas.height);
    const imageData = canvas.toDataURL('image/png');

    // Stockage local de l'image capturée
    if (!localStorage.getItem('capturedPhotos')) {
        localStorage.setItem('capturedPhotos', JSON.stringify([]));
    }
    const capturedPhotos = JSON.parse(localStorage.getItem('capturedPhotos'));
    capturedPhotos.push(imageData);
    localStorage.setItem('capturedPhotos', JSON.stringify(capturedPhotos));

    // Mettre à jour l'affichage des photos dans la page Last Game
    loadLastGamePhotos();
}

// Fonction pour charger les photos précédemment enregistrées dans la page Last Game
function loadLastGamePhotos() {
    const photoContainer = document.getElementById('last-game-photos');
    photoContainer.innerHTML = ''; // Efface les photos précédentes

    const capturedPhotos = JSON.parse(localStorage.getItem('capturedPhotos')) || [];
    capturedPhotos.forEach(photoData => {
        const img = new Image();
        img.src = photoData;
        photoContainer.appendChild(img);
    });
}
