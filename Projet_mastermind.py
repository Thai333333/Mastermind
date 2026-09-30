# Importation des librairies nécessaires
from random import*

# Création des fonctions

# Génération aléatoire de la combinaison secrète
def generer_combinaison_secrete(taille, chiffres_possibles):
    combinaison_secrete=[]
    for i in range (taille):
        combinaison_secrete.append(choice(chiffres_possibles)) # Combinaison secrète sous forme de liste
    return combinaison_secrete

# Proposition de l'utilisateur
def demander_proposition(taille, chiffres_possibles):
    combinaison=[]
    for i in range(taille):
        proposition=int(input())
        if proposition in chiffres_possibles: # Vérification de la validité de la proposition de l'utilisateur
            combinaison.append(proposition)
        else:
            taille+=1
    return combinaison

# Comparaison de la proposition de l'utilisateur par rapport à l'ordinateur
def analyser_proposition(secret, proposition):
    bien_place = 0
    mal_place = 0
    for i in range(len(secret)): # On test si les nombres sont bien placées
        if secret[i] == proposition[i]:
            bien_place += 1
    for i in range(len(secret)): # On test si les nombres sont dans la combinaison mais mal placées
        if proposition[i] != secret [i] and proposition[i] in secret: # On vérifie que le nombre est bien dans la combinaison mais mal placé
            mal_place += 1
    return bien_place, mal_place

# On affiche le résultat de l'analyse
def afficher_resultat(bien_places, mal_places):
    print("Il y a", bien_places, "chiffres bien placés et", mal_places, "chiffres mal placés.")

# On appelle les fonctions nécessaires au fonctionnement du jeu
def jouer_une_partie():
    # On initialise les variables et listes
    taille = 4
    essai = 0
    chiffres_possibles = [1,2,3,4,5,6]
    combinaison_secrete = generer_combinaison_secrete(taille,chiffres_possibles)
    while True: # Tant que la solution n'est pas trouvé le jeu continue
        essai += 1
        proposition = demander_proposition(taille, chiffres_possibles)
        if analyser_proposition(combinaison_secrete, proposition) == (0,4): # Si la combinaison est bonne on sort de la boucle et on dit que c'est gagné
            print("Bravo ! Vous avez réussi en", essai, "essai !")
            break
        else: # Si la solution n'est pas trouvé on affiche l'analyse
            print(afficher_resultat(analyser_proposition(combinaison_secrete, proposition)))

# On appelle la fonction main qui appelle la fonction jouer_une_partie pour lancer le jeu
def main():
    jouer_une_partie()