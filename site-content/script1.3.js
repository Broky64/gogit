document.addEventListener('DOMContentLoaded', function() {
    // Récupération des photos capturées depuis le stockage local
    const capturedPhotos = JSON.parse(localStorage.getItem('capturedPhotos'));

    // Affichage des photos sur la page
    const lastGameSection = document.getElementById('last-game');
    capturedPhotos.forEach(photoData => {
        const img = new Image();
        img.src = photoData;
        lastGameSection.appendChild(img);
    });
});
