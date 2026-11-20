"""Vérifie les événements utilisés pour déclencher les sons."""

import unittest

from jeu.entites.ennemis.flotte import Flotte
from jeu.entites.vaisseau import Vaisseau
from jeu.etat_partie import EtatPartie
from jeu.evenements_partie import EvenementPartie
from jeu.partie import Partie


class TestEvenementsPartie(unittest.TestCase):
    """Vérifie le signal envoyé à l'interface sans initialiser Pygame."""

    def setUp(self):
        """Crée le vaisseau et une partie encore au menu."""
        self.joueur = Vaisseau(376, 550)
        self.partie = Partie(Flotte(("N",)), [], EtatPartie.MENU)

    def test_les_tirs_refuses_ne_signalent_rien(self):
        """Vérifie les tirs refusés au menu et lorsqu'un tir est actif."""
        self.partie.tirer_normal(self.joueur)
        self.partie.tirer_mine(self.joueur, 600)
        self.assertEqual(self.partie.recuperer_evenements(), [])

        self.partie.demarrer()
        self.partie.tirer_normal(self.joueur)
        self.partie.tirer_normal(self.joueur)
        self.partie.tirer_mine(self.joueur, 600)
        self.partie.tirer_mine(self.joueur, 600)
        self.assertEqual(
            self.partie.recuperer_evenements(),
            [EvenementPartie.TIR_JOUEUR, EvenementPartie.MINE_LANCEE],
        )
        self.assertEqual(self.partie.recuperer_evenements(), [])

    def test_le_barrage_est_signale_au_lancement(self):
        """Vérifie que le barrage est signalé après son avertissement."""
        partie = Partie(Flotte(("B",)), [])
        for _ in range(120):
            partie.actualiser_tirs_ennemis(600)
        self.assertEqual(partie.recuperer_evenements(), [])

        for _ in range(59):
            partie.actualiser_tirs_ennemis(600)
        self.assertEqual(partie.recuperer_evenements(), [])

        partie.actualiser_tirs_ennemis(600)
        self.assertEqual(len(partie.projectiles_ennemis), 3)
        self.assertEqual(
            partie.recuperer_evenements(), [EvenementPartie.BARRAGE_BOSS]
        )
