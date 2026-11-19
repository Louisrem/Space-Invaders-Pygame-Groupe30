import pygame

from jeu.vaisseau import Vaisseau
from jeu.interface_pygame import dessiner_vaisseau, dessiner_flotte
from jeu.flotte import Flotte

def main():
    pygame.display.init()
    ecran = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Space Invaders - Groupe 30")

    joueur = Vaisseau(380,550)
    flotte = Flotte(2,5)
    horloge = pygame.time.Clock()
    en_cours = True

    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False

        touches = pygame.key.get_pressed()

        if touches[pygame.K_LEFT]:
            joueur.deplacer(-5, ecran.get_width())

        if touches[pygame.K_RIGHT]:
            joueur.deplacer(5,ecran.get_width())

        flotte.deplacer(ecran.get_width())

        ecran.fill((0,0,0))
        dessiner_vaisseau(ecran,joueur)
        dessiner_flotte(ecran,flotte)
        pygame.display.flip()

        horloge.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

