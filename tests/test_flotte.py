"""Vérifie la création et le déplacement des formations ennemies."""

import unittest

from jeu.entites.ennemis.boss import Boss
from jeu.entites.ennemis.flotte import Flotte


class TestFlotte(unittest.TestCase):
    """Tests unitaires de la formation des ennemis."""

    def test_la_grille_cree_les_ennemis_du_catalogue(self):
        """Vérifie les types, les capacités et l'indépendance des tirs.
        """
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
        """Vérifie que l'erreur indique la lettre invalide."""
        with self.assertRaisesRegex(ValueError, "Case de vague inconnue : X"):
            Flotte(("X",))


    def test_les_groupes_accelerent_a_chaque_descente(self):
        """Vérifie trois descentes avec des rangées de vitesses différentes."""
        flotte = Flotte(("NN", "RR"))
        gauche, droite, rapide_gauche, rapide_droite = flotte.ennemis
        flotte.deplacer(800)
        self.assertEqual(gauche.x, 232)
        self.assertEqual(rapide_gauche.x, 233)

        descentes = 0
        for _ in range(1000):
            vitesse = flotte.vitesse
            hauteur = gauche.y
            flotte.deplacer(800)

            self.assertEqual(droite.x - gauche.x, 75)
            self.assertEqual(rapide_droite.x - rapide_gauche.x, 75)
            self.assertEqual(rapide_gauche.y - gauche.y, 45)
            for ennemi in flotte.ennemis:
                self.assertGreaterEqual(ennemi.x, 0)
                self.assertLessEqual(ennemi.x + ennemi.largeur, 800)

            if gauche.y == hauteur:
                self.assertEqual(flotte.vitesse, vitesse)
            else:
                self.assertEqual(gauche.y - hauteur, 25)
                self.assertEqual(flotte.vitesse, vitesse + 0.25)
                descentes += 1
                if descentes == 3:
                    break

        self.assertEqual(descentes, 3)

    def test_la_rangee_rapide_accelere_quand_elle_reste_seule(self):
        """Vérifie que les rapides peuvent déclencher la descente."""
        flotte = Flotte(("R",))
        rapide = flotte.ennemis[0]
        rapide.x = 800 - rapide.largeur
        hauteur = rapide.y

        flotte.deplacer(800)
        self.assertEqual(rapide.y, hauteur + 25)
        self.assertEqual(flotte.vitesse, 2.25)

        position = rapide.x
        flotte.deplacer(800)
        self.assertEqual(position - rapide.x, 3.25)
