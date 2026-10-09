# Importation des librairies nécessaires et initialisation de la fenêtre Pyxel

from random import*
import pyxel
pyxel.init(250,250, title="Mastermind")
pyxel.load("Assemblage.pyxres")

#Initialisation de variables pour éviter les répétitions

# Création des fonctions de calcul


# Fonctions graphiques update et draw
def update():
    if 


def draw():
    pyxel.mouse(visible)

    # Placement des boutons colorés
    pyxel.blt(23,220,0,1,1,5,5,0,None,6)
    pyxel.blt(63,220,0,9,1,5,5,0,None,6)
    pyxel.blt(103,220,0,17,1,5,5,0,None,6)
    pyxel.blt(143,220,0,1,9,5,5,0,None,6)
    pyxel.blt(183,220,0,9,9,5,5,0,None,6)
    pyxel.blt(223,220,0,17,9,5,5,0,None,6)


# Lancement du jeu
pyxel.run(update, draw)