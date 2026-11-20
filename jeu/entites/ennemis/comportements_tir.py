"""Règles qui décident quand et combien de projectiles un ennemi lance.
"""

from abc import ABC, abstractmethod
from ..projectiles import Projectile, ProjectileBarrage
from random import randint

class ComportementTir(ABC):
    """Définit les règles communes aux comportements de tir des ennemis.

    Pour créer un nouveau comportement, hérite de cette classe et
    implémente la méthode tirer(). Tu peux ensuite l'associer à un
    ennemi dans le catalogue.
    """
    @abstractmethod
    def tirer(self, ennemi):
        """Renvoie les projectiles que l'ennemi lance à ce tour.

        :param ennemi: Ennemi qui utilise ce comportement de tir.
        :type ennemi: Ennemi
        :return: Les projectiles à lancer, ou une liste vide si aucun tir ne part.
        :rtype: list[Projectile]
        """
        pass

class SansTir(ComportementTir):
    """Équipe un ennemi qui ne tire jamais.

    Ennemi utilise ce comportement par défaut si aucun tir n'est configuré.
    """
    def tirer(self, ennemi):
        """Renvoie une liste vide à chaque tour.

        :param ennemi: Ennemi équipé de ce comportement.
        :type ennemi: Ennemi
        :return: Une liste vide, car aucun projectile ne part.
        :rtype: list[Projectile]
        """
        return []

# Suffit de changer le délai pour tirer plus vite (dans catalogue.py)
class TirSimple(ComportementTir):
    """Fait tirer un ennemi vers le bas à intervalles aléatoires.

    Donne une instance de TirSimple à chaque ennemi tireur pour que
    chacun ait son propre compteur. Par exemple, dans le catalogue :

    * Ennemi(x, y, comportement_tir=TirSimple(delai=60))
    """
    def __init__(self, delai=120):
        """Prépare le premier tir avec un délai aléatoire.

        :param delai: Délai de référence en tours de jeu. Vaut 120 par défaut.
        :type delai: int
        """
        self.delai = delai
        self.tours_restants = self._nouveau_delai()

    def tirer(self, ennemi):
        """Fait tirer l'ennemi quand son temps d'attente est écoulé

        Le jeu appelle cette méthode à chaque tour. S'il reste des tours
        à attendre, le compteur baisse de 1. Quand il est à zéro, un tir
        part du milieu de l'ennemi, vers le bas. Le compteur repart alors
        avec un nouveau délai choisi au hasard.

        :param ennemi: L'ennemi qui doit tirer.
        :type ennemi: Ennemi
        :return: [] pendant l'attente, ou [projectile] si un tir part.
        :rtype: list[Projectile]
        """
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
        """Tire un délai entre 50 % et 150 % du délai de base."""
        return randint(self.delai // 2, self.delai * 3 // 2)

class TirDeBarrage(ComportementTir):
    """Annonce trois colonnes, puis lance un projectile dans chacune.

    Les colonnes sont choisies selon la position de l'ennemi au moment
    de l'annonce. Elles restent fixes même si l'ennemi se déplace.
    """

    def __init__(self):
        """Attend 120 tours avant la première annonce."""
        self.tours_restants = 120
        self.colonnes_annoncees = []

    def tirer(self, ennemi):
        """Fait avancer le barrage d'un tour.

        À la fin de l'attente, annonce les trois colonnes. Après 60 tours
        d'avertissement, lance les trois tirs et attend 120 tours avant
        la prochaine annonce.

        :param ennemi: Ennemi dont la position sert à placer les colonnes.
        :type ennemi: Ennemi
        :return: [] pendant l'attente ou l'annonce, puis les trois tirs.
        :rtype: list[ProjectileBarrage]
        """
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
