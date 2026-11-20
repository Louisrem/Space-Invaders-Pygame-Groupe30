class Projectile:
    def __init__(self, x, y, direction=-1):
        self.x = x
        self.y = y
        self.vitesse = 8
        self.largeur = 6
        self.hauteur = 12
        self.direction = direction

    def avancer(self):
        self.y = self.y + self.vitesse * self.direction

    def zone_collision(self):
        gauche = self.x - self.largeur // 2
        haut = self.y - self.hauteur
        return gauche, haut, self.largeur, self.hauteur

    def est_sorti_par_le_haut(self):
        return self.y <= 0

    def est_sorti_par_le_bas(self, hauteur_ecran):
        haut = self.y - self.hauteur
        return haut >= hauteur_ecran

class ProjectileBarrage(Projectile):
    def __init__(self, x):
        super().__init__(x, 0, direction=1)


class Mine(Projectile):
    rayon_detection = 22
    rayon_explosion = 65

    def __init__(self, x, y, hauteur_arret):
        super().__init__(x, y)
        self.largeur = 16
        self.hauteur = 16
        self.y_arret = hauteur_arret + self.hauteur // 2

    @property
    def centre(self):
        return self.x, self.y - self.hauteur // 2

    @property
    def armee(self):
        return self.y <= self.y_arret

    def avancer(self):
        if not self.armee:
            super().avancer()
            self.y = max(self.y, self.y_arret)

    def dans_rayon(self, zone, rayon):
        gauche, haut, largeur, hauteur = zone
        x, y = self.centre
        proche_x = max(gauche, min(x, gauche + largeur))
        proche_y = max(haut, min(y, haut + hauteur))
        return (x - proche_x) ** 2 + (y - proche_y) ** 2 <= rayon ** 2
