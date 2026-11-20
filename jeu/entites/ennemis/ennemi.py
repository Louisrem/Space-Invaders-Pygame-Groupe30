from .comportements_tir import SansTir

class Ennemi:
    def __init__(self,x,y, comportement_tir=None, rapide=False, bouclier=None, pv=1):
        self.type_ennemi = "simple"
        self.x = x
        self.y = y
        self.hauteur = 25
        self.largeur = 40
        self.rapide = rapide
        self.bouclier = bouclier
        self.pv = pv

        if comportement_tir is None:
            comportement_tir = SansTir()

        self.comportement_tir = comportement_tir

    def zone_collision(self):
        return self.x, self.y, self.largeur, self.hauteur

    def tirer(self):
        return self.comportement_tir.tirer(self)

    def subir_impact(self):
        if self.bouclier is not None and self.bouclier.absorber_impact():
            return False

        self.pv -= 1
        return self.pv <= 0
