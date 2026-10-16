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

    def __init__(self, numero, ordre):
        self.ordre = ordre
        self.numero = numero

        self.x = 0
        self.y = 220
        self.largeur = 5
        self.hauteur = 5
        self.image = 0
        self.debut_x = 1
        self.debut_y = 1
        self.echelle = 6

    def calcul_bar_du_bas_position(self):
        self.x = 23 + 40*self.numero
        self.debut_x = 1 + 8*self.numero

    def est_clique(self):
        souris_dans_bouton = (self.x - 3 * self.echelle<= pyxel.mouse_x <= self.x + self.largeur * self.echelle / 2) and (self.y - 3 * self.echelle <= pyxel.mouse_y <= self.y + self.hauteur * self.echelle / 2)
        # Attention au scale qui agrandit des deux cotés donc il faut "replacer le point de placement" de l'objet dans son coin superieur gauche pour que la zone de clique corresponde à la zone de l'objet
        return souris_dans_bouton and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

    def calcul_proposition_position(self):
        self.debut_x = 8*self.numero
        self.debut_y = 8
        self.hauteur = 7
        self.largeur = 7
        self.x = 78 + 30*self.ordre
        self.y = 169
        self.echelle = 4
    
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

    def calcul_position_historique():
        pass


# Création des boutons colorés
boutons = [
    Bouton(0, None),
    Bouton(1, None),
    Bouton(2, None),
    Bouton(3, None),
    Bouton(4, None),
    Bouton(5, None)
]


# Création de la barette
barettes = [Barette()]

# Création des clones
boutons_clique : list[Bouton] = []

historique_propositions : list[list[Bouton]] = []


# Fonctions graphiques update et draw
def update():

    # Calcul des positions des boutons
    i=-1
    for bouton in boutons:
        i+=1
        bouton.calcul_bar_du_bas_position()
        if bouton.est_clique() and len(boutons_clique) < 4:
            # Gérer le clic sur le bouton
            index_dernier_boutons_clique = len(boutons_clique)
            boutons_clique.append(Bouton(i,index_dernier_boutons_clique))
                
    # Calcul des positions sur la barette
    for bouton in boutons_clique:
        bouton.calcul_proposition_position()

    # Valider la proposition par l'utlilisateur
    if len(boutons_clique) == 4 and (pyxel.mouse_x >= 203 and pyxel.mouse_x <= 243) and (pyxel.mouse_y >= 162 and pyxel.mouse_y <= 182) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT):
        historique_propositions.append(boutons_clique.copy())
        boutons_clique.clear()

    


def draw():
    pyxel.cls(6)
    pyxel.mouse(True)
    pyxel.blt(0,0,0,1,1,5,5,0,None)
    

    # Placement des boutons colorés
    for bouton in boutons:
        bouton.affichage()

    for barette in barettes:
        barette.affichage()

    for bouton in boutons_clique:
        bouton.affichage()

    if len(boutons_clique) == 4:
        pyxel.rect(203, 162, 40, 20, 0)
        pyxel.text(210, 168, "Valider", 7)
        


# Lancement du jeu
pyxel.run(update, draw)

