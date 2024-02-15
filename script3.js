document.getElementById("registerForm").addEventListener("submit", function(event) {
    event.preventDefault(); // Empêcher l'envoi du formulaire par défaut

    // Récupérer les valeurs des champs nom d'utilisateur, email et mot de passe
    var username = document.getElementById("username").value;
    var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;

    // Valider les champs (exemple simplifié)
    var isValid = validateForm(username, email, password);

    if (isValid) {
        // Les champs sont valides, vous pouvez ajouter votre logique de création de compte ici
        // Par exemple, vous pouvez envoyer les données à votre serveur pour enregistrer le nouveau compte
        // Après la création du compte, vous pouvez rediriger l'utilisateur vers la page de connexion
        alert("Compte créé avec succès !");
        window.location.href = "user.html"; // Redirection vers la page de connexion
    } else {
        // Les champs ne sont pas valides
        alert("Veuillez remplir tous les champs correctement.");
    }
});

function validateForm(username, email, password) {
    // Fonction de validation simplifiée
    // Vous pouvez implémenter votre propre logique de validation ici
    // Par exemple, vérifier si l'email est dans un format valide, si le mot de passe est assez fort, etc.
    return username.trim() !== "" && email.trim() !== "" && password.trim() !== "";
}
