"""Vérifie les règles d'une partie sans ouvrir de fenêtre."""

import random
import unittest

from jeu.constantes import EtatPartie, EvenementPartie
from jeu.ennemis import Boss
from jeu.partie import Partie
from jeu.projectiles import Mine, Projectile


def placer(entite, x, y):
    """Met une entité à une position précise pour préparer un test."""
    entite.decaler(x - entite.x, y - entite.y)


class TestPartie(unittest.TestCase):
    """Tests unitaires de l'évolution d'une partie."""

    def test_le_menu_ne_fait_pas_avancer_la_flotte(self):
        """La flotte bouge seulement après le démarrage."""
        partie = Partie({1: ("N",)})
        ennemi = list(partie.flotte)[0]
        position = ennemi.x

        partie.actualiser()
        self.assertEqual(ennemi.x, position)

        partie.demarrer()
        partie.actualiser()
        self.assertGreater(ennemi.x, position)

    def test_un_seul_tir_de_chaque_arme_a_la_fois(self):
        """On peut avoir un tir normal et une mine, mais pas deux tirs."""
        partie = Partie({1: ("N",)}, etat_initial=EtatPartie.EN_COURS)
        partie.tirer(Projectile)
        partie.tirer(Projectile)
        partie.tirer(Mine)
        self.assertEqual(
            [type(p) for p in partie.projectiles_joueur], [Projectile, Mine]
        )
        self.assertEqual(
            partie.recuperer_evenements(),
            [EvenementPartie.TIR_JOUEUR, EvenementPartie.MINE_LANCEE],
        )

    def test_un_tir_elimine_un_ennemi_et_augmente_le_score(self):
        """Un tir qui touche un ennemi à 1 PV l'élimine."""
        partie = Partie({1: ("NN",), 2: ("N",)}, etat_initial=EtatPartie.EN_COURS)
        ennemi = list(partie.flotte)[0]
        placer(ennemi, partie.joueur.x, partie.joueur.y - 100)
        partie.tirer(Projectile)

        for _ in range(20):
            partie.actualiser()
        self.assertEqual(partie.score, 1)
        self.assertEqual(len(partie.flotte), 1)

    def test_le_boss_resiste_a_deux_tirs(self):
        """Le boss perd un PV par tir et survit aux deux premiers."""
        partie = Partie({1: ("B",)}, etat_initial=EtatPartie.EN_COURS)
        boss = list(partie.flotte)[0]
        self.assertFalse(boss.subir_impact())
        self.assertFalse(boss.subir_impact())
        self.assertTrue(boss.subir_impact())

    def test_le_boss_blesse_tire_plus_souvent(self):
        """Après un impact, le boss tire plus de projectiles sur la même durée."""
        def tirs_sur(boss, tours):
            return sum(len(boss.tirer()) for _ in range(tours))

        random.seed(0)
        intact = tirs_sur(Boss(0, 0), 600)
        random.seed(0)
        blesse = Boss(0, 0)
        blesse.subir_impact()
        self.assertGreater(tirs_sur(blesse, 600), intact)

    def test_les_ennemis_tirent_sur_le_vaisseau(self):
        """Un tir ennemi qui touche le vaisseau lui retire une vie."""
        partie = Partie({1: ("T",)}, etat_initial=EtatPartie.EN_COURS)
        joueur = partie.joueur
        tireur = list(partie.flotte)[0]
        placer(tireur, tireur.x, joueur.y - 60)

        for _ in range(300):
            placer(joueur, tireur.x, joueur.y)  # le vaisseau reste sous le tireur
            partie.actualiser()
            if joueur.vies < 3:
                break
        self.assertEqual(joueur.vies, 2)
        evenements = partie.recuperer_evenements()
        self.assertIn(EvenementPartie.TIR_ENNEMI, evenements)
        self.assertIn(EvenementPartie.IMPACT_JOUEUR, evenements)

    def test_la_mine_armee_touche_les_ennemis_dans_son_rayon(self):
        """La mine explose près d'un ennemi et touche tous ceux du rayon."""
        partie = Partie({1: ("NN",), 2: ("N",)}, etat_initial=EtatPartie.EN_COURS)
        mine = Mine(400, 400)
        while not mine.armee:
            mine.avancer()
        a, b = list(partie.flotte)
        placer(a, mine.x - 20, mine.y - 30)
        placer(b, mine.x + 30, mine.y - 30)

        self.assertEqual(mine.ennemis_touches(partie.flotte), [a, b])

    def test_une_flotte_vide_passe_a_la_vague_suivante_puis_victoire(self):
        """Une vague vidée charge la suivante ; la dernière donne la victoire."""
        partie = Partie({1: (".",), 2: (".",)}, etat_initial=EtatPartie.EN_COURS)
        partie.actualiser()
        self.assertEqual(partie.niveau, 2)
        partie.actualiser()
        self.assertEqual(partie.etat, EtatPartie.VICTOIRE)

    def test_perdre_toutes_ses_vies_donne_la_defaite(self):
        """La partie se termine quand le vaisseau n'a plus de vie."""
        partie = Partie({1: ("N",)}, etat_initial=EtatPartie.EN_COURS)
        for _ in range(3):
            partie.joueur.perdre_vie()
        partie.actualiser()
        self.assertEqual(partie.etat, EtatPartie.DEFAITE)

    def test_l_etat_de_la_partie_est_en_lecture_seule(self):
        """Vies, score et listes de tirs ne se modifient pas de l'extérieur."""
        partie = Partie()
        with self.assertRaises(AttributeError):
            partie.joueur.vies = 99
        with self.assertRaises(AttributeError):
            partie.score = 99
        with self.assertRaises(AttributeError):
            partie.projectiles_joueur.append(Projectile(0, 0))


    def test_representations_lisibles(self):
        """__repr__ et __str__ affichent des textes lisibles (cours 3, labo 3)."""
        self.assertEqual(str(Partie()), "Vague 1 · score 0 · 3 vies")
        self.assertEqual(repr(Boss(230, 60)), "Boss(x=218, y=60, pv=3)")
        self.assertEqual(repr(Mine(400, 550)), "Mine(x=400, y=550)")
        self.assertEqual(repr(Partie().joueur), "Vaisseau(x=376, vies=3)")

    def test_le_vaisseau_avance_de_sa_vitesse(self):
        """deplacer_joueur(1) avance le vaisseau de Vaisseau.VITESSE pixels."""
        partie = Partie({1: ("N",)}, etat_initial=EtatPartie.EN_COURS)
        depart = partie.joueur.x
        partie.deplacer_joueur(1)
        self.assertEqual(partie.joueur.x, depart + partie.joueur.VITESSE)

    def test_le_boss_rapporte_plus_de_points(self):
        """Éliminer le boss rapporte Boss.POINTS et pas 1 seul point."""
        partie = Partie({1: ("B",), 2: ("N",)}, etat_initial=EtatPartie.EN_COURS)
        boss = list(partie.flotte)[0]
        boss.subir_impact()
        boss.subir_impact()  # il ne lui reste qu'un PV
        placer(boss, partie.joueur.x, partie.joueur.y - 100)
        partie.tirer(Projectile)
        for _ in range(20):
            partie.actualiser()
        self.assertEqual(partie.score, Boss.POINTS)


if __name__ == "__main__":
    unittest.main()
