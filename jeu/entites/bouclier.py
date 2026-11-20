"""Protection utilisable par le vaisseau et les ennemis."""

class Bouclier:
    """Absorbe un seul impact avant de se désactiver."""

    def __init__(self):
        """Crée un bouclier actif."""
        self.actif = True

    def absorber_impact(self):
        """Absorbe un impact si le bouclier est encore actif.

        :return: True si l'impact a été absorbé, False sinon.
        :rtype: bool
        """
        if self.actif:
            self.actif = False
            return True

        return False
