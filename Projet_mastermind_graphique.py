# Importation des librairies nécessaires et initialisation de la fenêtre Pyxel
from random import*
import pyxel


# Initialisation des dimensions de la fenêtre
fenetre_x = 250
fenetre_y = 250


# Initialisation de la fenêtre Pyxel
pyxel.init(fenetre_x,fenetre_y, title="Mastermind", fps=60, quit_key=pyxel.KEY_ESCAPE)
pyxel.load("Assemblage.pyxres")


#Initialisation des classes graphiques
class Bouton:

    def __init__(self, ordre):
        self.ordre = ordre

        self.x = 0
        self.y = 220
        self.largeur = 5
        self.hauteur = 5
        self.image = 0
        self.debut_x = 0
        self.debut_y = 1
        self.echelle = 6

    def calcul_bar_du_bas_position(self):
        self.x = 23 + 40*self.ordre
        self.debut_x = 1 + 8*self.ordre

    def est_clique(self):
        souris_dans_bouton = (self.x <= pyxel.mouse_x <= self.x + self.largeur * self.echelle) and (self.y <= pyxel.mouse_y <= self.y + self.hauteur * self.echelle)
        return souris_dans_bouton and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

    def calcul_proposition_position():
        pass    

    def calcul_barette(self):
        self.x = 138 + 40*self.ordre
        self.echelle = 4
        self.y = 180
    
    def affichage(self):
        pyxel.blt(self.x, self.y, self.image, self.debut_x, self.debut_y, self.largeur, self.hauteur, 0, None, self.echelle)

class Barette:

    def __init__(self):
        self.x = 118
        self.y = 170
        self.largeur = 15
        self.hauteur = 4
        self.image = 1
        self.debut_x = 0
        self.debut_y = 1
        self.echelle = 10

    def affichage(self):
        pyxel.blt(self.x, self.y, self.image, self.debut_x, self.debut_y, self.largeur, self.hauteur, 0, None, self.echelle)


# Création des boutons colorés
boutons = [
    Bouton(0),
    Bouton(1),
    Bouton(2),
    Bouton(3),
    Bouton(4),
    Bouton(5)
]


# Création de la barette
barettes = [Barette()]

# Création des clones
boutons_clique = []


# Fonctions graphiques update et draw
def update():

    # Calcul des positions des boutons
    i=-1
    for bouton in boutons:
        i+=1
        bouton.calcul_bar_du_bas_position()
        if bouton.est_clique():
            # Gérer le clic sur le bouton
                boutons_clique.append(Bouton(i))
                print(boutons_clique)

    for bouton in boutons_clique:
        bouton.calcul_barette()
    


def draw():
    pyxel.cls(0)
    pyxel.mouse(True)
    pyxel.blt(0,0,0,1,1,5,5,0,None)
    

    # Placement des boutons colorés
    for bouton in boutons:
        bouton.affichage()

    for barette in barettes:
        barette.affichage()


# Lancement du jeu
pyxel.run(update, draw)

'''
echelle piège
'''