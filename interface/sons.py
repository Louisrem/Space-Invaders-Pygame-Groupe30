"""Joue les effets WAV associés aux événements de la partie."""

import pygame

from jeu.constantes import EvenementPartie

from .affichage import DOSSIER_ASSETS


class SonsJeu:
    """Associe chaque événement du jeu à un effet sonore."""

    def __init__(self):
        """Charge les effets si l'audio est disponible."""
        self._effets = {}
        try:
            pygame.mixer.init()
        except pygame.error:
            return

        dossier = DOSSIER_ASSETS / "sons" / "effets"
        for evenement in EvenementPartie:
            self._effets[evenement] = pygame.mixer.Sound(dossier / f"{evenement.value}.wav")

    def jouer(self, evenements):
        """Joue chaque effet au plus une fois pendant ce tour."""
        for evenement in dict.fromkeys(evenements):
            effet = self._effets.get(evenement)
            if effet is not None:
                effet.play()
