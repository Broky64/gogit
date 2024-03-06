document.addEventListener('DOMContentLoaded', function() {
    const registerForm = document.getElementById('registerForm');

    registerForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Empêche le formulaire de soumettre de manière traditionnelle

        // Récupération des valeurs du formulaire
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Construction de l'objet data contenant les informations d'inscription
        const userData = {
            email: email,
            password: password
        };

        // Envoi de la requête POST à l'application Flask pour créer un compte
        fetch('http://192.168.1.11:5000/register', { // Remplacez l'URL par celle de votre serveur
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData), // Conversion de l'objet userData en chaîne JSON
        })
        .then(response => response.json()) // Conversion de la réponse en JSON
        .then(data => {
            console.log(data); // Affiche la réponse du serveur dans la console
            alert('Réponse du serveur : ' + data.message); // Affiche la réponse du serveur dans une alerte
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de la création du compte. Veuillez réessayer.'); // Affiche l'erreur sur la page
        });
    });
});
