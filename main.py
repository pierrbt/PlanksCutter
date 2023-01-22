from flask import * # Importer Flask pour créer une application web
from pyvpsolver.solvers import vbpsolver # Importer le module de résolution de problème de bin packing

app = Flask(__name__) # Créer une application web

@app.route('/') # Définir la route de la page d'accueil
def main(): # Définir la fonction qui sera appelée lors de l'arrivée sur la page d'accueil
    f = open('static/index.html', 'r') # Ouvrir le fichier index.html
    return f.read() # Retourner le contenu du fichier index.html

@app.route('/upload', methods=['GET', 'POST']) # Définir la route de la page d'upload
def upload(): # Définir la fonction qui sera appelée lors de l'arrivée sur la page d'upload
    data = request.json # Récupérer les données envoyées par le client
    longeurBasePlanche = int(data['longueurBasePlanche']) # Récupérer la longueur de la base des planches
    planksValues = data['planksToSend'] # Récupérer les valeurs des planches
    for plank in planksValues: # Pour chaque planche
        nbr = int(plank['nombrePlanche']) # Récupérer le nombre de planches
        lng = int(plank['longueurPlanche']) # Récupérer la longueur de la planche
    W = (longeurBasePlanche, 10) # Définir la longueur de la base des planches
    w = []  # Définir la liste des longueurs des planches
    b = [] # Définir la liste des nombres de planches
    for plank in planksValues: # Pour chaque planche
        nbr = int(plank['nombrePlanche']) # Récupérer le nombre de planches
        lng = int(plank['longueurPlanche']) # Récupérer la longueur de la planche
        w.append((lng, 1)) # Ajouter la longueur de la planche à la liste des longueurs des planches
        b.append(nbr) # Ajouter le nombre de planches à la liste des nombres de planches
    obj, lst_sol = vbpsolver.solve( # Résoudre le problème de bin packing
        W, w, b, script="vpsolver_glpk.sh", verbose=True # Utiliser le script vpsolver_glpk.sh pour résoudre le problème
    )
    print("Obj = ", obj) # Afficher l'objectif de coupe
    sol = lst_sol[0]  # Récupérer les solutions
    for row in sol: # Pour chaque solution
        cb = row[0] # Récupérer le nombre de planches à couper avec la pattern
        vals = row[1] # Récupérer les valeurs de la pattern
        pattern = [] # Définir la liste des valeurs de la pattern
        ch = "" # Définir la chaîne de caractères qui contiendra les valeurs de la pattern
        for val in vals: # Pour chaque valeur de la pattern
            pattern.append(w[val[0]][0]) # Ajouter la valeur de la pattern à la liste des valeurs de la pattern
            ch += str(w[val[0]][0]) + "cm " # Ajouter la valeur de la pattern à la chaîne de caractères
        print(cb, " planche(s) avec la pattern : ", ch) # Afficher le nombre de planches à couper avec la pattern et la pattern
    return 'ok' # Retourner ok