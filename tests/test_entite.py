"""Vérifie la classe mère Entite."""

import unittest

from jeu.ennemis import Boss
from jeu.entite import Entite
from jeu.projectiles import Mine
from jeu.vaisseau import Vaisseau


class TestEntite(unittest.TestCase):
    """Tests de la classe mère commune."""

    def test_vaisseau_ennemi_et_projectile_sont_des_entites(self):
        """Les trois familles d'objets héritent d'Entite."""
        for objet in (Vaisseau(0, 0), Boss(0, 0), Mine(0, 0)):
            self.assertIsInstance(objet, Entite)

    def test_zone_collision_par_defaut(self):
        """Par défaut, la zone part du coin en haut à gauche."""
        self.assertEqual(Vaisseau(10, 20).zone_collision(), (10, 20, 48, 24))

    def test_touche_detecte_le_chevauchement(self):
        """Deux entités qui se recouvrent se touchent, sinon non."""
        joueur = Vaisseau(100, 100)
        self.assertTrue(joueur.touche(Vaisseau(120, 110)))
        self.assertFalse(joueur.touche(Vaisseau(200, 100)))


if __name__ == "__main__":
    unittest.main()
