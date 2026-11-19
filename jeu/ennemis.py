class Ennemi:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.hauteur = 25
        self.largeur = 40

    def zone_collision(self):
        return (self.x, self.y, self.largeur, self.hauteur)