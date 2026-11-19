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