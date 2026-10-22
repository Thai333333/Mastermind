import pyxel
import random
from math import ceil

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
            self.y = 14 + self.ecart_historique * (self.compte_historique - 5)
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
    def __init__(self, x, y, texte : str, couleur) -> None :
        self.texte = texte
        self.x = x
        self.y = y
        self.couleur = couleur

    def affichage(self) -> None:
        if not self.texte == None :
            pyxel.text(self.x, self.y, self.texte, self.couleur)


class FondTexte:
    def __init__(self, x, y, largeur, hauteur, couleur) -> None:
        self.x = x
        self.y = y
        self.largeur = largeur
        self.hauteur = hauteur
        self.couleur = couleur

    def affichage(self) -> None:
        pyxel.rect(self.x, self.y, self.largeur, self.hauteur, self.couleur)

class ListeBouton:

    def __init__(self) -> None:
        self.liste_bouton : list[Bouton] = []
        for i in range (6):
            self.liste_bouton.append(Bouton(i, None, None))

class CodeSecret:

    def __init__(self) -> None:
        self.liste_combinaison : list[Bouton] = []
        self.liste_boutons: list[Bouton] = ListeBouton().liste_bouton

        for i in range (4):
            self.liste_combinaison.append(random.choice(self.liste_boutons))

class Comparateur:

    def __init__(self, code_secret : list[Bouton], compte_historique) -> None:
        self.code_secret = code_secret
        self.compte_historique = compte_historique

        self.bien_place = 0
        self.mal_place = 0
        self.texte : str = None
        self.texte_x = 120
        self.texte_y = 0
        self.texte_couleur = 0
        self.liste_proposition: list[Bouton] = []

    # On réinitialise à chaque calcul les variables 
    def initialiser_les_variables(self, proposition) -> None:
        self.bien_place = 0
        self.mal_place = 0
        self.liste_proposition = list(proposition)
        
    def analyser_bien_place(self) -> int:
        self.bien_place = sum(
            secret.couleur == proposition.couleur
            for secret, proposition in zip(self.code_secret, self.liste_proposition)
        )
        return self.bien_place

    def analyser_mal_place(self) -> int:
        couleurs_restantes = [
            secret.couleur
            for secret, proposition in zip(self.code_secret, self.liste_proposition)
            if secret.couleur != proposition.couleur
        ]

        for index, proposition in enumerate(self.liste_proposition):
            if (
            proposition.couleur != self.code_secret[index].couleur
            and proposition.couleur in couleurs_restantes
            ):
                self.mal_place += 1
                couleurs_restantes.remove(proposition.couleur)
        return self.mal_place

            

    def generer_resultat(self, proposition : list[Bouton]) -> Texte:
        self.initialiser_les_variables(proposition)
        self.texte = str(self.analyser_bien_place()) + str(self.analyser_mal_place())
        if self.compte_historique >= 5:
            self.texte_x = 155
            self.texte_y = 14 + (self.compte_historique - 5) * 30
        else:
            self.texte_x = 90
            self.texte_y = 14 + self.compte_historique * 30

        self.compte_historique += 1
        return Texte(self.texte_x, self.texte_y, self.texte, self.texte_couleur)
