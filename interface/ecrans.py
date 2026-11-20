"""Dessine le menu, le classement et le bilan de fin de partie."""

from jeu.etat_partie import EtatPartie


def dessiner_message_centre(ecran, police, texte, decalage_y=0):
    """Dessine un texte centré avec un décalage vertical facultatif.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    :param texte: Message à afficher.
    :type texte: str
    :param decalage_y: Décalage vertical en pixels, positif vers le bas.
    :type decalage_y: int
    """
    message = police.render(texte, True, (255, 255, 255))
    centre_x, centre_y = ecran.get_rect().center
    position = message.get_rect(center=(centre_x, centre_y + decalage_y))
    ecran.blit(message, position)


def dessiner_menu(ecran, police):
    """Affiche le menu et ses commandes.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    """
    centre_x, centre_y = ecran.get_rect().center

    titre = police.render("SPACE INVADERS", True, (255, 255, 255))
    ecran.blit(titre, titre.get_rect(center=(centre_x, centre_y - 40)))

    dessiner_message_centre(ecran, police, "Entrée pour jouer")
    dessiner_message_centre(ecran, police, "C pour voir le classement", decalage_y=40)


def dessiner_classement(ecran, police, resultats):
    """Affiche les résultats reçus dans l'ordre fourni.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    :param resultats: Résultats triés à afficher dans le tableau.
    :type resultats: list[dict]
    """
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


def dessiner_fin_partie(ecran, police, partie):
    """Affiche l'issue, les statistiques et la commande pour rejouer.

    :param ecran: Surface sur laquelle dessiner.
    :type ecran: pygame.Surface
    :param police: Police utilisée pour le texte.
    :type police: pygame.font.Font
    :param partie: État de la partie à afficher.
    :type partie: Partie
    """
    titre = "VICTOIRE !" if partie.etat == EtatPartie.VICTOIRE else "PARTIE TERMINÉE"
    dessiner_message_centre(ecran, police, titre)
    dessiner_message_centre(ecran, police, "Entrée pour rejouer", decalage_y=40)
    minutes, secondes = divmod(partie.duree_secondes(), 60)
    texte_temps = f"Temps : {minutes:02d}:{secondes:02d}"
    dessiner_message_centre(ecran, police, texte_temps, decalage_y=80)

    texte_tirs = f"Tirs normaux utilisés : {partie.tirs_normaux}"
    dessiner_message_centre(ecran, police, texte_tirs, decalage_y=110)

    texte_mines = f"Mines utilisées : {partie.mines_lancees}"
    dessiner_message_centre(ecran, police, texte_mines, decalage_y=140)
