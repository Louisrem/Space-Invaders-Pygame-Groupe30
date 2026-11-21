"""Vérifie la création et le déplacement de la flotte."""

import unittest

from jeu.ennemis import Boss, Ennemi, Tireur
from jeu.flotte import Flotte


class TestFlotte(unittest.TestCase):
    """Tests unitaires de la formation des ennemis."""

    def test_la_grille_cree_les_ennemis_du_catalogue(self):
        """Les lettres créent les bons types, et un point laisse une case vide."""
        flotte = Flotte(("N.TB",))
        self.assertEqual([type(e) for e in flotte], [Ennemi, Tireur, Boss])
        self.assertEqual(len(flotte), 3)
        self.assertEqual(list(flotte)[2].pv, 3)

    def test_une_lettre_inconnue_signale_la_case(self):
        """L'erreur indique la lettre invalide."""
        with self.assertRaisesRegex(ValueError, "Case de vague inconnue : X"):
            Flotte(("X",))

    def test_la_flotte_descend_et_change_de_sens_au_bord(self):
        """Au bord, toute la flotte descend et repart dans l'autre sens."""
        flotte = Flotte(("N",))
        ennemi = list(flotte)[0]
        ennemi.x = 800 - ennemi.largeur
        y_depart = ennemi.y

        flotte.deplacer(800)
        self.assertEqual(ennemi.y, y_depart + Flotte.DESCENTE)
        flotte.deplacer(800)
        self.assertLess(ennemi.x, 800 - ennemi.largeur)


if __name__ == "__main__":
    unittest.main()
