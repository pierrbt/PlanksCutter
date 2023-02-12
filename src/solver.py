from datetime import datetime

from pyvpsolver.solvers import vbpsolver
import time
import threading

def checkInData(cuts):
    l = []
    q = []

    for i in cuts["sizes"]:
        if (type(i) != int):
            continue
        else:
            l.append((i,))
    for j in cuts["quantity"]:
        if (type(j) != int):
            continue
        else:
            q.append(j)
    return l, q

def startJson():
    json = {}
    json["success"] = True
    json["message"] = "Calculs effectués avec succès"
    json["results"] = {}
    json["execution_time"] = "0ms"
    json["exports"] = {
        "direct" : "#"
    }
    return json

def solver(k, l, q, back):
    B = (k,)
    objective, list_solutions = vbpsolver.solve(B, l, q, script="vpsolver_glpk.sh", verbose=False)
    list_solutions = list_solutions[0]

    longueurBrute = objective * k
    longueurNette = 0

    back["results"][k] = {
        "statistics": {
            "objective": objective
        },
        "patterns": [],
        "quantity": [],
        "csv": ""
    }

    for row in list_solutions:  # Pour chaque solution
        cb = row[0]  # Récupérer le nombre de planches à couper avec la pattern
        back["results"][k]["quantity"].append(cb)

        vals = row[1]  # Récupérer les valeurs de la pattern
        back["results"][k]["patterns"].append([])
        index = len(back["results"][k]["patterns"]) - 1
        for val in vals:  # Pour chaque valeur de la pattern
            back["results"][k]["patterns"][index].append(l[val[0]][0])

        longueurNette += cb * sum(back["results"][k]["patterns"][index])

    back["results"][k]["statistics"]["brut"] = longueurBrute
    back["results"][k]["statistics"]["net"] = longueurNette
    back["results"][k]["statistics"]["loss_unit"] = longueurBrute - longueurNette
    back["results"][k]["statistics"]["loss_percent"] = round(((longueurBrute - longueurNette) / longueurBrute) * 100, 2)

    # On doit créer un fichier CSV pour chaque planche qui ressemble à ça :
    """
    Résultats pour la planche de : ;;;5000;;;;;;
;;;;;;;;;
Statistiques :;;;;;;;;;
Perte (%);12%;;;;;;;;
Perte (u);450;;;;;;;;
Utilisé;6500;;;;;;;;
Totale;6950;;;;;;;;
;;;;;;;;;
Coupes :;Nombre de coupes;Longueurs;;;;;;;
;20;10;20;30;500;420;590;;
;12;106;54;87;21;36;;;
;90;204;6;2;4;94;62;418;18
;;;;;;;;;
Exporté par PlanksCutter, le 06/05/2023;;;;;;;;;
"""
    back["results"][k]["csv"] = "Resultats pour la planche de : ;;;" + str(k) + ";;;;;;\n"
    back["results"][k]["csv"] += ";;;;;;;;;\n"
    back["results"][k]["csv"] += "Statistiques :;;;;;;;;;\n"
    back["results"][k]["csv"] += "Perte (%);" + str(back["results"][k]["statistics"]["loss_percent"]) + "%;;;;;;;\n"
    back["results"][k]["csv"] += "Perte (u);" + str(back["results"][k]["statistics"]["loss_unit"]) + ";;;;;;;\n"
    back["results"][k]["csv"] += "Utilise;" + str(back["results"][k]["statistics"]["net"]) + ";;;;;;;\n"
    back["results"][k]["csv"] += "Totale;" + str(back["results"][k]["statistics"]["brut"]) + ";;;;;;;\n"
    back["results"][k]["csv"] += ";;;;;;;;;\n"
    back["results"][k]["csv"] += "Coupes :;Nombre de coupes;Longueurs;;;;;;;\n"


    # On met chaque quantity de coupes et toutes les longueurs de chaque pattern
    for i in range(len(back["results"][k]["quantity"])):
        back["results"][k]["csv"] += ";" + str(back["results"][k]["quantity"][i])
        for j in range(len(back["results"][k]["patterns"][i])):
            back["results"][k]["csv"] += ";" + str(back["results"][k]["patterns"][i][j])
        back["results"][k]["csv"] += ";\n"



    back["results"][k]["csv"] += ";;;;;;;;;\n"

    current_datetime = datetime.now()
    current_date_time = current_datetime.strftime("%m/%d/%Y, %H:%M")

    back["results"][k]["csv"] += "Export par PlanksCutter, le " + str(current_date_time) + ";;;;;;;;;\n"


def calcul(jsonData):
    start_time = time.time()
    back = startJson()
    try:
        cuts = jsonData["cuts"]
        planks = jsonData["planks"]

        l, q = checkInData(cuts)

        if (
                (len(l) != len(q)) or
                (len(l) == 0) or
                (len(q) == 0)
        ):
            raise ValueError("Les valeurs rentrées sont incorrectes. Veuillez réessayer avec des nombres entiers.")

        workers = []
        for k in planks:
            if (k < max(l)[0]):
                raise ValueError("Les coupes ne peuvent pas êtres plus petites que la planche !")
            workers.append(
                threading.Thread(target=solver, args=(k, l, q, back))
            )
        for m in range(len(workers)):
            workers[m].start()
        for m in range(len(workers)):
            workers[m].join()




    except Exception as e:
        print("[ERROR] : ", str(e))
        back["success"] = False
        back["message"] = str(e)

    end_time = time.time()
    duration = round(((end_time - start_time) * 1000), 1)
    print("Runtime : ", duration, " ms")
    back["execution_time"] = str(duration) + " ms"

    return back