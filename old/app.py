from flask import * # Importer Flask pour créer une application web
from pyvpsolver.solvers import vbpsolver # Importer le module de résolution de problème de bin packing

app = Flask(__name__) # Créer une application web

@app.route('/') # Définir la route de la page d'accueil
def main(): # Définir la fonction qui sera appelée lors de l'arrivée sur la page d'accueil
    f = open('index.html', 'r') # Ouvrir le fichier index.html
    return f.read() # Retourner le contenu du fichier index.html

@app.route('/upload', methods=['POST']) # Définir la route de la page d'upload
def upload(): # Définir la fonction qui sera appelée lors de l'arrivée sur la page d'upload
    backJson = dict();
    backJson['success'] = True
    backJson['message'] = "OK"
    try:
        data = request.json  # Récupérer les données envoyées par le client
        longeurBasePlanche = int(data['longueurBasePlanche']) # Récupérer la longueur de la base des planches

        backJson['baseSize'] = longeurBasePlanche # Ajouter la longueur de la base des planches au json de retour
        planksValues = data['planksToSend'] # Récupérer les valeurs des planches

        W = (longeurBasePlanche, 10) # Définir la longueur de la base des planches
        w = []  # Définir la liste des longueurs des planches
        b = [] # Définir la liste des nombres de planches

        for plank in planksValues: # Pour chaque planche
            nbr = int(plank['nombrePlanche']) # Récupérer le nombre de planches
            lng = int(plank['longueurPlanche']) # Récupérer la longueur de la planche
            w.append((lng, 1)) # Ajouter la longueur de la planche à la liste des longueurs des planches
            b.append(nbr) # Ajouter le nombre de planches à la liste des nombres de planches

        obj, lst_sol = vbpsolver.solve( # Résoudre le problème de bin packing
        W, w, b, script="vpsolver_glpk.sh", verbose=False # Utiliser le script vpsolver_glpk.sh pour résoudre le problème
        )
        backJson['objective'] = obj # Ajouter l'objectif au json de retour
        backJson['planks'] = [] # Ajouter la liste des planches au json de retour
        sol = lst_sol[0]  # Récupérer les solutions
        for row in sol: # Pour chaque solution
            cb = row[0] # Récupérer le nombre de planches à couper avec la pattern
            vals = row[1] # Récupérer les valeurs de la pattern
            pattern = [] # Définir la liste des valeurs de la pattern
            for val in vals: # Pour chaque valeur de la pattern
                pattern.append(w[val[0]][0]) # Ajouter la valeur de la pattern à la liste des valeurs de la pattern
            backJson['planks'].append({'nbr': cb, 'pattern': pattern}) # Ajouter la pattern au json de retour
    except Exception as e: # Si une erreur est survenue
        print("[ERROR] : " + str(e)) # Afficher l'erreur
        backJson['message'] = str(e) # Ajouter le message d'erreur au json de retour
        backJson['success'] = False # Ajouter l'erreur au json de retour

    return jsonify(backJson) # Retourner le json de retour

# Send the files from css, js and static folders

@app.route('/css/<path:path>')
def send_css(path):
    return send_from_directory('../css', path)

@app.route('/js/<path:path>')
def send_js(path):
    return send_from_directory('../js', path)

@app.route('/favicon.ico')
def favicon():
    return send_from_directory('../static', 'favicon.ico')