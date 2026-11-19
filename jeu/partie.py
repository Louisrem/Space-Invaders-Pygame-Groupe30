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

    def gerer_collisions(self):
        for projectile in self.projectiles[:]:
            for ennemi in self.flotte.ennemis:
                if rectangles_se_chevauchent(
                    projectile.zone_collision(), ennemi.zone_collision()
               ):
                    self.flotte.ennemis.remove(ennemi)
                    self.projectiles.remove(projectile)
                    self.score += 1
                    break

    def retirer_projectiles_hors_ecran(self):
        for projectile in self.projectiles[:]:
            if projectile.est_sorti_par_le_haut():
                self.projectiles.remove(projectile)