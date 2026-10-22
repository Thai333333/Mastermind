# Importation des librairies nécessaires et initialisation de la fenêtre Pyxel
import pyxel
import Class
import Police


class App:
    def __init__(self):
        # Initialisation de la fenêtre Pyxel
        pyxel.init(250, 250, title="Mastermind", fps=60, quit_key=pyxel.KEY_ESCAPE)
        pyxel.load("Assemblage.pyxres")

        # Création des variables de comptage pour l'affichage
        self.essai = 0
        
        # Création des variables de gestion pour l'affichage
        self.gagner = False
        self.perdu = False
        self.menu = False
        self.jeu = True

        # Génération de la combinaison
        self.liste_combinaison_secrete: list[Class.Bouton] = Class.CodeSecret().liste_combinaison

        # Création des boutons colorés
        self.liste_boutons: list[Class.Bouton] = Class.ListeBouton().liste_bouton

        # Création de la barette
        self.liste_barettes: list[Class.Barette] = [Class.Barette(None)]
        
        # Création du comparateur
        self.comparateur = Class.Comparateur(self.liste_combinaison_secrete, 0)

        # Création des listes de clones
        self.liste_boutons_clique: list[Class.Bouton] = []
        self.liste_historique_propositions_bouton: list[list[Class.Bouton]] = []
        self.liste_historique_propositions_barette: list[Class.Barette] = []
        self.liste_fond_texte: list[Class.FondTexte] = []
        self.liste_texte_police: list[Police.PoliceBitmap] = []
        self.liste_texte: list[Class.Texte] = [Class.Texte(None, None, None, None), 
                                               Class.Texte(110, 5, "Essai:" + str(self.essai), 0)
                                               ]

        # Lancement du jeu
        pyxel.run(self.update,self.draw)


    # Fonctions calcul update et graphique draw
    def update(self) -> None:

        # Gestion du menu
        if self.menu:
            pass

        # Lancement du jeu et gestion
        if self.jeu:
            # Vérifie et crée un bouton sur la barette si cliqué
            for couleur, bouton in enumerate(self.liste_boutons):
                bouton.calcul_bar_du_bas_position()
                if bouton.est_clique() and len(self.liste_boutons_clique) < 4:
                    # Gérer le clic sur le bouton
                    self.liste_boutons_clique.append(Class.Bouton(couleur, len(self.liste_boutons_clique), self.essai))

            if len(self.liste_boutons_clique) == 4 and not self.liste_fond_texte:
                self.liste_fond_texte.append(Class.FondTexte(203, 162, 40, 20, 0))
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
                self.liste_fond_texte.clear()
                self.liste_texte[0] = Class.Texte(None, None, None, None)
                self.liste_texte[1] = Class.Texte(110, 5, "Essai:" + str(self.essai), 0)

        # Gestion de l'écran de fin

        # Texte à afficher en fonction de si le joueur à gagné ou perdu
        if self.gagner or self.perdu:

            for bouton in self.liste_combinaison_secrete:
                bouton.calcul_proposition_position()

            if self.gagner:
                self.liste_texte_police.append(Police.PoliceBitmap(75, 65, "Bien joué !", 0))
                self.liste_texte_police.append(Police.PoliceBitmap(48, 85, "Vous avez gagné !", 0))
                
            else:
                self.liste_texte_police.append(Police.PoliceBitmap(84, 65, "Dommage !", 0))
                self.liste_texte_police.append(Police.PoliceBitmap(48, 85, "Vous avez perdu !", 0))

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

        if not (self.gagner or self.perdu or self.menu):
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
            for fond in self.liste_fond_texte:
                fond.affichage()

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

            if self.gagner:
                for texte in self.liste_texte_police:
                    texte.affichage()
                
            else:
                for texte in self.liste_texte_police:
                    texte.affichage()

App()