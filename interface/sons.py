"""Charge et joue les effets WAV des événements de partie."""

import pygame

from jeu.evenements_partie import EvenementPartie

from .ressources import DOSSIER_ASSETS


class SonsJeu:
    """Associe les événements du jeu à des effets préchargés."""

    def __init__(self):
        """Charge les effets au démarrage si l'audio est disponible."""
        self._effets = {}
        if pygame.mixer.get_init() is None:
            try:
                pygame.mixer.init()
            except pygame.error:
                return

        dossier = DOSSIER_ASSETS / "sons" / "effets"
        for evenement in EvenementPartie:
            chemin = dossier / f"{evenement.value}.wav"
            self._effets[evenement] = pygame.mixer.Sound(chemin)

    def jouer_evenements(self, evenements):
        """Joue chaque effet au plus une fois pendant ce tour.

        :param evenements: Événements récupérés auprès de la partie.
        :type evenements: list[EvenementPartie]
        """
        for evenement in dict.fromkeys(evenements):
            effet = self._effets.get(evenement)
            if effet is not None:
                effet.play()
