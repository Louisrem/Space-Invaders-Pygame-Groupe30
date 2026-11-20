from jeu.flotte import Flotte
from jeu.vagues import BONUS_PAR_VAGUE, VAGUES
from jeu.etat_partie import EtatPartie
from random import randint
from jeu.projectiles import Mine

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
        self.bonus = None
        self.tours_avant_bonus = None
        self.mine = None
        self.explosion_mine = None
        self.tours_explosion_mine = 0

    def gerer_collisions(self):
        for projectile in self.projectiles[:]:
            for ennemi in self.flotte.ennemis:
                if rectangles_se_chevauchent(
                    projectile.zone_collision(), ennemi.zone_collision()
               ):
                    self.projectiles.remove(projectile)

                    self._appliquer_impact(ennemi)
                    break

    def _appliquer_impact(self, ennemi):
        if ennemi.subir_impact():
            self.flotte.ennemis.remove(ennemi)
            self.score += 1

    def tirer_mine(self, joueur, hauteur_ecran):
        if self.etat == EtatPartie.EN_COURS and self.mine is None:
            x = joueur.x + joueur.largeur // 2
            self.mine = Mine(x, joueur.y, hauteur_ecran // 2)

    def actualiser_mine(self):
        if self.tours_explosion_mine > 0:
            self.tours_explosion_mine -= 1
            if self.tours_explosion_mine == 0:
                self.explosion_mine = None

        mine = self.mine
        if mine is None:
            return

        mine.avancer()
        if not mine.armee:
            return

        if not any(
            mine.dans_rayon(ennemi.zone_collision(), mine.rayon_detection)
            for ennemi in self.flotte.ennemis
        ):
            return

        self.mine = None
        self.explosion_mine = (mine.centre, mine.rayon_explosion)
        self.tours_explosion_mine = 12

        for ennemi in self.flotte.ennemis[:]:
            if mine.dans_rayon(ennemi.zone_collision(), mine.rayon_explosion):
                self._appliquer_impact(ennemi)

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
            self.tours_avant_bonus = None
            if self.niveau in BONUS_PAR_VAGUE:
                self.tours_avant_bonus = randint(120, 300)
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
                joueur.subir_impact()

    def actualiser_bonus(self, joueur, largeur_ecran, hauteur_ecran):
        if self.tours_avant_bonus is not None:
            self.tours_avant_bonus -= 1

            if self.tours_avant_bonus == 0:
                type_bonus = BONUS_PAR_VAGUE[self.niveau]
                milieu = joueur.x + (joueur.largeur - type_bonus.largeur) // 2
                gauche = max(0, milieu - 160)
                droite = min(largeur_ecran - type_bonus.largeur, milieu + 160)

                self.bonus = type_bonus(randint(gauche, droite), 0)
                self.tours_avant_bonus = None

        if self.bonus is None:
            return

        self.bonus.avancer()

        if rectangles_se_chevauchent(
            self.bonus.zone_collision(), joueur.zone_collision()
        ):
            self.bonus.appliquer(joueur)
            self.bonus = None
        elif self.bonus.est_sorti_par_le_bas(hauteur_ecran):
            self.bonus = None