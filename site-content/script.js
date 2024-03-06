document.getElementById('file-upload').addEventListener('change', function(event) {
    const fileList = event.target.files; 
    const fileListContainer = document.getElementById('library'); 

    for (const file of fileList) {
        const listItem = document.createElement('li'); 
        listItem.textContent = file.name; 

        const downloadLink = document.createElement('a'); 
        downloadLink.textContent = 'Télécharger'; 
        downloadLink.href = URL.createObjectURL(file); 
        downloadLink.setAttribute('download', file.name); 

        const deleteButton = document.createElement('button'); 
        deleteButton.textContent = 'Supprimer'; 
        deleteButton.addEventListener('click', function() {
            listItem.remove(); // Vous pouvez ajouter une logique pour supprimer côté serveur ici// Gestion de l'upload de fichiers
            document.getElementById('upload-form').addEventListener('submit', async function(event) {
                event.preventDefault(); // Empêche le formulaire de s'envoyer normalement
            
                const formData = new FormData(this); // Crée un objet FormData à partir du formulaire
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
            
            // Gestion de la suppression de fichiers
            document.querySelectorAll('.delete-button').forEach(button => {
                button.addEventListener('click', async function(event) {
                    const fileName = this.dataset.fileName;
                    const response = await fetch(`/delete/${fileName}`, {
                        method: 'DELETE'
                    });
            
                    if (response.ok) {
                        // Supprime l'élément de la bibliothèque une fois que le fichier est supprimé du serveur
                        this.parentNode.remove();
                    } else {
                        console.error('Erreur lors de la suppression du fichier');
                    }
                });
            });
            
        });

        listItem.appendChild(downloadLink); 
        listItem.appendChild(deleteButton); 

        fileListContainer.appendChild(listItem); 
    }
});
