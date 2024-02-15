document.getElementById("loginForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Empêcher l'envoi du formulaire par défaut

    // Récupérer les valeurs des champs email et mot de passe
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    // Vérifier les identifiants (simulation)
    var credentialsValid = checkCredentials(email, password);

    if (credentialsValid) {
        // Les identifiants sont valides, rediriger l'utilisateur vers la page index.html
        window.location.href = "index.html";
    } else {
        // Les identifiants ne sont pas valides, rediriger l'utilisateur vers la page de création de compte
        window.location.href = "creecompte.html";
    }
});

function checkCredentials(email, password) {
    // Simulation : vérification si les identifiants sont dans une liste prédéfinie
    var validEmails = ["utilisateur1@example.com", "utilisateur2@example.com", "utilisateur2@example.fr"];
    var validPasswords = ["motdepasse1", "motdepasse2"];

    // Vérifier si les identifiants sont dans la liste prédéfinie
    for (var i = 0; i < validEmails.length; i++) {
        if (email === validEmails[i] && password === validPasswords[i]) {
            return true; // Identifiants valides
        }
    }

    return false; // Identifiants non valides
}
