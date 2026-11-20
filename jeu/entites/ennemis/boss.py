from .ennemi import Ennemi
from .comportements_tir import TirDeBarrage

class Boss(Ennemi):
    def __init__(self, x, y):
        super().__init__(x, y, comportement_tir=TirDeBarrage(), pv=3) # On réutilise Ennemi avec super() on file juste 3pv

        self.type_ennemi = "boss"
        centre_x = self.x + self.largeur // 2
        self.largeur = 64
        self.hauteur = 35
        self.x = centre_x - self.largeur // 2

    def colonnes_barrage(self):
        return self.comportement_tir.colonnes_annoncees
