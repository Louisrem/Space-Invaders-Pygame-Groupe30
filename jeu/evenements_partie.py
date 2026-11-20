"""Événements que la logique signale après une action du jeu."""

from enum import Enum


class EvenementPartie(Enum):
    """Identifie une action terminée ou un changement d'état."""

    TIR_JOUEUR = "tir_joueur"
    MINE_LANCEE = "mine_lancee"
    EXPLOSION_MINE = "explosion_mine"
    BARRAGE_BOSS = "barrage_boss"
    IMPACT_JOUEUR = "impact_joueur"
    BONUS_RAMASSE = "bonus_ramasse"
    VICTOIRE = "victoire"
    DEFAITE = "defaite"
