document.addEventListener('DOMContentLoaded', function () {
    const loginForm = document.getElementById('loginForm');

    loginForm.addEventListener('submit', function (event) {
        event.preventDefault(); // Empêche le formulaire de soumettre de manière traditionnelle

        // Récupération des valeurs du formulaire
        var email = document.getElementById('email').value;
        var password = document.getElementById('password').value;

        // Envoi de la requête POST à l'application Flask
        axios.post('http://192.168.1.11:5000/test', { // Assurez-vous que l'URL est correcte et pointe vers votre route Flask
            username: email,
            password: password
        })
        .then(function (response) {
            console.log(response.data); // Affiche la réponse du serveur dans la console
            alert('Réponse du serveur : ' + response.data); // Affiche la réponse du serveur dans une alerte
        })
        .catch(function (error) {
            console.error('Erreur:', error);
            alert('Erreur lors de la connexion. Veuillez réessayer.');
        });
    });
});
