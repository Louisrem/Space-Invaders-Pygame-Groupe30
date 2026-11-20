class Coeur:
    largeur = 24
    hauteur = 24
    vitesse = 9

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def avancer(self):
        self.y += self.vitesse

    def zone_collision(self):
        return self.x, self.y, self.largeur, self.hauteur

    def est_sorti_par_le_bas(self, hauteur_ecran):
        return self.y >= hauteur_ecran