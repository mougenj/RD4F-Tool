import App
from PyQt5.QtWidgets import QApplication
import random as rd
import json
import sip
import sys
sip.setdestroyonexit(True)


def create_json_example():
    data = []
    # ajout de données "sensées"
    data.append(["D", [1, 6]])
    data.append(["S", [1, 6]])
    alphabet_latin = [chr(x) for x in range(ord('a'), ord('z') + 1)]
    # ecriture de 5 nom au hasard de 9 caractere de long
    liste_nom_equation = []
    for _ in range(5):
        nom = "".join([rd.choice(alphabet_latin) for _ in range(9)])
        liste_nom_equation.append(nom)
    for nom in liste_nom_equation:
        data.append((nom, [rd.randint(0, 50) for _ in range(rd.randint(1, 5))]))
    chaine = json.dumps(data, indent=4)
    with open("ressources/json.txt", "w") as fichier:
        fichier.write(chaine)

# todo:
# revoir le json et y ajouter des paramètres
# ajouter un champs de recherche des valeurs sur le graphes en fonction de l'abscisse (qu'en est-il de s'il y a plusieurs courbes?)
# lire le matlab founi par le client
# gérer la fermeture des onglets et leurs conséquances sur le graphe
# gérer le drag and drop (avertir l'utilisateur si il y a un fichier mal chargé)
# enlever le chargement automatique du json au lancement
# nettoyer les import
# ne plus pouvoir modifer les box dans l'onglet lecture
if __name__ == '__main__':
    create_json_example()
    #print("création de l'interface")
    #print(sys.argv)
    app = QApplication(sys.argv)
    #print("lancement de l'interface")
    ex = App.App()
    #print("sortie de l'interface")
    rc = app.exec_()
    #print("sortie prog")
    del app
    sys.exit(rc)
