import pygame

from jeu.vaisseau import Vaisseau
from jeu.interface_pygame import dessiner_vaisseau, dessiner_flotte, dessiner_projectile
from jeu.flotte import Flotte
from jeu.projectiles import Projectile
from jeu.partie import Partie

def main():
    pygame.display.init()
    ecran = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Space Invaders - Groupe 30")

    joueur = Vaisseau(380,550)
    flotte = Flotte(2,5)
    horloge = pygame.time.Clock()
    en_cours = True

    projectiles = []
    partie = Partie(flotte, projectiles)

    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_SPACE:
                x = joueur.x + joueur.largeur // 2
                y = joueur.y
                projectiles.append(Projectile(x,y))
                print(len(projectiles))

        touches = pygame.key.get_pressed()

        if touches[pygame.K_LEFT]:
            joueur.deplacer(-5, ecran.get_width())

        if touches[pygame.K_RIGHT]:
            joueur.deplacer(5,ecran.get_width())

        flotte.deplacer(ecran.get_width())

        for projectile in projectiles:
            projectile.avancer()

        partie.gerer_collisions()

        ecran.fill((0,0,0))
        dessiner_vaisseau(ecran,joueur)
        dessiner_flotte(ecran,flotte)
        for projectile in projectiles:
            dessiner_projectile(ecran, projectile)
        pygame.display.flip()

        horloge.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

