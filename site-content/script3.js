document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Empêcher l'envoi du formulaire par défaut

    // Récupérer les valeurs des champs nom d'utilisateur, email et mot de passe
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    // Valider les champs (exemple simplifié)
    var isValid = validateForm(username, email, password);

    if (isValid) {
        // Les champs sont valides, enregistrer les identifiants dans le stockage local
        var users = JSON.parse(localStorage.getItem("users")) || [];
        users.push({ username: username, email: email, password: password });
        localStorage.setItem("users", JSON.stringify(users));

        // Afficher un message de succès
        alert("Compte créé avec succès !");
        // Redirection vers la page de connexion
        window.location.href = "user.html";
    } else {
        // Les champs ne sont pas valides, afficher un message d'erreur
        alert("Veuillez remplir tous les champs correctement.");
    }
});

function validateForm(username, email, password) {
    // Fonction de validation simplifiée
    // Vous pouvez implémenter votre propre logique de validation ici
    // Par exemple, vérifier si l'email est dans un format valide, si le mot de passe est assez fort, etc.
    return username.trim() !== "" && email.trim() !== "" && password.trim() !== "";
}
