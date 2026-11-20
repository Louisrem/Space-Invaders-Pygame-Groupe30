from abc import ABC, abstractmethod
from jeu.projectiles import Projectile, ProjectileBarrage
from random import randint

class ComportementTir(ABC):
    @abstractmethod
    def tirer(self, ennemi):
        pass

class SansTir(ComportementTir):
    def tirer(self, ennemi):
        return []

class TirSimple(ComportementTir):
    def __init__(self, delai=120):
        self.delai = delai
        self.tours_restants = self._nouveau_delai()

    def tirer(self, ennemi):
        if self.tours_restants > 0:
            self.tours_restants -= 1
            return []

        x = ennemi.x + ennemi.largeur // 2
        bas_ennemi = ennemi.y + ennemi.hauteur

        projectile = Projectile(x, bas_ennemi, direction=1)
        projectile.y += projectile.hauteur

        self.tours_restants = self._nouveau_delai()
        return [projectile]

    def _nouveau_delai(self):
        return randint(self.delai // 2, self.delai * 3 // 2)

class TirDeBarrage(ComportementTir):
    def __init__(self):
        self.tours_restants = 120
        self.colonnes_annoncees = []

    def tirer(self, ennemi):
        self.tours_restants -= 1
        if self.tours_restants > 0:
            return []

        if not self.colonnes_annoncees:
            centre = ennemi.x + ennemi.largeur // 2
            ecart = ennemi.largeur // 3
            self.colonnes_annoncees = [centre - ecart, centre, centre + ecart]
            self.tours_restants = 60
            return []

        projectiles = [ProjectileBarrage(x) for x in self.colonnes_annoncees]
        self.colonnes_annoncees = []
        self.tours_restants = 120
        return projectiles