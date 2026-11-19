class Projectile:
    def __init__(self,x,y):
        self.x = x
        self.y = y
        self.vitesse = 8

    def avancer(self):
        self.y = self.y - self.vitesse
