class Projectile:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vitesse = 8
        self.largeur = 6
        self.hauteur = 12

    def avancer(self):
        self.y = self.y - self.vitesse

    def zone_collision(self):
        gauche = self.x - self.largeur // 2
        haut = self.y - self.hauteur
        return (gauche, haut, self.largeur, self.hauteur)

    def est_sorti_par_le_haut(self):
        return self.y <= 0