from flask import *
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)) + '/src')
from solver import calcul

app = Flask(__name__) # Créer une application web

@app.route('/') # Définir la route de la page d'accueil
def main(): # Définir la fonction qui sera appelée lors de l'arrivée sur la page d'accueil
    f = open('static/main.html', 'r') # Ouvrir le fichier index.html
    return f.read() # Retourner le contenu du fichier index.html


@app.route('/api/upload', methods=['POST'])
def upload():
    data = request.get_json()
    print(data)
    back = calcul(data)
    return jsonify(back)

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('./css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('./js', path)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('./static', 'favicon.ico')


if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)
