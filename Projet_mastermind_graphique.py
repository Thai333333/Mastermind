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
        self.menu = True
        self.ecran_menu_en_jeu_pret = False
        self.ecran_menu_pret = False
        self.ecran_aide_pret = False
        self.ecran_fin_pret = False
        self.menu_en_jeu = False
        self.gagner = False
        self.perdu = False
        self.aide = False
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
        self.formes: dict[str, Class.Forme] = {
            "menu_jouer_cercle": Class.Forme("cercle", 11, 125, 125, 20),
            "menu_jouer_triangle": Class.Forme("triangle", 7, 117, 113, x_2=117, y_2=137, x_3=137, y_3=125),
        }
        self.textes_police: list[Police.PoliceBitmap] = [
                                                            Police.PoliceBitmap((250 - len("Mastermind") * 8 * 2) // 2, 40, "Mastermind", 0, 2)
                                                            ]
        self.textes: dict[str, Class.Texte] = {
            "valider": Class.Texte(None, None, None, None),
            "essai": Class.Texte(110, 5, "Essai:" + str(self.essai), 0),
        }
        self.texte_aide: tuple[str] = (
            "- Votre but est de deviner la combinaison de",
            "  couleurs choisi par l'ordinateur",
            "- Cliquez sur les formes colorees pour composer",
            "  votre proposition",
            "- Une fois votre proposition complete, appuyez",
            '  sur le bouton "valider"',
            "- Un resultat s'affiche a cote de votre",
            "  proposition a la suite des precedentes",
            "- Le premier indique le nombre de couleurs",
            "  qui sont bien placees et le deuxieme le",
            "  nombre qui sont mal placees",
            "- Si vous obtenez un score de 40, bien joue",
            "  vous avez gagne",
        )

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
        self.textes_police = []
        self.formes = {
                    "effacer_forme": Class.Forme("rectangle", 0, 5, 162, 40, 20),
                    "menu_en_jeu": Class.Forme("rectangle", 13, 230, 242, 20, 20),
                    "menu_en_jeu_l1": Class.Forme("rectangle", 0, 233, 247, 14, 2),
                    "menu_en_jeu_l2": Class.Forme("rectangle", 0, 233, 252, 14, 2),
                    "menu_en_jeu_l3": Class.Forme("rectangle", 0, 233, 257, 14, 2),
                    }
        self.textes = {
            "valider": Class.Texte(None, None, None, None),
            "essai": Class.Texte(110, 5, "Essai:" + str(self.essai), 0),
            "effacer": Class.Texte(12, 169, "Effacer", 7),
                    }

    # Fonctions calcul update et graphique draw
    def update(self) -> None:
        
        # Gestion du menu
        if self.menu:
            # Preparation de l'affichage du menu
            if not self.ecran_menu_pret:
                self.formes = {
                    "menu_jouer_cercle": Class.Forme("cercle", 11, 125, 125, 20),
                    "menu_jouer_triangle": Class.Forme("triangle", 7, 117, 113, x_2=117, y_2=137, x_3=137, y_3=125),
                    "menu_aide": Class.Forme("cercle", 11, 230, 230, 12),
                }
                self.textes_police = [
                                            Police.PoliceBitmap((250 - len("Mastermind") * 8 * 2) // 2, 40, "Mastermind", 0, 2),
                                            Police.PoliceBitmap(225, 223, "?", 7)
                                            ]
                self.ecran_menu_pret = True

            # Vérification du clique sur le bouton pour lancer le jeu
            if (
                Geometrie.pythagore((pyxel.mouse_x-125), (pyxel.mouse_y-125)) <= 20
                and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            ):
                self.reinitialiser_les_variables()
                self.lancer_une_partie()
                self.textes_police.clear()
                self.menu = False
                self.jeu = True
                self.ecran_menu_pret = False

            # Vérification du clique sur le bouton pour lancer l'aide
            if(
                Geometrie.pythagore((pyxel.mouse_x-230),(pyxel.mouse_y-230)) <= 12
                and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            ):
                self.formes.clear()
                self.textes_police.clear()
                self.menu = False
                self.ecran_menu_pret = False
                self.aide = True

        # Gestion de l'aide
        if self.aide:
            # Preparation de l'affichage de l'aide
            if not self.ecran_aide_pret:
                self.formes.update({
                    "aide_fond": Class.Forme("rectangle", 6, 20, 20, 210, 210),
                    "aide_fermer": Class.Forme("rectangle", 8, 210, 20, 20, 20),
                })
                self.textes_police.extend([
                    Police.PoliceBitmap(65, 25, "COMMENT JOUER", 0),
                    Police.PoliceBitmap(215, 22, "X", 0)
                    ])
                self.ecran_aide_pret = True

            # Vérification du clique sur le bouton pour fermer l'aide
            if (
                210 <= pyxel.mouse_x <= 230
                and 20 <= pyxel.mouse_y <= 40
                and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            ):
                self.aide = False
                self.menu = True
                self.ecran_aide_pret = False
                self.textes_police.clear()
                self.formes.clear()

        # Lancement du jeu et gestion
        if self.jeu:

            # Vérifie et crée un bouton sur la barette si cliqué
            for couleur, bouton in enumerate(self.liste_boutons):
                bouton.calcul_bar_du_bas_position()
                if bouton.est_clique() and len(self.liste_boutons_clique) < 4:
                    # Gérer le clic sur le bouton
                    self.liste_boutons_clique.append(Class.Bouton(couleur, len(self.liste_boutons_clique), self.essai))

            # Vérifie et supprime le dernier bouton de la barette si boutton effacer est cliqué
            if (len(self.liste_boutons_clique) > 0
                and 5 <= pyxel.mouse_x <= 45
                and 162 <= pyxel.mouse_y <= 182
                and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
                ):
                self.liste_boutons_clique.pop()
                
            # Vérifie et crée le bouton valider si 4 boutons sont cliqués
            if len(self.liste_boutons_clique) == 4 and "bouton_valider" not in self.formes:
                self.formes["bouton_valider"] = Class.Forme("rectangle", 0, 203, 162, 40, 20)
                self.textes["valider"] = Class.Texte(210, 168, "Valider", 7)
            # Vérifie et supprime le bouton valider si moins de 4 boutons sont cliqués
            elif "bouton_valider" in self.formes and len(self.liste_boutons_clique) < 4:
                self.formes.pop("bouton_valider")
                self.textes.pop("valider")

            # Approche la souris du bouton pour accéder au menu en jeu
            if (215 <=pyxel.mouse_x <= 250
                and 220 <= pyxel.mouse_y <= 250
                ):
                self.formes["menu_en_jeu"] = Class.Forme("rectangle", 13, 230, 230, 20, 20)
                self.formes["menu_en_jeu_l1"] = Class.Forme("rectangle", 0, 233, 235, 14, 2)
                self.formes["menu_en_jeu_l2"] = Class.Forme("rectangle", 0, 233, 240, 14, 2)
                self.formes["menu_en_jeu_l3"] = Class.Forme("rectangle", 0, 233, 245, 14, 2)
            else:
                self.formes["menu_en_jeu"] = Class.Forme("rectangle", 13, 230, 242, 20, 20)
                self.formes["menu_en_jeu_l1"] = Class.Forme("rectangle", 0, 233, 247, 14, 2)
                self.formes["menu_en_jeu_l2"] = Class.Forme("rectangle", 0, 233, 252, 14, 2)
                self.formes["menu_en_jeu_l3"] = Class.Forme("rectangle", 0, 233, 257, 14, 2)

            # Vérifie si le bouton menu en jeu est cliqué
            if ( 230 <= pyxel.mouse_x <= 250
                and 230 <= pyxel.mouse_y <= 250
                and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
            ):
                self.menu_en_jeu = True
                self.jeu = False
                if not self.ecran_menu_en_jeu_pret:
                    self.formes.clear()
                    self.formes["menu_en_jeu_fond"] = Class.Forme("rectangle", 6, 20, 20, 210, 210)
                    self.formes["menu_en_jeu_continuer"] = Class.Forme("rectangle", 3, 80, 70, 89, 22)
                    self.formes["menu_en_jeu_rejouer"] = Class.Forme("rectangle", 11, 80, 110, 89, 22)
                    self.formes["menu_en_jeu_menu"] = Class.Forme("rectangle", 13, 80, 150, 89, 22)
                    self.textes_police.append(Police.PoliceBitmap(84, 73, "Continuer", 7))
                    self.textes_police.append(Police.PoliceBitmap(93, 113, "Rejouer", 7))
                    self.textes_police.append(Police.PoliceBitmap(107, 153, "Menu", 7))
                    self.ecran_menu_en_jeu_pret = True

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
                cle_resultat = f"resultat_{self.essai}"
                self.textes[cle_resultat] = self.comparateur.generer_resultat(self.liste_boutons_clique)

                # Gestion des conditions de victoire
                if self.textes[cle_resultat].texte == "40" and self.essai <= 10:
                    self.gagner = True

                elif self.essai >=10:
                    self.perdu = True
                    
                # Réinitialiser les boutons cliqués et compte du nombre d'essai
                self.liste_boutons_clique.clear()
                self.formes.pop("bouton_valider")
                self.textes["valider"] = Class.Texte(None, None, None, None)
                self.textes["essai"] = Class.Texte(110, 5, "Essai:" + str(self.essai), 0)

        # Vérifie si le bouton continuer du menu en jeu est cliqué
        if (
            self.menu_en_jeu
            and 80 <= pyxel.mouse_x <= 169
            and 70 <= pyxel.mouse_y <= 92
            and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        ):
            self.menu_en_jeu = False
            self.jeu = True
            self.ecran_menu_en_jeu_pret = False
            self.formes = {
                "effacer_forme": Class.Forme("rectangle", 0, 5, 162, 40, 20),
                "menu_en_jeu": Class.Forme("rectangle", 13, 230, 242, 20, 20),
                "menu_en_jeu_l1": Class.Forme("rectangle", 0, 233, 247, 14, 2),
                "menu_en_jeu_l2": Class.Forme("rectangle", 0, 233, 252, 14, 2),
                "menu_en_jeu_l3": Class.Forme("rectangle", 0, 233, 257, 14, 2),
            }
            self.textes_police.clear()

        # Vérifie si le bouton rejouer du menu en jeu est cliqué
        if (
            self.menu_en_jeu
            and 80 <= pyxel.mouse_x <= 169
            and 110 <= pyxel.mouse_y <= 132
            and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        ):
            self.ecran_fin_pret = False
            self.jeu = True
            self.menu_en_jeu = False
            self.ecran_menu_en_jeu_pret = False
            self.reinitialiser_les_variables()
            self.lancer_une_partie()

        # Vérifie si le bouton menu du menu en jeu est cliqué
        if (
            self.menu_en_jeu
            and 80 <= pyxel.mouse_x <= 169
            and 150 <= pyxel.mouse_y <= 172
            and pyxel.btnp(pyxel.MOUSE_BUTTON_LEFT)
        ):
            self.menu = True
            self.ecran_fin_pret = False
            self.menu_en_jeu = False
            self.ecran_menu_en_jeu_pret = False
            self.reinitialiser_les_variables()

        # Gestion de l'écran de fin

        # Texte à afficher en fonction de si le joueur à gagné ou perdu
        if self.gagner or self.perdu:
            self.jeu = False

            for bouton in self.liste_combinaison_secrete:
                bouton.calcul_proposition_position()

            if not self.ecran_fin_pret:
                self.ecran_fin_pret = True
                self.formes.clear()

                self.formes["fin_rejouer"] = Class.Forme("rectangle", 11, 30, 220, 85, 22)
                self.formes["fin_menu"] = Class.Forme("rectangle", 13, 135, 220, 85, 22)

                self.textes_police.append(Police.PoliceBitmap(41, 223, "Rejouer", 7))
                self.textes_police.append(Police.PoliceBitmap(159, 223, "Menu", 7))

                if self.gagner:
                    self.textes_police.append(Police.PoliceBitmap(75, 65, "Bien joué !", 0))
                    self.textes_police.append(Police.PoliceBitmap(48, 85, "Vous avez gagné !", 0))
                    
                else:
                    self.textes_police.append(Police.PoliceBitmap(84, 65, "Dommage !", 0))
                    self.textes_police.append(Police.PoliceBitmap(48, 85, "Vous avez perdu !", 0))

            # Rejouer une partie
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

            # Retour au menu de départ
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
            for forme in self.formes.values():
                forme.affichage()

            for texte in self.textes_police:
                texte.affichage()

        # Affichage de l'aide
        if self.aide:

            # Affichage des formmes et textes de l'aide
            for forme in self.formes.values():
                forme.affichage()

            # Affichage du titre de la page d'aide et du bouton de fermeture
            for texte in self.textes_police:
                texte.affichage()

            # Affichage du texte d'aide
            for index, ligne in enumerate(self.texte_aide):
                pyxel.text(27, 47 + index * 14, ligne, 0)

        # Affichage du jeu
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
            for forme in self.formes.values():
                forme.affichage()

            # Affichage du texte
            for texte in self.textes.values():
                texte.affichage()

            # Placement des barettes pour l'historique
            for barette in self.liste_historique_propositions_barette:
                barette.affichage()

            # Placement de l'historique des propositions
            for proposition in self.liste_historique_propositions_bouton:
                for bouton in proposition:
                    bouton.affichage()

        if self.menu_en_jeu:
            # Affichage du fond du menu en jeu
            for forme in self.formes.values():
                forme.affichage()

            # Affichage des textes du menu en jeu
            for texte in self.textes_police:
                texte.affichage()

        # Affichage de l'écran de fin
        if self.gagner or self.perdu:
            # Affichage des boutons de fin de partie et de la barette de la combinaison secrète
            for barette in self.liste_barettes:
                barette.affichage()

            for bouton in self.liste_combinaison_secrete:
                bouton.affichage()

            # Affichage du nombre d'essai
            self.textes["essai"].affichage()

            # Affichage des bouttons pour aller au menu et rejouer
            for forme in self.formes.values():
                forme.affichage()

            # Affichage des textes de fin de partie
            if self.gagner:
                for texte in self.textes_police:
                    texte.affichage()
                
            else:
                for texte in self.textes_police:
                    texte.affichage()

App()