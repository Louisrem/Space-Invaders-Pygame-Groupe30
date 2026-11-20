from ..bouclier import Bouclier
from .boss import Boss
from .comportements_tir import TirSimple
from .ennemi import Ennemi


# Chaque lettre associe un nom de sprite et une fonction de création.
# Chaque tireur reçoit sa propre instance de TirSimple et son propre délai.
CATALOGUE_ENNEMIS = {
    "N": ("simple", Ennemi),
    "T": ("tireur", lambda x, y: Ennemi(x, y, TirSimple())),
    "R": ("rapide", lambda x, y: Ennemi(x, y, TirSimple(), rapide=True)),
    "P": ("protege", lambda x, y: Ennemi(x, y, TirSimple(), bouclier=Bouclier())),
    "B": ("boss", Boss),
}


def creer_ennemi(case, x, y):
    try:
        type_ennemi, construire = CATALOGUE_ENNEMIS[case]
    except KeyError:
        raise ValueError(f"Case de vague inconnue : {case}") from None

    ennemi = construire(x, y)
    ennemi.type_ennemi = type_ennemi
    return ennemi
