import pickle
import os
import Projet_mastermind_graphique
import random
import Class

class IA:

    def __init__(self) -> None:
        self.poids = {}

        if os.path.exists("donnees.pkl"):
             self.charger()

        else:
            self.creer_possibilite()
            self.sauvegarder()
        
 
    def charger(self) -> None:
        
        with open("donnees.pkl", "rb") as fichier :
            self.poids = pickle.load(fichier)
        
    def creer_possibilite(self) -> None:
        for c1 in range(6):
            for c2 in range(6):
                for c3 in range(6):
                    for c4 in range (6):

                        actions = (c1,c2,c3,c4)
                        self.poids[actions] = 1.0

    def sauvegarder(self) -> None:
        with open("donnees.pkl", "wb") as fichier:
            pickle.dump(self.poids, fichier)

    def entrainement(self) -> tuple:
        self.liste_actions = list(self.poids.keys())
        self.liste_poids = list(self.poids.values())

        return random.choices(self.liste_actions, self.liste_poids, k=1)[0]

    def analyse(self) -> None:
        (self.bien_place, self.mal_place) = Class.Comparateur.utilisation_IA(self.entrainement())

    def combinaison_possibles(self) -> list:
        self.combinaison_possibles = []
