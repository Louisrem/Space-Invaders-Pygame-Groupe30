from jeu.flotte import Flotte
from jeu.vagues import VAGUES, VAGUES_AVEC_COEUR
from jeu.etat_partie import EtatPartie
from random import randint
from jeu.bonus import Coeur

def rectangles_se_chevauchent(zone_a, zone_b):
    x_a, y_a, largeur_a, hauteur_a = zone_a
    x_b, y_b, largeur_b, hauteur_b = zone_b

    chevauchement_x = x_a < x_b + largeur_b and x_a + largeur_a > x_b
    chevauchement_y = y_a < y_b + hauteur_b and y_a + hauteur_a > y_b

    return chevauchement_x and chevauchement_y

class Partie:
    def __init__(self, flotte, projectiles):
        self.flotte = flotte
        self.projectiles = projectiles
        self.score = 0
        self.niveau = 1
        self.projectiles_ennemis = []
        self.etat = EtatPartie.EN_COURS
        self.coeur = None
        self.tours_avant_coeur = None

    def gerer_collisions(self):
        for projectile in self.projectiles[:]:
            for ennemi in self.flotte.ennemis:
                if rectangles_se_chevauchent(
                    projectile.zone_collision(), ennemi.zone_collision()
               ):
                    self.projectiles.remove(projectile)

                    if ennemi.subir_impact():
                        self.flotte.ennemis.remove(ennemi)
                        self.score += 1
                    break

    def retirer_projectiles_hors_ecran(self):
        for projectile in self.projectiles[:]:
            if projectile.est_sorti_par_le_haut():
                self.projectiles.remove(projectile)

    def verifier_fin_vague(self):
        if self.flotte.ennemis:
            return

        vague_suivante = self.niveau + 1

        if vague_suivante in VAGUES:
            self.flotte = Flotte(VAGUES[vague_suivante])
            self.niveau = vague_suivante
            if self.niveau in VAGUES_AVEC_COEUR:
                self.tours_avant_coeur = randint(120, 300)
        else:
            self.etat = EtatPartie.VICTOIRE

    def verifier_defaite(self, joueur):
        if joueur.vies == 0:
            self.etat = EtatPartie.DEFAITE
            return

        for ennemi in self.flotte.ennemis:
            bas_ennemi = ennemi.y + ennemi.hauteur
            if bas_ennemi >= joueur.y:
                self.etat = EtatPartie.DEFAITE
                return

    def actualiser_tirs_ennemis(self, hauteur_ecran):
        for ennemi in self.flotte.ennemis:
            self.projectiles_ennemis.extend(ennemi.tirer())

        for projectile in self.projectiles_ennemis[:]:
            projectile.avancer()

            if projectile.est_sorti_par_le_bas(hauteur_ecran):
                self.projectiles_ennemis.remove(projectile)

    def gerer_impacts_joueur(self, joueur):
        for projectile in self.projectiles_ennemis[:]:
            if rectangles_se_chevauchent(projectile.zone_collision(), joueur.zone_collision()):
                self.projectiles_ennemis.remove(projectile)
                joueur.perdre_vie()

    def actualiser_coeur(self, joueur, largeur_ecran, hauteur_ecran):
        if self.tours_avant_coeur is not None:
            self.tours_avant_coeur -= 1

            if self.tours_avant_coeur == 0:
                milieu = joueur.x + (joueur.largeur - Coeur.largeur) // 2
                gauche = max(0, milieu - 160)
                droite = min(largeur_ecran - Coeur.largeur, milieu + 160)

                self.coeur = Coeur(randint(gauche, droite), 0)
                self.tours_avant_coeur = None

        if self.coeur is None:
            return

        self.coeur.avancer()

        if rectangles_se_chevauchent(
            self.coeur.zone_collision(), joueur.zone_collision()
        ):
            joueur.gagner_vie()
            self.coeur = None
        elif self.coeur.est_sorti_par_le_bas(hauteur_ecran):
            self.coeur = None