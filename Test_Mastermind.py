import pytest
from pyxel import *
from Projet_mastermind import*

combinaison_longueur = 4
combinaison_chiffres_possibles = [1, 2, 3, 4, 5, 6]
reponses = iter("1","2","3","4")

# Test generer combinaison secrète
def test_longueur_generer_combinaison_secrete():
    assert len(generer_combinaison_secrete(combinaison_longueur, combinaison_chiffres_possibles)) == 4

def test_contenu_generer_combinaison_secrete():
    assert set(generer_combinaison_secrete(combinaison_longueur, combinaison_chiffres_possibles)).issubset(set(combinaison_chiffres_possibles))

def test_longueur_demander_proposition(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: next(reponses))
    resultat = demander_proposition(combinaison_longueur, combinaison_chiffres_possibles)
    assert len(resultat) == 4

def test_contenu_demander_proposition(monkeypatch):
    monkeypatch.setattr("builtins.input", lambda: next(reponses))
    resultat = demander_proposition(combinaison_longueur, combinaison_chiffres_possibles)
    assert len(resultat) == 4
