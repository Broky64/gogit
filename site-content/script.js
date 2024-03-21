// Fonction pour charger la liste des fichiers sur la page
async function loadFileList() {
    const response = await fetch('/files');
    const files = await response.json();

    const fileListElement = document.getElementById('file-list');
    fileListElement.innerHTML = ''; // Efface la liste actuelle des fichiers

    files.forEach(file => {
        const listItem = document.createElement('li');
        listItem.textContent = file;
        fileListElement.appendChild(listItem);
    });
}

// Charge la liste des fichiers au chargement de la page
document.addEventListener('DOMContentLoaded', loadFileList);

// Écouteur d'événement pour soumettre le formulaire
document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Empêche le formulaire de s'envoyer normalement

    const formData = new FormData(this); // Crée un objet FormData à partir du formulaire

    const response = await fetch('/uploads', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        // Rechargement de la liste des fichiers après l'upload réussi
        loadFileList();
    } else {
        console.error('Erreur lors de l\'upload du fichier');
    }
});
