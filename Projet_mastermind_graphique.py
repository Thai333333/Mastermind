# Importation des librairies nécessaires et initialisation de la fenêtre Pyxel
import pyxel
import Class
import Police
from Calcul_geometrie import Geometrie

class App:
    def __init__(self):
        # Initialisation de la fenêtre Pyxel
        pyxel.init(250, 250, title="Mastermind", fps=60, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load("Assemblage.pyxres")

        # Création des variables de comptage pour l'affichage
        self.essai = 0
        
        # Création des variables de gestion pour l'affichage
        self.ecran_fin_pret = False
        self.ecran_menu_pret = False
        self.gagner = False
        self.perdu = False
        self.menu = True
        self.jeu = False

        # Génération de la combinaison
        self.liste_combinaison_secrete: list[Class.Bouton] = []

        # Création des boutons colorés
        self.liste_boutons: list[Class.Bouton] = Class.ListeBouton().liste_bouton

        # Création de la barette
        self.liste_barettes: list[Class.Barette] = [Class.Barette(None)]
        
        # Création des listes de clones
        self.liste_boutons_clique: list[Class.Bouton] = []
        self.liste_historique_propositions_bouton: list[list[Class.Bouton]] = []
        self.liste_historique_propositions_barette: list[Class.Barette] = []
        self.liste_forme: list[Class.Forme] = [
                                                Class.Forme("cercle", 11, 125, 125, 20),
                                                Class.Forme("triangle", 7, 117, 113 , x_2=117, y_2=137, x_3=137, y_3=125)
                                                ]
        self.liste_texte_police: list[Police.PoliceBitmap] = [
                                                            Police.PoliceBitmap((250 - len("Mastermind") * 8 * 2) // 2, 40, "Mastermind", 0, 2)
                                                            ]
        self.liste_texte: list[Class.Texte] = [
                                                Class.Texte(None, None, None, None), 
                                                Class.Texte(110, 5, "Essai:" + str(self.essai), 0)
                                               ]

        # Lancement du jeu
        pyxel.run(self.update,self.draw)

    def lancer_une_partie(self):
        self.liste_combinaison_secrete = Class.CodeSecret().liste_combinaison
        # Création du comparateur
        self.comparateur = Class.Comparateur(self.liste_combinaison_secrete, 0)

    def reinitialiser_les_variables(self):
        self.essai = 0
        self.liste_historique_propositions_barette.clear()
        self.liste_historique_propositions_bouton.clear()
        self.liste_forme.clear()
        self.liste_texte_police.clear()
        self.liste_texte = [
                            Class.Texte(None, None, None, None), 
                            Class.Texte(110, 5, "Essai:" + str(self.essai), 0)
                            ]

    # Fonctions calcul update et graphique draw
    def update(self) -> None:
        
        # Gestion du menu
        if self.menu:
            if not self.ecran_menu_pret:
                self.liste_forme = [
                                    Class.Forme("cercle", 11, 125, 125, 20),
                                    Class.Forme("triangle", 7, 117, 113 , x_2=117, y_2=137, x_3=137, y_3=125)
                                    ]
                self.liste_texte_police = [
                                            Police.PoliceBitmap((250 - len("Mastermind") * 8 * 2) // 2, 40, "Mastermind", 0, 2)
                                            ]
                self.ecran_menu_pret = True

            # Vérification du clique sur le bouton pour lancer le jeu
            if (
                Geometrie.pythagore((pyxel.mouse_x-125), (pyxel.mouse_y-125)) <= 20
                and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            ):
                self.lancer_une_partie()
                self.liste_forme.clear()
                self.liste_texte_police.clear()
                self.menu = False
                self.jeu = True
                self.ecran_menu_pret = False

        # Lancement du jeu et gestion
        if self.jeu:
            # Vérifie et crée un bouton sur la barette si cliqué
            for couleur, bouton in enumerate(self.liste_boutons):
                bouton.calcul_bar_du_bas_position()
                if bouton.est_clique() and len(self.liste_boutons_clique) < 4:
                    # Gérer le clic sur le bouton
                    self.liste_boutons_clique.append(Class.Bouton(couleur, len(self.liste_boutons_clique), self.essai))

            if len(self.liste_boutons_clique) == 4 and not self.liste_forme:
                self.liste_forme.append(Class.Forme("rectangle", 0, 203, 162, 40, 20))
                self.liste_texte[0] = Class.Texte(210, 168, "Valider", 7)

            # Valider la proposition lorsque le bouton est cliqué
            if (
                len(self.liste_boutons_clique) == 4
                and 203 <= pyxel.mouse_x <= 243
                and 162 <= pyxel.mouse_y <= 182
                and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            ):

                # Stockage de l'historique d'affichage dans une liste de listes de boutons
                self.liste_historique_propositions_bouton.append(self.liste_boutons_clique.copy())
                self.liste_historique_propositions_barette.append(Class.Barette(self.essai))

                # Mise à jour du nombre d'essai
                self.essai += 1

                # Ajouter le texte à afficher
                self.liste_texte.append(self.comparateur.generer_resultat(self.liste_boutons_clique))

                # Gestion des conditions de victoire
                if self.liste_texte[-1].texte == "40" and self.essai <= 10:
                    self.gagner = True

                elif self.essai >=10:
                    self.perdu = True
                    
                # Réinitialiser les boutons cliqués et compte du nombre d'essai
                self.liste_boutons_clique.clear()
                self.liste_forme.clear()
                self.liste_texte[0] = Class.Texte(None, None, None, None)
                self.liste_texte[1] = Class.Texte(110, 5, "Essai:" + str(self.essai), 0)

        # Gestion de l'écran de fin

        # Texte à afficher en fonction de si le joueur à gagné ou perdu
        if self.gagner or self.perdu:
            self.jeu = False

            for bouton in self.liste_combinaison_secrete:
                bouton.calcul_proposition_position()

            if not self.ecran_fin_pret:
                self.ecran_fin_pret = True

                self.liste_forme.append(Class.Forme("rectangle", 11, 30, 220, 85, 22))
                self.liste_forme.append(Class.Forme("rectangle", 13, 135, 220, 85, 22))

                self.liste_texte_police.append(Police.PoliceBitmap(41, 223, "Rejouer", 7))
                self.liste_texte_police.append(Police.PoliceBitmap(159, 223, "Menu", 7))

                if self.gagner:
                    self.liste_texte_police.append(Police.PoliceBitmap(75, 65, "Bien joué !", 0))
                    self.liste_texte_police.append(Police.PoliceBitmap(48, 85, "Vous avez gagné !", 0))
                    
                else:
                    self.liste_texte_police.append(Police.PoliceBitmap(84, 65, "Dommage !", 0))
                    self.liste_texte_police.append(Police.PoliceBitmap(48, 85, "Vous avez perdu !", 0))

            if (
                30 <= pyxel.mouse_x <= 115
                and 220 <= pyxel.mouse_y <= 242
                and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            ):
                self.jeu = True
                self.perdu = False
                self.gagner = False
                self.ecran_fin_pret = False
                self.reinitialiser_les_variables()
                self.lancer_une_partie()

            if (
                135 <= pyxel.mouse_x <= 220
                and 220 <= pyxel.mouse_y <= 242
                and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            ):
                self.perdu = False
                self.gagner = False
                self.menu = True
                self.ecran_fin_pret = False
                self.reinitialiser_les_variables()
                
        # Calcul des positions des boutons et de la barette que ce soit la fin de partie ou pas
        for bouton in self.liste_boutons_clique:
            bouton.calcul_proposition_position()

        for liste_de_bouton in self.liste_historique_propositions_bouton:
            for bouton in liste_de_bouton:
                bouton.calcul_position_historique_bouton()

        for barette in self.liste_historique_propositions_barette:
            barette.calcul_position_historique_barette()


    def draw(self) -> None:
        pyxel.cls(15)
        pyxel.mouse(True)

        if self.menu:
            for texte in self.liste_texte_police:
                texte.affichage()

            for forme in self.liste_forme:
                forme.affichage()

        if self.jeu:
            # Placement des boutons colorés
            for bouton in self.liste_boutons:
                bouton.affichage()

            # Placement de la barette
            for barette in self.liste_barettes:
                barette.affichage()

            # Placement des boutons cliqués
            for bouton in self.liste_boutons_clique:
                bouton.affichage()

            # Affichage du fond du bouton valider
            for forme in self.liste_forme:
                forme.affichage()

            # Affichage du texte
            for texte in self.liste_texte:
                texte.affichage()

            # Placement des barettes pour l'historique
            for barette in self.liste_historique_propositions_barette:
                barette.affichage()

            # Placement de l'historique des propositions
            for proposition in self.liste_historique_propositions_bouton:
                for bouton in proposition:
                    bouton.affichage()

        if self.gagner or self.perdu:
            for barette in self.liste_barettes:
                barette.affichage()

            for bouton in self.liste_combinaison_secrete:
                bouton.affichage()

            self.liste_texte[1].affichage()

            for forme in self.liste_forme:
                forme.affichage()
                
            if self.gagner:
                for texte in self.liste_texte_police:
                    texte.affichage()
                
            else:
                for texte in self.liste_texte_police:
                    texte.affichage()

App()