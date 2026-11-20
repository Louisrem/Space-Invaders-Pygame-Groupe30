from .comportements_tir import SansTir

class Ennemi:
    def __init__(self,x,y, comportement_tir=None, rapide=False):
        self.x = x
        self.y = y
        self.hauteur = 25
        self.largeur = 40
        self.rapide = rapide

        if comportement_tir is None:
            comportement_tir = SansTir()

        self.comportement_tir = comportement_tir

    def zone_collision(self):
        return (self.x, self.y, self.largeur, self.hauteur)

    def tirer(self):
        return self.comportement_tir.tirer(self)
