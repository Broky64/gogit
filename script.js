document.getElementById('file-upload').addEventListener('change', function(event) {
    const fileList = event.target.files; // Récupère la liste des fichiers sélectionnés
    const fileListContainer = document.getElementById('library'); // Récupère le conteneur de la liste des fichiers

    // Parcourt la liste des fichiers sélectionnés
    for (const file of fileList) {
        const listItem = document.createElement('li'); // Crée un élément li pour chaque fichier
        listItem.textContent = file.name; // Définit le contenu de l'élément li comme le nom du fichier
        fileListContainer.appendChild(listItem); // Ajoute l'élément li à la liste des fichiers
    }
});
