"""Vérifie les règles d'une partie sans ouvrir de fenêtre."""

import unittest
from unittest.mock import patch

from jeu.entites.ennemis.flotte import Flotte
from jeu.entites.projectiles import Projectile
from jeu.entites.vaisseau import Vaisseau
from jeu.etat_partie import EtatPartie
from jeu.partie import Partie


class TestPartie(unittest.TestCase):
    """Tests unitaires de l'évolution d'une partie."""

    def setUp(self):
        """Crée un vaisseau neuf pour chaque test."""
        self.joueur = Vaisseau(376, 550)

    def test_le_menu_ne_fait_pas_avancer_la_flotte(self):
        """Vérifie que la flotte bouge seulement après le démarrage."""
        flotte = Flotte(("N",))
        partie = Partie(flotte, [], etat_initial=EtatPartie.MENU)
        position = flotte.ennemis[0].x

        partie.actualiser(self.joueur, 800, 600)
        self.assertEqual(flotte.ennemis[0].x, position)

        partie.demarrer()
        partie.actualiser(self.joueur, 800, 600)
        self.assertGreater(flotte.ennemis[0].x, position)

    def test_la_pause_fige_le_jeu_et_le_chronometre(self):
        """Vérifie que la reprise conserve la flotte et exclut l'attente."""
        flotte = Flotte(("N",))
        with patch("jeu.partie.monotonic", return_value=10) as horloge:
            partie = Partie(flotte, [])
            position = flotte.ennemis[0].x
            horloge.return_value = 15
            partie.mettre_en_pause()

            horloge.return_value = 35
            partie.actualiser(self.joueur, 800, 600)
            self.assertEqual(partie.etat, EtatPartie.PAUSE)
            self.assertEqual(flotte.ennemis[0].x, position)
            self.assertEqual(partie.duree_secondes(), 5)

            partie.reprendre()
            horloge.return_value = 37
            partie.actualiser(self.joueur, 800, 600)
            self.assertEqual(partie.etat, EtatPartie.EN_COURS)
            self.assertGreater(flotte.ennemis[0].x, position)
            self.assertEqual(partie.duree_secondes(), 7)

    def test_une_flotte_vide_passe_a_la_vague_suivante(self):
        """Vérifie qu'une vague vidée charge la formation suivante."""
        partie = Partie(Flotte((".",)), [])
        partie.actualiser(self.joueur, 800, 600)
        self.assertEqual(partie.niveau, 2)
        self.assertEqual(len(partie.flotte.ennemis), 15)

    def test_un_ennemi_a_la_hauteur_du_vaisseau_declenche_la_defaite(self):
        """Vérifie la défaite si la flotte atteint le joueur."""
        flotte = Flotte(("N",))
        ennemi = flotte.ennemis[0]
        ennemi.y = self.joueur.y - ennemi.hauteur
        partie = Partie(flotte, [])

        partie.actualiser(self.joueur, 800, 600)

        self.assertEqual(partie.etat, EtatPartie.DEFAITE)
        self.assertEqual(partie.resultat()["issue"], "defaite")

    def test_le_dernier_ennemi_est_touche_au_moment_de_descendre(self):
        """Vérifie la priorité de la défaite lors d'un impact simultané."""
        self.joueur.x = 0
        cas = (
            (0, EtatPartie.DEFAITE, 1, 0),
            (1, EtatPartie.EN_COURS, 2, 1),
        )
        for marge, etat_attendu, niveau_attendu, score_attendu in cas:
            with self.subTest(pixels_avant_la_ligne=marge):
                flotte = Flotte(("N",))
                flotte.direction = -1
                ennemi = flotte.ennemis[0]
                ennemi.x = 0
                ennemi.y = self.joueur.y - ennemi.hauteur - 25 - marge
                partie = Partie(flotte, [])
                partie.tirer_normal(self.joueur)

                partie.actualiser(self.joueur, 800, 600)

                self.assertEqual(ennemi.y + ennemi.hauteur, self.joueur.y - marge)
                self.assertEqual(partie.etat, etat_attendu)
                self.assertEqual(partie.niveau, niveau_attendu)
                self.assertEqual(partie.score, score_attendu)

    def test_la_mine_se_recharge_apres_cinq_eliminations(self):
        """Vérifie la recharge de la mine après cinq éliminations."""
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
