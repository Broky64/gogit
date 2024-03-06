document.addEventListener('DOMContentLoaded', function() {
    // Accéder au formulaire d'inscription par son ID
    const registerForm = document.getElementById('registerForm');

    // Ajouter un écouteur d'événements pour la soumission du formulaire
    registerForm.addEventListener('submit', function(event) {
        // Empêcher le formulaire de se soumettre de la manière traditionnelle
        event.preventDefault();

        // Récupérer les valeurs saisies dans le formulaire
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Préparer l'objet data avec les informations de l'utilisateur
        const userData = {
            email: email,
            password: password
        };
        console.log("Sending user data:", JSON.stringify(userData));

        // Envoyer la requête POST à l'application Flask pour créer un compte
        fetch('http://192.168.1.11:5000/register', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        })
        .then(response => {
            console.log("Raw Server Response:", response);
            if (!response.ok) {
                return response.text()  // ou response.json(), selon le type de réponse attendu
                .then(text => { throw new Error(`Network response was not ok: ${response.statusText}. Body: ${text}`); });
            }
            return response.json();
        })
        
        .then(data => {
            console.log("Processed Server Data:", data);
            alert('Réponse du serveur : ' + data.message);
        })
        .catch(error => {
            console.error('Error during Fetch request:', error);
            alert('Erreur lors de la création du compte. Veuillez réessayer.');
        });

        
    });
});
