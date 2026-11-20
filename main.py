import pygame

from jeu.vaisseau import Vaisseau
from jeu.interface_pygame import (
    dessiner_avertissement_boss,
    dessiner_bonus,
    dessiner_explosion_mine,
    dessiner_flotte,
    dessiner_message_centre,
    dessiner_mine,
    dessiner_projectile,
    dessiner_score,
    dessiner_vague,
    dessiner_vaisseau,
    dessiner_vies,
    dessiner_etat_mine
)
from jeu.flotte import Flotte
from jeu.projectiles import Projectile
from jeu.partie import Partie
from jeu.vagues import VAGUES
from jeu.etat_partie import EtatPartie

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
            elif (
                evenement.type == pygame.KEYDOWN
                and evenement.key == pygame.K_SPACE
                and not projectiles
                and partie.etat == EtatPartie.EN_COURS
            ):
                x = joueur.x + joueur.largeur // 2
                y = joueur.y
                projectiles.append(Projectile(x,y))
                print(len(projectiles))
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_x:
                partie.tirer_mine(joueur, ecran.get_height())

        if partie.etat == EtatPartie.EN_COURS:
            touches = pygame.key.get_pressed()

            if touches[pygame.K_LEFT]:
                joueur.deplacer(-5, ecran.get_width())

            if touches[pygame.K_RIGHT]:
                joueur.deplacer(5, ecran.get_width())

            partie.flotte.deplacer(ecran.get_width())

            for projectile in projectiles:
                projectile.avancer()

            partie.gerer_collisions()
            partie.retirer_projectiles_hors_ecran()
            partie.actualiser_tirs_ennemis(ecran.get_height())
            partie.gerer_impacts_joueur(joueur)
            partie.verifier_defaite(joueur)

            if partie.etat == EtatPartie.EN_COURS:
                partie.actualiser_mine()
                partie.actualiser_bonus(joueur, ecran.get_width(), ecran.get_height())
                partie.verifier_fin_vague()

        ecran.fill((0,0,0))
        dessiner_avertissement_boss(ecran, partie.flotte)
        dessiner_vaisseau(ecran,joueur)
        dessiner_flotte(ecran,partie.flotte)

        if partie.bonus is not None:
            dessiner_bonus(ecran, partie.bonus)
        if partie.mine is not None:
            dessiner_mine(ecran, partie.mine)
        if partie.explosion_mine is not None:
            dessiner_explosion_mine(ecran, partie.explosion_mine)

        for projectile in projectiles:
            dessiner_projectile(ecran, projectile)

        for projectile in partie.projectiles_ennemis:
            dessiner_projectile(ecran,projectile)

        dessiner_score(ecran, police, partie.score)
        dessiner_vies(ecran, police, joueur.vies)
        dessiner_vague(ecran, police, partie.niveau, len(partie.flotte.ennemis))

        dessiner_etat_mine(
            ecran, police, partie.mine is not None, partie.ennemis_avant_mine()
        )

        if partie.etat == EtatPartie.DEFAITE:
            dessiner_message_centre(ecran, police, "PARTIE TERMINÉE")
        elif partie.etat == EtatPartie.VICTOIRE:
            dessiner_message_centre(ecran, police, "VICTOIRE !")

        pygame.display.flip()

        horloge.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

