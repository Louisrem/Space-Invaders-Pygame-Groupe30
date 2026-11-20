import unittest

from jeu.entites.ennemis.flotte import Flotte
from jeu.entites.projectiles import Projectile
from jeu.entites.vaisseau import Vaisseau
from jeu.etat_partie import EtatPartie
from jeu.partie import Partie


class TestPartie(unittest.TestCase):
    def setUp(self):
        self.joueur = Vaisseau(376, 550)

    def test_le_menu_ne_fait_pas_avancer_la_flotte(self):
        flotte = Flotte(("N",))
        partie = Partie(flotte, [], etat_initial=EtatPartie.MENU)
        position = flotte.ennemis[0].x

        partie.actualiser(self.joueur, 800, 600)
        self.assertEqual(flotte.ennemis[0].x, position)

        partie.demarrer()
        partie.actualiser(self.joueur, 800, 600)
        self.assertGreater(flotte.ennemis[0].x, position)

    def test_une_flotte_vide_passe_a_la_vague_suivante(self):
        partie = Partie(Flotte((".",)), [])
        partie.actualiser(self.joueur, 800, 600)
        self.assertEqual(partie.niveau, 2)
        self.assertEqual(len(partie.flotte.ennemis), 15)

    def test_un_ennemi_a_la_hauteur_du_vaisseau_declenche_la_defaite(self):
        flotte = Flotte(("N",))
        ennemi = flotte.ennemis[0]
        ennemi.y = self.joueur.y - ennemi.hauteur
        partie = Partie(flotte, [])

        partie.actualiser(self.joueur, 800, 600)

        self.assertEqual(partie.etat, EtatPartie.DEFAITE)
        self.assertEqual(partie.resultat()["issue"], "defaite")

    def test_la_mine_se_recharge_apres_cinq_eliminations(self):
        flotte = Flotte(("NNNNN",))
        tirs = []
        partie = Partie(flotte, tirs)
        partie.tirer_mine(self.joueur, 600)

        cible = flotte.ennemis[0]
        cible.x, cible.y = 380, 300
        for _ in range(40):
            partie.actualiser_mine()

        self.assertIsNone(partie.mine)
        self.assertEqual(partie.score, 1)
        partie.tirer_mine(self.joueur, 600)
        self.assertEqual(partie.mines_lancees, 1)

        for ennemi in flotte.ennemis[:]:
            tirs.append(Projectile(ennemi.x + 20, ennemi.y + 12))
        partie.gerer_collisions()
        self.assertEqual(partie.ennemis_avant_mine(), 0)

        partie.tirer_mine(self.joueur, 600)
        self.assertIsNotNone(partie.mine)
        self.assertEqual(partie.mines_lancees, 2)
