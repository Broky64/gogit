from flask import Flask, request, send_from_directory
import os

app = Flask(__name__)

# Chemin absolu vers le répertoire de stockage des fichiers SGF
UPLOAD_FOLDER = '/chemin/vers/votre/repertoire/sgf'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/upload', methods=['POST'])
def upload_file():
    # Vérifier si la requête contient un fichier
    if 'file' not in request.files:
        return "Aucun fichier trouvé dans la requête", 400
    
    file = request.files['file']

    # Vérifier si le fichier a un nom
    if file.filename == '':
        return "Nom de fichier invalide", 400

    # Enregistrer le fichier dans le répertoire de stockage
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    
    return "Fichier téléchargé avec succès", 200

@app.route('/download/<path:filename>', methods=['GET'])
def download_file(filename):
    # Renvoyer le fichier demandé
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8080, debug=True)
