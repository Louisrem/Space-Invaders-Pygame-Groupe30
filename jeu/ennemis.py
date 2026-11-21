"""Les ennemis et leurs comportements de tir.

- ComportementTir (abstraite), SansTir, TirSimple : décident quand un ennemi
  tire. Pour un nouveau comportement, hérite de ComportementTir.
- Ennemi : possède un ComportementTir (composition).
- Tireur : hérite d'Ennemi et tire à intervalles aléatoires.
- Boss : hérite d'Ennemi, plus grand, 3 points de vie, et redéfinit
  subir_impact() pour tirer plus vite quand il est blessé.
"""

from abc import ABC, abstractmethod
from random import randint

from .entite import Entite
from .projectiles import Projectile


class ComportementTir(ABC):
    """Interface commune à tous les comportements de tir."""

    @abstractmethod
    def tirer(self, ennemi):
        """Renvoie les projectiles que l'ennemi lance à ce tour.

        :param ennemi: Ennemi qui utilise ce comportement.
        :type ennemi: Ennemi
        :return: Les projectiles à lancer (liste vide si aucun).
        :rtype: list[Projectile]
        """


class SansTir(ComportementTir):
    """Comportement par défaut : l'ennemi ne tire jamais."""

    def tirer(self, ennemi):
        """Ne lance aucun projectile."""
        return []


class TirSimple(ComportementTir):
    """Tire un projectile vers le bas à intervalles aléatoires."""

    def __init__(self, delai=120):
        """Prépare le premier tir.

        :param delai: Délai moyen entre deux tirs, en tours de jeu.
        :type delai: int
        """
        self._delai = delai
        self._tours_restants = self._nouveau_delai()

    def tirer(self, ennemi):
        """Tire depuis le bas de l'ennemi quand l'attente est écoulée."""
        if self._tours_restants > 0:
            self._tours_restants -= 1
            return []

        self._tours_restants = self._nouveau_delai()
        x = ennemi.x + ennemi.largeur // 2
        y = ennemi.y + ennemi.hauteur + Projectile.HAUTEUR
        return [Projectile(x, y, direction=1)]

    def _nouveau_delai(self):
        """Tire un délai entre 50 % et 150 % du délai de base."""
        return randint(self._delai // 2, self._delai * 3 // 2)


class Ennemi(Entite):
    """Représente un ennemi de la flotte.

    Composition : l'ennemi possède un ComportementTir qui décide quand il
    tire. Changer de comportement ne demande pas de nouvelle classe.
    """

    LARGEUR = 40
    HAUTEUR = 25
    POINTS = 1   # points gagnés quand on l'élimine

    def __init__(self, x, y, comportement_tir=None, pv=1):
        """Crée un ennemi à sa position de départ.

        :param x: Position du bord gauche en pixels.
        :type x: int
        :param y: Position du bord supérieur en pixels.
        :type y: int
        :param comportement_tir: Règle de tir (par défaut : ne tire pas).
        :type comportement_tir: ComportementTir | None
        :param pv: Points de vie au départ.
        :type pv: int
        """
        super().__init__(x, y)
        self._pv = pv
        self._comportement_tir = comportement_tir or SansTir()

    @property
    def pv(self):
        """Points de vie restants, en lecture seule."""
        return self._pv

    def __repr__(self):
        """Représentation de débogage, par exemple « Boss(x=218, y=60, pv=3) ».

        type(self).__name__ donne le nom de la vraie classe : la même
        méthode affiche « Ennemi », « Tireur » ou « Boss ».
        """
        return f"{type(self).__name__}(x={self.x}, y={self.y}, pv={self._pv})"

    def tirer(self):
        """Délègue la décision de tirer au comportement de tir."""
        return self._comportement_tir.tirer(self)

    def subir_impact(self):
        """Retire un point de vie.

        :return: True si l'ennemi est éliminé.
        :rtype: bool
        """
        self._pv -= 1
        return self._pv <= 0


class Tireur(Ennemi):
    """Ennemi qui tire vers le bas à intervalles aléatoires."""

    def __init__(self, x, y):
        """Crée un tireur avec son propre compteur de tir."""
        super().__init__(x, y, comportement_tir=TirSimple())


class Boss(Ennemi):
    """Ennemi plus grand, à trois points de vie, qui s'énerve quand on le touche."""

    LARGEUR = 64
    HAUTEUR = 35
    POINTS = 5
    DELAI_TIR = 60
    DELAI_TIR_ENERVE = 25

    def __init__(self, x, y):
        """Crée le boss centré sur sa case de la grille.

        :param x: Bord gauche de la case de la grille.
        :type x: int
        :param y: Bord supérieur en pixels.
        :type y: int
        """
        x_centre = x + Ennemi.LARGEUR // 2 - self.LARGEUR // 2
        super().__init__(x_centre, y, comportement_tir=TirSimple(self.DELAI_TIR), pv=3)

    def subir_impact(self):
        """Retire un point de vie, puis fait tirer le boss plus vite s'il survit.

        Redéfinit Ennemi.subir_impact() : la partie appelle la même méthode
        pour tous les ennemis, et le boss y ajoute son propre comportement
        (polymorphisme).

        :return: True si le boss est éliminé.
        :rtype: bool
        """
        elimine = super().subir_impact()
        if not elimine:
            self._comportement_tir = TirSimple(self.DELAI_TIR_ENERVE)
        return elimine
