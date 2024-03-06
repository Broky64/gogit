from flask import Flask, request, jsonify
import mysql.connector
from flask_cors import CORS


app = Flask(__name__)
CORS(app)
# Configuration de la connexion à la base de données MySQL
db = mysql.connector.connect(
    host="mysql",
    user="root",
    password="vivelego",
    database="govision"
)
# Route pour gérer la requête de connexion
@app.route('/login', methods=['POST'])
def login():
    # Récupérer les données du formulaire de connexion envoyées par le frontend
    username = request.json.get('username')
    password = request.json.get('password')

    # Créer un curseur pour exécuter des requêtes SQL
    cursor = db.cursor(dictionary=True)

    # Exécuter une requête SQL pour vérifier les identifiants dans la base de données
    cursor.execute('SELECT * FROM utilisateurs WHERE username = %s AND password = %s', (username, password))
    user = cursor.fetchone()
    cursor.close()

    if user:
        # Authentification réussie, retourner une réponse JSON
        return jsonify({'message': 'Authentification réussie','redirect_url': 'index.html'}), 200
    else:
        # Si les identifiants ne correspondent pas, retourner une réponse JSON d'erreur
        return jsonify({'message': 'Identifiants incorrects'}), 401

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)