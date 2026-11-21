"""Joue les effets WAV associés aux événements de la partie."""

from pathlib import Path

import pygame

from jeu.constantes import EvenementPartie

DOSSIER_SONS = Path(__file__).resolve().parent.parent / "assets" / "sons" / "effets"

# Événement -> fichier WAV. Les tirs ennemis n'ont pas de son exprès,
# sinon ça fait trop de bruit quand toute la flotte tire.
SONS = {
    EvenementPartie.TIR_JOUEUR: "tir_joueur.wav",
    EvenementPartie.MINE_LANCEE: "mine_lancee.wav",
    EvenementPartie.EXPLOSION_MINE: "explosion_mine.wav",
    EvenementPartie.IMPACT_JOUEUR: "impact_joueur.wav",
    EvenementPartie.VICTOIRE: "victoire.wav",
    EvenementPartie.DEFAITE: "defaite.wav",
}


class SonsJeu:
    """Associe chaque événement du jeu à un effet sonore."""

    def __init__(self):
        """Charge les effets si l'audio est disponible."""
        self._effets = {}
        try:
            pygame.mixer.init()
        except pygame.error:
            return

        for evenement, fichier in SONS.items():
            self._effets[evenement] = pygame.mixer.Sound(DOSSIER_SONS / fichier)

    def jouer(self, evenements):
        """Joue chaque effet au plus une fois pendant ce tour."""
        for evenement in dict.fromkeys(evenements):
            effet = self._effets.get(evenement)
            if effet is not None:
                effet.play()
