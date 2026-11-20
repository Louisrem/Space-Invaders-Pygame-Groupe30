import unittest

from jeu.entites.ennemis.boss import Boss
from jeu.entites.ennemis.flotte import Flotte


class TestFlotte(unittest.TestCase):
    def test_la_grille_cree_les_ennemis_du_catalogue(self):
        flotte = Flotte(("N.TRPB",))

        self.assertEqual(
            [ennemi.type_ennemi for ennemi in flotte.ennemis],
            ["simple", "tireur", "rapide", "protege", "boss"],
        )
        _, tireur, rapide, protege, boss = flotte.ennemis
        self.assertTrue(rapide.rapide)
        self.assertTrue(protege.bouclier.actif)
        self.assertIsInstance(boss, Boss)
        self.assertIsNot(tireur.comportement_tir, rapide.comportement_tir)

    def test_une_lettre_inconnue_signale_la_case(self):
        with self.assertRaisesRegex(ValueError, "Case de vague inconnue : X"):
            Flotte(("X",))
