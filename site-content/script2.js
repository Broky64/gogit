document.addEventListener('DOMContentLoaded', function() {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function(event) {
        event.preventDefault(); // Empêche le formulaire de soumettre de manière traditionnelle

        // Récupération des valeurs du formulaire
        const email = document.getElementById('email').value;
        const password = document.getElementById('password').value;

        // Construction de l'objet data contenant les informations d'identification
        const userData = {
            username: email,
            password: password
        };

        // Envoi de la requête POST à l'application Flask
        fetch('http://192.168.1.11:5000/login', { // Remplacez 'localhost' par l'adresse IP de votre serveur si nécessaire
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData), // Conversion de l'objet userData en chaîne JSON
        })
        .then(response => response.json()) // Conversion de la réponse en JSON
        .then(data => {
            if (data.redirect_url) {
                console.log(data.redirect_url);
                console.log(data.redirect_url.replace("site-content/", ""));
                window.location.href = data.redirect_url;
            } 
            else {
                alert('Réponse du serveur : ' + data.message);
            }
        })
        .catch(error => {
            console.error('Erreur:', error);
            alert('Erreur lors de la connexion. Veuillez réessayer.'); // Affiche l'erreur sur la page
        });
    });
});

