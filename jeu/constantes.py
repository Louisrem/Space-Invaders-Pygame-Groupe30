"""Constantes partagées : taille du terrain, états et événements de la partie."""

from enum import Enum, auto

LARGEUR_TERRAIN = 800
HAUTEUR_TERRAIN = 600


class EtatPartie(Enum):
    """Énumère les états disponibles pour une partie."""

    MENU = "menu"
    EN_COURS = "en_cours"
    VICTOIRE = "victoire"
    DEFAITE = "defaite"


class EvenementPartie(Enum):
    """Ce qui vient de se passer dans la partie.

    La logique les signale, l'interface décide quoi en faire (jouer un son).
    """

    TIR_JOUEUR = auto()
    TIR_ENNEMI = auto()
    MINE_LANCEE = auto()
    EXPLOSION_MINE = auto()
    IMPACT_JOUEUR = auto()
    VICTOIRE = auto()
    DEFAITE = auto()
