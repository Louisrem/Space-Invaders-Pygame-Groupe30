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
    dessiner_etat_mine,
    dessiner_menu,
    dessiner_chrono,
    dessiner_compteurs_tirs,
    dessiner_classement,
)
from jeu.flotte import Flotte
from jeu.ressources import (
    charger_fond,
    charger_sprite_vaisseau,
    charger_sprites_ennemis,
    charger_sprites_projectiles,
)
from jeu.partie import Partie
from jeu.vagues import VAGUES
from jeu.etat_partie import EtatPartie
from jeu.classement import enregistrer_resultat, meilleurs_resultats


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

            partie.flotte.deplacer(ecran.get_width())

            for projectile in partie.projectiles:
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

            if partie.etat in (EtatPartie.VICTOIRE, EtatPartie.DEFAITE):
                enregistrer_resultat({
                    "score": partie.score,
                    "duree_secondes": partie.duree_secondes(),
                    "tirs_normaux": partie.tirs_normaux,
                    "mines_lancees": partie.mines_lancees,
                    "issue": partie.etat.value,
                })

        dessiner_avertissement_boss(ecran, partie.flotte)
        dessiner_vaisseau(ecran, joueur, sprite_vaisseau)
        dessiner_flotte(ecran, partie.flotte, sprites_ennemis)

        if partie.bonus is not None:
            dessiner_bonus(ecran, partie.bonus)
        if partie.mine is not None:
            dessiner_mine(ecran, partie.mine, sprites_projectiles)
        if partie.explosion_mine is not None:
            dessiner_explosion_mine(ecran, partie.explosion_mine)

        for projectile in partie.projectiles:
            dessiner_projectile(ecran, projectile, sprites_projectiles)

        for projectile in partie.projectiles_ennemis:
            dessiner_projectile(ecran, projectile, sprites_projectiles)

        dessiner_score(ecran, police, partie.score)
        dessiner_vies(ecran, police, joueur.vies)
        dessiner_vague(ecran, police, partie.niveau, len(partie.flotte.ennemis))

        if partie.etat == EtatPartie.EN_COURS:
            dessiner_chrono(ecran, police, partie.duree_secondes())
            dessiner_compteurs_tirs(
                ecran, police, partie.tirs_normaux, partie.mines_lancees
            )

        dessiner_etat_mine(
            ecran, police, partie.mine is not None, partie.ennemis_avant_mine()
        )

        if partie.etat == EtatPartie.DEFAITE:
            dessiner_message_centre(ecran, police, "PARTIE TERMINÉE")
        elif partie.etat == EtatPartie.VICTOIRE:
            dessiner_message_centre(ecran, police, "VICTOIRE !")

        if partie.etat in (EtatPartie.VICTOIRE, EtatPartie.DEFAITE):
            dessiner_message_centre(ecran, police, "Entrée pour rejouer", decalage_y=40)
            minutes, secondes = divmod(partie.duree_secondes(), 60)
            texte_temps = f"Temps : {minutes:02d}:{secondes:02d}"
            dessiner_message_centre(ecran, police, texte_temps, decalage_y=80)

            texte_tirs = f"Tirs normaux utilisés : {partie.tirs_normaux}"
            dessiner_message_centre(ecran, police, texte_tirs, decalage_y=110)

            texte_mines = f"Mines utilisées : {partie.mines_lancees}"
            dessiner_message_centre(ecran, police, texte_mines, decalage_y=140)

        pygame.display.flip()

        horloge.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()

