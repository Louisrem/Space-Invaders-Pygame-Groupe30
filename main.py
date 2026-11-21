"""Lance le jeu et relie les entrées clavier, la logique et l'affichage.
"""

import pygame

from interface.ecrans import dessiner_classement, dessiner_fin_partie, dessiner_menu
from interface.rendu import dessiner_partie
from interface.ressources import (
    charger_fond,
    charger_sprite_vaisseau,
    charger_sprites_ennemis,
    charger_sprites_projectiles,
)
from interface.sons import SonsJeu
from jeu.classement import enregistrer_resultat, meilleurs_resultats
from jeu.entites.ennemis.flotte import Flotte
from jeu.entites.vaisseau import Vaisseau
from jeu.etat_partie import EtatPartie
from jeu.partie import Partie
from jeu.terrain import HAUTEUR_TERRAIN, LARGEUR_TERRAIN
from jeu.vagues import VAGUES


def creer_partie(etat_initial):
    """Crée le vaisseau et la partie prêts pour la première vague.

    :param etat_initial: État de départ, au menu ou directement en jeu.
    :type etat_initial: EtatPartie
    :return: Le vaisseau et la partie.
    :rtype: tuple[Vaisseau, Partie]
    """
    joueur = Vaisseau(376, 550)
    flotte = Flotte(VAGUES[1])
    partie = Partie(flotte, [], etat_initial=etat_initial)
    return joueur, partie

def main():
    """Ouvre la fenêtre et exécute la boucle du jeu."""
    pygame.display.init()
    ecran = pygame.display.set_mode((LARGEUR_TERRAIN, HAUTEUR_TERRAIN))
    fond = charger_fond(ecran.get_size())
    sons = SonsJeu()
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
            sons.jouer_evenements(partie.recuperer_evenements())

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
