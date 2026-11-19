class Vaisseau:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.largeur = 40
        self.hauteur = 20

    def deplacer(self, distance):
        self.x = self.x + distance