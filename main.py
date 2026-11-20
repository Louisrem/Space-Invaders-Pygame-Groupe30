import pygame

from interface.ecrans import dessiner_classement, dessiner_fin_partie, dessiner_menu
from interface.rendu import dessiner_partie
from interface.ressources import (
    charger_fond,
    charger_sprite_vaisseau,
    charger_sprites_ennemis,
    charger_sprites_projectiles,
)
from jeu.classement import enregistrer_resultat, meilleurs_resultats
from jeu.entites.ennemis.flotte import Flotte
from jeu.entites.vaisseau import Vaisseau
from jeu.etat_partie import EtatPartie
from jeu.partie import Partie
from jeu.vagues import VAGUES


def creer_partie(etat_initial):
    joueur = Vaisseau(376, 550)
    flotte = Flotte(VAGUES[1])
    partie = Partie(flotte, [], etat_initial=etat_initial)
    return joueur, partie

def main():
    pygame.display.init()
    ecran = pygame.display.set_mode((800,600))
    fond = charger_fond(ecran.get_size())
    pygame.display.set_caption("Space Invaders - Groupe 30")
    horloge = pygame.time.Clock()
    en_cours = True

    joueur, partie = creer_partie(EtatPartie.MENU)
    sprite_vaisseau = charger_sprite_vaisseau((joueur.largeur, joueur.hauteur))
    sprites_ennemis = charger_sprites_ennemis()
    sprites_projectiles = charger_sprites_projectiles()
    classement_affiche = None

    pygame.font.init()
    police = pygame.font.Font(None, 32)

    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            elif classement_affiche is not None:
                if evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_ESCAPE:
                    classement_affiche = None
            elif (
                partie.etat == EtatPartie.MENU
                and evenement.type == pygame.KEYDOWN
                and evenement.key == pygame.K_c
            ):
                classement_affiche = meilleurs_resultats()
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_RETURN:
                if partie.etat == EtatPartie.MENU:
                    partie.demarrer()
                elif partie.etat in (EtatPartie.VICTOIRE, EtatPartie.DEFAITE):
                    joueur, partie = creer_partie(EtatPartie.EN_COURS)
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_SPACE:
                partie.tirer_normal(joueur)
            elif evenement.type == pygame.KEYDOWN and evenement.key == pygame.K_x:
                partie.tirer_mine(joueur, ecran.get_height())

        ecran.blit(fond, (0, 0))
        if partie.etat == EtatPartie.MENU:
            if classement_affiche is None:
                dessiner_menu(ecran, police)
            else:
                dessiner_classement(ecran, police, classement_affiche)
            pygame.display.flip()
            horloge.tick(60)
            continue

        if partie.etat == EtatPartie.EN_COURS:
            touches = pygame.key.get_pressed()

            if touches[pygame.K_LEFT]:
                joueur.deplacer(-5, ecran.get_width())

            if touches[pygame.K_RIGHT]:
                joueur.deplacer(5, ecran.get_width())

            partie.actualiser(joueur, ecran.get_width(), ecran.get_height())

            if partie.etat in (EtatPartie.VICTOIRE, EtatPartie.DEFAITE):
                enregistrer_resultat(partie.resultat())

        dessiner_partie(
            ecran, police, joueur, partie, sprite_vaisseau, sprites_ennemis, sprites_projectiles
        )
        if partie.etat in (EtatPartie.VICTOIRE, EtatPartie.DEFAITE):
            dessiner_fin_partie(ecran, police, partie)

        pygame.display.flip()

        horloge.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
