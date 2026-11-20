"""Associe les lettres des vagues aux ennemis et à leur sprite."""

from ..bouclier import Bouclier
from .boss import Boss
from .comportements_tir import TirSimple
from .ennemi import Ennemi

# FORMAT CATALOGUE_ENNEMIS
# "lettre": ("sprite sans .png", fonction qui crée l’ennemi en x, y)
# POUR AJOUTER : choisis une lettre libre, ajoute-la ici et dans vagues.py.
# EXEMPLE : "D" dans "NNDNN" crée un tireur rapide avec bouclier et 2 PV.
# "D": ("protege", lambda x, y: Ennemi(
#     x, y, TirSimple(delai=60), rapide=True, bouclier=Bouclier(), pv=2)),


CATALOGUE_ENNEMIS = {
    "N": ("simple", Ennemi),
    "T": ("tireur", lambda x, y: Ennemi(x, y, TirSimple())),
    "R": ("rapide", lambda x, y: Ennemi(x, y, TirSimple(), rapide=True)),
    "P": ("protege", lambda x, y: Ennemi(x, y, TirSimple(), bouclier=Bouclier())),
    "B": ("boss", Boss),
    # "D": ("protege", lambda x, y: Ennemi(x, y, TirSimple(delai=60), rapide=True, bouclier=Bouclier(), pv=2)),
}

def creer_ennemi(case, x, y):
    """Crée un ennemi à partir d'une lettre du catalogue.

    :param case: Lettre qui identifie l'ennemi dans la grille de la vague.
    :type case: str
    :param x: Position horizontale de départ en pixels.
    :type x: int
    :param y: Position verticale de départ en pixels.
    :type y: int
    :return: Le nouvel ennemi placé aux coordonnées indiquées.
    :rtype: Ennemi
    :raises ValueError: Si la lettre est absente du catalogue.
    """
    try:
        type_ennemi, construire = CATALOGUE_ENNEMIS[case]
    except KeyError:
        raise ValueError(f"Case de vague inconnue : {case}") from None

    ennemi = construire(x, y)
    ennemi.type_ennemi = type_ennemi
    return ennemi
