from pyvpsolver.solvers import vbpsolver
from flask import *
import time
import threading


def checkInData(cuts):
    l = []
    q = []

    for i in cuts["sizes"]:
        if (type(i) != int):
            continue
        else:
            l.append((i, 1))
    for j in cuts["quantity"]:
        if (type(j) != int):
            continue
        else:
            q.append(j)

    print("Longueurs : ", l)
    print("Quantités : ", q)
    return l, q

def startJson():
    json = {}
    json["success"] = True
    json["message"] = "Calculs effectués avec succès"
    json["results"] = {}
    json["execution_time"] = "0ms"
    json["exports"] = []
    return json

def solver(k, l, q, back):
    B = (k, 9)
    objective, list_solutions = vbpsolver.solve(B, l, q, script="vpsolver_glpk.sh", verbose=False)
    print("Avec longueur ", k, ", objectif : ", objective)
    back["results"][k] = {
        "statistics": {
            "objectif": objective
        }
    }

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
    print("JSON : ", back)
    return


def start():
    json = {
        "cuts":
            {
                "sizes":
                    [
                        482, 299, 239, 392, 129, 500, 23
                    ],
                "quantity":
                    [
                        3832, 3841, 2842, 11930, 8294, 2033, 2839
                    ]
            },
        "planks":
            [
                2000, 5000, 2000, 1000, 500
            ],
        "cutSize": 2,
        "export":
            {
                "direct": True,
                "pdf": False,
                "csv": False
            }
    }
    calcul(json)
    return


if __name__ == "__main__":
    start()