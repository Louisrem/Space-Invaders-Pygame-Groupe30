from jeu.flotte import Flotte
from jeu.vagues import VAGUES
from jeu.etat_partie import EtatPartie

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