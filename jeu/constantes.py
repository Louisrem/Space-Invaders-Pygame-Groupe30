"""Constantes partagées : taille du terrain, états et événements de la partie."""

from enum import Enum

LARGEUR_TERRAIN = 800
HAUTEUR_TERRAIN = 600


class EtatPartie(Enum):
    """Énumère les états disponibles pour une partie."""

    MENU = "menu"
    EN_COURS = "en_cours"
    VICTOIRE = "victoire"
    DEFAITE = "defaite"


class EvenementPartie(Enum):
    """Événements que la logique signale pour que l'interface joue un son.

    La valeur de chaque événement est aussi le nom du fichier WAV joué.
    """

    TIR_JOUEUR = "tir_joueur"
    MINE_LANCEE = "mine_lancee"
    EXPLOSION_MINE = "explosion_mine"
    IMPACT_JOUEUR = "impact_joueur"
    VICTOIRE = "victoire"
    DEFAITE = "defaite"
