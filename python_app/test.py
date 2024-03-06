from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route('/login', methods=['POST'])
def login():
    # Récupérer les données du formulaire de connexion envoyées par le frontend
    username = request.json.get('username')
    password = request.json.get('password')

    # Vérifier les identifiants (remplacez cette logique par votre propre vérification)
    if username == "admin" and password == "password":
        # Si l'authentification réussit, renvoyer l'URL de redirection
        return jsonify({'redirect_url': '/index.html'}), 200
    else:
        # Si l'authentification échoue, renvoyer un message d'erreur
        return jsonify({'message': 'Identifiants incorrects'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
