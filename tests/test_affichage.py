"""Vérifie le choix des images, sans ouvrir de fenêtre."""

import unittest

from interface.affichage import nom_image
from jeu.ennemis import Boss, Ennemi, Tireur
from jeu.projectiles import Mine, Projectile


class TestAffichage(unittest.TestCase):
    """Tests de nom_image()."""

    def test_chaque_classe_a_son_image(self):
        """Ennemis et tirs prennent l'image prévue pour leur classe."""
        self.assertEqual(nom_image(Ennemi(0, 0)), "simple")
        self.assertEqual(nom_image(Boss(0, 0)), "boss")
        self.assertEqual(nom_image(Projectile(0, 0)), "tir_joueur")
        self.assertEqual(nom_image(Projectile(0, 0, direction=1)), "tir_ennemi")
        self.assertEqual(nom_image(Mine(0, 500)), "mine")

    def test_une_nouvelle_sous_classe_prend_l_image_de_sa_mere(self):
        """Une classe ajoutée sans image ne fait pas planter le jeu."""
        class TireurRapide(Tireur):
            pass

        class TirDouble(Projectile):
            pass

        self.assertEqual(nom_image(TireurRapide(0, 0)), "tireur")
        self.assertEqual(nom_image(TirDouble(0, 0)), "tir_joueur")


if __name__ == "__main__":
    unittest.main()
