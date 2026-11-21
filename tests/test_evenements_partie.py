"""Vérifie les événements utilisés pour déclencher les sons."""

import random
import unittest
from unittest.mock import patch

from jeu.entites.ennemis.flotte import Flotte
from jeu.entites.vaisseau import Vaisseau
from jeu.etat_partie import EtatPartie
from jeu.evenements_partie import EvenementPartie
from jeu.partie import Partie
from jeu.terrain import LARGEUR_TERRAIN


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
        boss = partie.flotte.ennemis[0]
        for _ in range(120):
            partie.actualiser_tirs_ennemis(600)
        annonce = boss.colonnes_barrage()[:]
        self.assertEqual(len(annonce), 3)
        self.assertEqual(partie.recuperer_evenements(), [])

        for _ in range(59):
            boss.x += 2
            partie.actualiser_tirs_ennemis(600)
            self.assertEqual(boss.colonnes_barrage(), annonce)
        self.assertEqual(partie.recuperer_evenements(), [])

        partie.actualiser_tirs_ennemis(600)
        self.assertEqual([tir.x for tir in partie.projectiles_ennemis], annonce)
        self.assertEqual(boss.colonnes_barrage(), [])
        self.assertEqual(
            partie.recuperer_evenements(), [EvenementPartie.BARRAGE_BOSS]
        )

    def test_les_colonnes_du_barrage_varient_et_laissent_de_la_place(self):
        """Vérifie les écarts variables et la place pour le vaisseau."""
        boss = Flotte(("B",)).ennemis[0]
        hasard = random.Random(30)
        annonces = set()
        espacements = set()
        with patch("jeu.entites.ennemis.comportements_tir.sample", hasard.sample):
            for _ in range(16):
                for _ in range(120):
                    boss.tirer()
                annonce = tuple(boss.colonnes_barrage())
                for _ in range(59):
                    boss.tirer()
                tirs = boss.tirer()

                self.assertEqual(len(set(annonce)), 3)
                self.assertEqual(tuple(tir.x for tir in tirs), annonce)
                zones = [tir.zone_collision() for tir in tirs]
                self.assertGreaterEqual(zones[0][0], 0)
                self.assertLessEqual(zones[-1][0] + zones[-1][2], LARGEUR_TERRAIN)
                for gauche, droite in zip(zones, zones[1:]):
                    espace = droite[0] - (gauche[0] + gauche[2])
                    self.assertGreater(espace, self.joueur.largeur)
                annonces.add(annonce)
                espacements.add((annonce[1] - annonce[0], annonce[2] - annonce[1]))

        self.assertGreater(len(annonces), 1)
        self.assertGreater(len(espacements), 1)
