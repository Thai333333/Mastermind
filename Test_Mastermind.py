import pytest
from Projet_mastermind import*

# Test
def test_longueur_generer_combinaison_secrete():
    assert len(generer_combinaison_secrete(4,[1,2,3,4,5,6]))

def test_contenu_generer_combinaison_secrete():
    for i in range (4):
        assert generer_combinaison_secrete(4,[1,2,3,4,5,6]) in [1,2,3,4,5,6]
