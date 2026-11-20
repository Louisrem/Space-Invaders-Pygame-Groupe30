from pathlib import Path

import pygame
from jeu.ennemis.boss import Boss
from jeu.bonus import BonusBouclier, Coeur

def charger_sprite_vaisseau(taille):
    chemin = Path(__file__).resolve().parent.parent / "assets" / "images" / "vaisseau.png"
    sprite = pygame.image.load(chemin).convert_alpha()
    return pygame.transform.scale(sprite, taille)


def dessiner_vaisseau(ecran, vaisseau, sprite):
    rectangle = pygame.Rect(vaisseau.zone_collision())
    ecran.blit(sprite, rectangle.topleft)
    if vaisseau.bouclier is not None and vaisseau.bouclier.actif:
        pygame.draw.rect(ecran, (80, 190, 255), rectangle, 2)

def dessiner_flotte(ecran, flotte):
    for ennemi in flotte.ennemis:
        rectangle = pygame.Rect(
            ennemi.x, ennemi.y, ennemi.largeur, ennemi.hauteur
        )
        couleur = (180, 105, 255) if isinstance(ennemi, Boss) else (240, 100, 100)
        pygame.draw.rect(ecran, couleur, rectangle)
        if ennemi.bouclier is not None and ennemi.bouclier.actif:
            pygame.draw.rect(ecran, (80,190,255), rectangle, 2)

def dessiner_avertissement_boss(ecran, flotte):
    bas = ecran.get_height() - 1

    for ennemi in flotte.ennemis:
        if isinstance(ennemi, Boss):
            for x in ennemi.colonnes_barrage():
                pygame.draw.line(ecran, (255, 145, 70), (x, 0), (x, bas), 2)

def dessiner_projectile(ecran, projectile):
    rectangle = pygame.Rect(projectile.zone_collision())
    pygame.draw.rect(ecran, (255,255,255), rectangle)

def dessiner_score(ecran, police, score):
    texte = police.render(f"Score : {score}", True, (255,255,255))
    ecran.blit(texte, (15,15 ))

def dessiner_vies(ecran, police, vies):
    texte = police.render(f"VIES : {vies}", True, (255, 255, 255))
    ecran.blit(texte, (15,37))

def dessiner_vague(ecran, police, niveau, ennemis_restants):
    blanc = (255, 255, 255)
    largeur = ecran.get_width()

    vague = police.render(f"VAGUE {niveau}", True, blanc)
    ennemis = police.render(f"ENNEMIS RESTANTS : {ennemis_restants}", True, blanc)

    ecran.blit(vague, vague.get_rect(midtop=(largeur // 2, 15)))
    ecran.blit(ennemis, ennemis.get_rect(topright=(largeur - 15, 15)))

def dessiner_message_centre(ecran, police, texte, decalage_y=0):
    message = police.render(texte, True, (255, 255, 255))
    centre_x, centre_y = ecran.get_rect().center
    position = message.get_rect(center=(centre_x, centre_y + decalage_y))
    ecran.blit(message, position)

def dessiner_coeur(ecran, coeur):
    x, y = coeur.x, coeur.y
    rose = (255, 90, 130)
    pygame.draw.circle(ecran, rose, (x + 6, y + 6), 6)
    pygame.draw.circle(ecran, rose, (x + 18, y + 6), 6)
    pygame.draw.polygon(
        ecran, rose, [(x, y + 7), (x + 23, y + 7), (x + 12, y + 23)]
    )

def dessiner_bonus(ecran, bonus):
    if isinstance(bonus, Coeur):
        dessiner_coeur(ecran, bonus)
    elif isinstance(bonus, BonusBouclier):
        rectangle = pygame.Rect(bonus.zone_collision())
        pygame.draw.rect(ecran, (80, 190, 255), rectangle, 3)


def dessiner_mine(ecran, mine):
    couleur = (255, 205, 85) if mine.armee else (206, 160, 65)
    if mine.armee:
        pygame.draw.circle(ecran, couleur, mine.centre, mine.rayon_detection, 1)
    pygame.draw.circle(ecran, couleur, mine.centre, mine.largeur // 2)


def dessiner_explosion_mine(ecran, explosion):
    centre, rayon = explosion
    pygame.draw.circle(ecran, (255, 145, 70), centre, rayon, 3)

def dessiner_etat_mine(ecran, police, mine_active, ennemis_restants):
    if mine_active:
        texte = "MINE POSÉE"
    elif ennemis_restants == 0:
        texte = "MINE PRÊTE [X]"
    else:
        texte = f"MINE : ENCORE {ennemis_restants} À ÉLIMINER"

    image = police.render(texte, True, (255, 205, 85))
    position = image.get_rect(midtop=(ecran.get_width() // 2, 37))
    ecran.blit(image, position)

def dessiner_menu(ecran, police):
    ecran.fill((0, 0, 0))
    centre_x, centre_y = ecran.get_rect().center

    titre = police.render("SPACE INVADERS", True, (255, 255, 255))
    ecran.blit(titre, titre.get_rect(center=(centre_x, centre_y - 40)))

    dessiner_message_centre(ecran, police, "Entrée pour jouer")
    dessiner_message_centre(ecran, police, "C pour voir le classement", decalage_y=40)


def dessiner_classement(ecran, police, resultats):
    ecran.fill((0, 0, 0))
    dessiner_message_centre(ecran, police, "MEILLEURS SCORES", decalage_y=-210)
    dessiner_message_centre(ecran, police, "Échap pour revenir au menu", decalage_y=140)

    if not resultats:
        dessiner_message_centre(ecran, police, "Aucune partie terminée")
        return

    colonnes = (70, 180, 300, 420, 540, 690)
    lignes = [("Rang", "Score", "Temps", "Tirs", "Mines", "Résultat")]
    for rang, resultat in enumerate(resultats, start=1):
        minutes, secondes = divmod(resultat["duree_secondes"], 60)
        lignes.append((
            str(rang),
            str(resultat["score"]),
            f"{minutes:02d}:{secondes:02d}",
            str(resultat["tirs_normaux"]),
            str(resultat["mines_lancees"]),
            "Victoire" if resultat["issue"] == "victoire" else "Défaite",
        ))

    for indice, ligne in enumerate(lignes):
        couleur = (255, 205, 85) if indice == 0 else (255, 255, 255)
        for x, valeur in zip(colonnes, ligne):
            texte = police.render(valeur, True, couleur)
            ecran.blit(texte, texte.get_rect(center=(x, 140 + indice * 44)))


def dessiner_chrono(ecran, police, duree_secondes):
    minutes, secondes = divmod(duree_secondes, 60)
    texte = police.render(f"Temps : {minutes:02d}:{secondes:02d}", True, (255, 255, 255))
    position = texte.get_rect(topright=(ecran.get_width() - 15, 37))
    ecran.blit(texte, position)


def dessiner_compteurs_tirs(ecran, police, tirs_normaux, mines_lancees):
    lignes = (f"Tirs utilisés : {tirs_normaux}", f"Mines utilisées : {mines_lancees}")
    droite = ecran.get_width() - 15

    for ligne, haut in zip(lignes, (59, 81)):
        texte = police.render(ligne, True, (255, 255, 255))
        ecran.blit(texte, texte.get_rect(topright=(droite, haut)))
