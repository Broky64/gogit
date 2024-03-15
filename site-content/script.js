document.getElementById('upload-form').addEventListener('submit', async function(event) {
    event.preventDefault(); // Empêche le formulaire de s'envoyer normalement

    const formData = new FormData(this); // Crée un objet FormData à partir du formulaire
    formData.append('user_id', USER_ID); // Remplacer USER_ID par l'identifiant de l'utilisateur connecté
    const response = await fetch('/upload', {
        method: 'POST',
        body: formData
    });

    if (response.ok) {
        // Rechargement de la page pour mettre à jour la bibliothèque après l'upload
        location.reload();
    } else {
        console.error('Erreur lors de l\'upload du fichier');
    }
});
