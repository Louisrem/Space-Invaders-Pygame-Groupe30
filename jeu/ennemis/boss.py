from .ennemi import Ennemi

class Boss(Ennemi):
    def __init__(self, x, y):
        super().__init__(x, y, pv=3) # On réutilise Ennemi avec super() on file juste 3pv

        centre_x = self.x + self.largeur // 2
        self.largeur = 64
        self.hauteur = 35
        self.x = centre_x - self.largeur // 2