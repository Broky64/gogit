from flask import Flask
from flask_cors import CORS


app = Flask(__name__)
CORS(app)  # Active CORS pour toutes les routes, ajustez selon besoin

@app.route('/test', methods=['GET'])
def test():
    return 'Oui'

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)