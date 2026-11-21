"""Lance le jeu : relie le clavier, la logique (jeu/) et l'affichage (interface/)."""

import pygame

from interface.affichage import charger_images, dessiner_partie
from interface.sons import SonsJeu
from jeu.constantes import HAUTEUR_TERRAIN, LARGEUR_TERRAIN, EtatPartie
from jeu.partie import Partie
from jeu.projectiles import Mine, Projectile

# Touche -> arme. Pour ajouter une arme, crée une sous-classe de
# Projectile et ajoute une ligne ici.
ARMES = {
    pygame.K_SPACE: Projectile,
    pygame.K_x: Mine,
}
VITESSE_JOUEUR = 5


def main():
    """Ouvre la fenêtre et exécute la boucle du jeu."""
    pygame.init()
    ecran = pygame.display.set_mode((LARGEUR_TERRAIN, HAUTEUR_TERRAIN))
    pygame.display.set_caption("Space Invaders - Groupe 30")
    images = charger_images(ecran.get_size())
    sons = SonsJeu()
    police = pygame.font.Font(None, 32)
    horloge = pygame.time.Clock()

    partie = Partie()
    en_cours = True

    while en_cours:
        for evenement in pygame.event.get():
            if evenement.type == pygame.QUIT:
                en_cours = False
            elif evenement.type == pygame.KEYDOWN:
                if evenement.key == pygame.K_RETURN:
                    if partie.etat in (EtatPartie.VICTOIRE, EtatPartie.DEFAITE):
                        partie = Partie()
                    partie.demarrer()
                elif evenement.key in ARMES:
                    partie.tirer(ARMES[evenement.key])

        touches = pygame.key.get_pressed()
        if touches[pygame.K_LEFT]:
            partie.deplacer_joueur(-VITESSE_JOUEUR)
        if touches[pygame.K_RIGHT]:
            partie.deplacer_joueur(VITESSE_JOUEUR)

        partie.actualiser()
        sons.jouer(partie.recuperer_evenements())

        dessiner_partie(ecran, police, partie, images)
        pygame.display.flip()
        horloge.tick(60)

    pygame.quit()


if __name__ == "__main__":
    main()
