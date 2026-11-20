class Bouclier:
    def __init__(self):
        self.actif = True

    def absorber_impact(self):
        if self.actif:
            self.actif = False
            return True

        return False
