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

    def __init__(self, couleur, ordre, compte_historique) -> None :
        self.ordre = ordre
        self.couleur = couleur
        self.compte_historique = compte_historique

        self.x = 0
        self.y = 220
        self.largeur = 5
        self.hauteur = 5
        self.image = 0
        self.debut_x = 0
        self.debut_y = 1
        self.echelle = 6
        self.ecart_historique = 30

    def calcul_bar_du_bas_position(self) -> None :
        self.x = 23 + 40*self.couleur
        self.debut_x = 1 + 8*self.couleur

    def est_clique(self) -> bool :
        souris_dans_bouton = (self.x - 3 * self.echelle<= pyxel.mouse_x <= self.x + self.largeur * self.echelle / 2) and (self.y - 3 * self.echelle <= pyxel.mouse_y <= self.y + self.hauteur * self.echelle / 2)
        # Attention au scale qui agrandit des deux cotés donc il faut "replacer le point de placement" de l'objet dans son coin superieur gauche pour que la zone de clique corresponde à la zone de l'objet
        return souris_dans_bouton and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)

    def calcul_proposition_position(self) -> None :
        self.debut_x = 8*self.couleur
        self.debut_y = 8
        self.hauteur = 7
        self.largeur = 7
        self.x = 78 + 30*self.ordre
        self.y = 169
        self.echelle = 4

    def calcul_position_historique_bouton(self) -> None :
        self.echelle = 2
        if self.compte_historique >= 5:
            self.x = 184 + self.ordre * 15
            self.compte_historique -= 5
        else :
            self.x = 15 + self.ordre * 15
        self.y = 14 + self.ecart_historique * self.compte_historique
        self.debut_x = self.couleur * 8
        self.largeur = 7

    def affichage(self) -> None :
        pyxel.blt(self.x, self.y, self.image, self.debut_x, self.debut_y, self.largeur, self.hauteur, 0, None, self.echelle)

class Barette:

    def __init__(self,compte_historique) -> None :
        self.compte_historique = compte_historique

        self.x = 118
        self.y = 170
        self.largeur = 15
        self.hauteur = 4
        self.image = 1
        self.debut_x = 0
        self.debut_y = 1
        self.echelle = 10

    def calcul_position_historique_barette(self) -> None :
        if self.compte_historique >= 5:
            self.x = 202
            self.y = 15 + (self.compte_historique - 5) * 30
        else :
            self.x = 33
            self.y = 15 + self.compte_historique * 30
        self.echelle = 5

    def affichage(self) -> None :
        pyxel.blt(self.x, self.y, self.image, self.debut_x, self.debut_y, self.largeur, self.hauteur, 0, None, self.echelle)

class Texte:
    def __init__(self, x, y, text : str, couleur) -> None :
        self.text = text
        self.x = x
        self.y = y
        self.couleur = couleur

    def affichage(self):
        pyxel.text(self.x, self.y, self.text, self.couleur)

class Fond_texte:
    def __init__(self, x, y, largeur, hauteur, couleur):
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur

    def affichage(self):
        pyxel.rect(self.x, self.y, self.largeur, self.hauteur, self.couleur)



# Création des boutons colorés
boutons = [
    Bouton(0, None, None),
    Bouton(1, None, None),
    Bouton(2, None, None),
    Bouton(3, None, None),
    Bouton(4, None, None),
    Bouton(5, None, None)
]


# Création de la barette
barettes = [Barette(None)]

# Création des clones
boutons_clique : list[Bouton] = []

historique_propositions_bouton : list[list[Bouton]] = []

historique_propositions_barette : list[Barette] = []

liste_fond_texte : list[Fond_texte] = []

liste_texte : list[Texte] = []


# Fonctions graphiques update et draw
def update() -> None :

    # Calcul des positions des boutons
    couleur=-1
    essai = len(historique_propositions_bouton)

    # Vérifie et crée un bouton sur la barette si cliqué
    for bouton in boutons:
        couleur+=1
        bouton.calcul_bar_du_bas_position()
        if bouton.est_clique() and len(boutons_clique) < 4:
            # Gérer le clic sur le bouton
            boutons_clique.append(Bouton(couleur, len(boutons_clique), essai))
                
    # Calcul des positions sur la barette
    for bouton in boutons_clique:
        bouton.calcul_proposition_position()

    if len(boutons_clique) == 4:
        liste_fond_texte.insert(0,Fond_texte(203, 162, 40, 20, 0))
        liste_texte.append(Texte(210, 168, "Valider", 7))

    # Valider la proposition par l'utlilisateur quand valider est cliqué
    if len(boutons_clique) == 4 and (pyxel.mouse_x >= 203 and pyxel.mouse_x <= 243) and (pyxel.mouse_y >= 162 and pyxel.mouse_y <= 182) and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT): 
        # Stockage de l'historique d'affichage dans une liste de listes de boutons

        for bouton in boutons_clique:
            bouton.calcul_position_historique_bouton()
        
        historique_propositions_bouton.append(boutons_clique.copy())
        historique_propositions_barette.append(Barette(essai))
        
        # Réinitialiser les boutons cliqués et compte du nombre d'essai
        boutons_clique.clear()
        liste_fond_texte.clear()
        liste_texte.clear()
        essai += 1

    for barette in historique_propositions_barette:
        barette.calcul_position_historique_barette()


def draw() -> None :
    pyxel.cls(6)
    pyxel.mouse(True)
    

    # Placement des boutons colorés
    for bouton in boutons:
        bouton.affichage()

    # Placement de la barette
    for barette in barettes:
        barette.affichage()

    # Placement des boutons cliqués
    for bouton in boutons_clique:
        bouton.affichage()

    # Affichage du fond du boutoon valider
    for fond in liste_fond_texte :
        fond.affichage()

    # Affichage du texte
    for text in liste_texte:
        text.affichage()

    # Placement des barettes pour l'historique
    for barette in historique_propositions_barette:
            barette.affichage()

    # Placement de l'historique des propositions
    for proposition in historique_propositions_bouton:
        for bouton in proposition:
            bouton.affichage()



# Lancement du jeu
pyxel.run(update, draw)