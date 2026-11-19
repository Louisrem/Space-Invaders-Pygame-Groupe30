import pygame

from jeu.vaisseau import Vaisseau
from jeu.interface_pygame import dessiner_vaisseau, dessiner_flotte, dessiner_projectile, dessiner_score, dessiner_vague
from jeu.flotte import Flotte
from jeu.projectiles import Projectile
from jeu.partie import Partie
from jeu.vagues import VAGUES

def main():
    pygame.display.init()
    ecran = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Space Invaders - Groupe 30")

    joueur = Vaisseau(380,550)
    flotte = Flotte(VAGUES[1])
    horloge = pygame.time.Clock()
    en_cours = True

    projectiles = []
    partie = Partie(flotte, projectiles)

    pygame.font.init()
    police = pygame.font.Font(None, 32)

    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_SPACE and not projectiles:
                x = joueur.x + joueur.largeur // 2
                y = joueur.y
                projectiles.append(Projectile(x,y))
                print(len(projectiles))

        touches = pygame.key.get_pressed()

        if touches[pygame.K_LEFT]:
            joueur.deplacer(-5, ecran.get_width())

        if touches[pygame.K_RIGHT]:
            joueur.deplacer(5,ecran.get_width())

        partie.flotte.deplacer(ecran.get_width())

        for projectile in projectiles:
            projectile.avancer()

        partie.gerer_collisions()
        partie.verifier_fin_vague()
        partie.retirer_projectiles_hors_ecran()
        partie.actualiser_tirs_ennemis(ecran.get_height())

        ecran.fill((0,0,0))
        dessiner_vaisseau(ecran,joueur)
        dessiner_flotte(ecran,partie.flotte)
        for projectile in projectiles:
            dessiner_projectile(ecran, projectile)

        for projectile in partie.projectiles_ennemis:
            dessiner_projectile(ecran,projectile)

        dessiner_score(ecran, police, partie.score)
        dessiner_vague(ecran, police, partie.niveau, len(partie.flotte.ennemis))

        pygame.display.flip()

        horloge.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

