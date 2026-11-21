"""Règles d'une partie, de la mise à jour du terrain au résultat final.
"""

from random import randint
from time import monotonic

from .entites.ennemis.flotte import Flotte
from .entites.projectiles import Mine, Projectile, ProjectileBarrage
from .etat_partie import EtatPartie
from .evenements_partie import EvenementPartie
from .vagues import BONUS_PAR_VAGUE, VAGUES


def rectangles_se_chevauchent(zone_a, zone_b):
    """Vérifie si deux rectangles ont une surface commune.

    :param zone_a: Premier rectangle (x, y, largeur, hauteur).
    :type zone_a: tuple[int, int, int, int]
    :param zone_b: Second rectangle au même format.
    :type zone_b: tuple[int, int, int, int]
    :return: True si les rectangles se recouvrent sur les deux axes.
    :rtype: bool
    """
    x_a, y_a, largeur_a, hauteur_a = zone_a
    x_b, y_b, largeur_b, hauteur_b = zone_b

    chevauchement_x = x_a < x_b + largeur_b and x_a + largeur_a > x_b
    chevauchement_y = y_a < y_b + hauteur_b and y_a + hauteur_a > y_b

    return chevauchement_x and chevauchement_y

class Partie:
    """Gère une partie et applique ses règles à chaque tour.

    La boucle principale lui transmet le vaisseau et les dimensions du
    terrain. Le rendu lit ensuite l'état de la partie pour l'afficher.
    """

    def __init__(self, flotte, projectiles, etat_initial=EtatPartie.EN_COURS):
        """Initialise la partie, ses compteurs et ses projectiles.

        :param flotte: Formation de départ.
        :type flotte: Flotte
        :param projectiles: Liste des tirs normaux du joueur, conservée
            par la partie.
        :type projectiles: list[Projectile]
        :param etat_initial: État de départ. Le chrono démarre si la
            partie est en cours.
        :type etat_initial: EtatPartie
        """
        self.flotte = flotte
        self.projectiles = projectiles
        self.score = 0
        self.niveau = 1
        self.projectiles_ennemis = []
        self.etat = etat_initial
        self.tirs_normaux = 0
        self.mines_lancees = 0
        self._evenements = []

        self.debut = None
        self.fin = None
        self.debut_pause = None

        if self.etat in (EtatPartie.EN_COURS, EtatPartie.PAUSE):
            self.debut = monotonic()
        if self.etat == EtatPartie.PAUSE:
            self.debut_pause = self.debut

        self.bonus = None
        self.tours_avant_bonus = None
        self.mine = None
        self.explosion_mine = None
        self.tours_explosion_mine = 0
        self.score_prochaine_mine = 0

    def actualiser(self, joueur, largeur_terrain, hauteur_terrain):
        """Fait avancer d'un tour une partie en cours.

        Déplace la flotte et vérifie si elle atteint la ligne du joueur
        avant de traiter les impacts. Vérifie ensuite la défaite liée
        aux vies, puis met à jour la mine, le bonus et la vague.

        :param joueur: Vaisseau de la partie.
        :type joueur: Vaisseau
        :param largeur_terrain: Largeur du terrain en pixels.
        :type largeur_terrain: int
        :param hauteur_terrain: Hauteur du terrain en pixels.
        :type hauteur_terrain: int
        """
        if self.etat != EtatPartie.EN_COURS:
            return

        self.flotte.deplacer(largeur_terrain)
        self.verifier_defaite(joueur)
        if self.etat == EtatPartie.DEFAITE:
            return

        for projectile in self.projectiles:
            projectile.avancer()

        self.gerer_collisions()
        self.retirer_projectiles_hors_ecran()
        self.actualiser_tirs_ennemis(hauteur_terrain)
        self.gerer_impacts_joueur(joueur)
        self.verifier_defaite(joueur)

        if self.etat == EtatPartie.EN_COURS:
            self.actualiser_mine()
            self.actualiser_bonus(joueur, largeur_terrain, hauteur_terrain)
            self.verifier_fin_vague()

    def recuperer_evenements(self):
        """Renvoie les événements depuis le dernier appel et vide la liste.

        :return: Les événements de la partie dans leur ordre d'apparition.
        :rtype: list[EvenementPartie]
        """
        evenements = self._evenements
        self._evenements = []
        return evenements

    def resultat(self):
        """Prépare les données utilisées pour enregistrer le résultat.

        :return: Score, durée, compteurs de tirs et état de la partie.
        :rtype: dict
        """
        return {
            "score": self.score,
            "duree_secondes": self.duree_secondes(),
            "tirs_normaux": self.tirs_normaux,
            "mines_lancees": self.mines_lancees,
            "issue": self.etat.value,
        }

    def gerer_collisions(self):
        """Applique les impacts des tirs normaux sur la flotte.

        Un tir normal peut toucher un seul ennemi, même s'il est
        protégé.
        """
        for projectile in self.projectiles[:]:
            for ennemi in self.flotte.ennemis:
                if rectangles_se_chevauchent(
                    projectile.zone_collision(), ennemi.zone_collision()
               ):
                    self.projectiles.remove(projectile)

                    self._appliquer_impact(ennemi)
                    break

    def demarrer(self):
        """Passe du menu à la partie en cours et lance le chronomètre.
        """
        if self.etat == EtatPartie.MENU:
            self.debut = monotonic()
            self.etat = EtatPartie.EN_COURS

    def mettre_en_pause(self):
        """Suspend le jeu et fige le chronomètre."""
        if self.etat == EtatPartie.EN_COURS:
            self.debut_pause = monotonic()
            self.etat = EtatPartie.PAUSE

    def reprendre(self):
        """Reprend le jeu en retirant le temps passé en pause du chrono."""
        if self.etat == EtatPartie.PAUSE:
            self.debut += monotonic() - self.debut_pause
            self.debut_pause = None
            self.etat = EtatPartie.EN_COURS

    def _terminer(self, etat_final):
        """Mémorise l'heure de fin et applique l'état de fin demandé."""
        self.fin = monotonic()
        self.etat = etat_final
        evenement = (
            EvenementPartie.VICTOIRE
            if etat_final == EtatPartie.VICTOIRE
            else EvenementPartie.DEFAITE
        )
        self._evenements.append(evenement)

    def duree_secondes(self):
        """Calcule la durée écoulée depuis le début de la partie.

        :return: Durée entière en secondes, figée en pause et à la fin.
        :rtype: int
        """
        if self.debut is None:
            return 0

        if self.fin is not None:
            return int(self.fin - self.debut)
        if self.debut_pause is not None:
            return int(self.debut_pause - self.debut)
        return int(monotonic() - self.debut)

    def _appliquer_impact(self, ennemi):
        """Applique un impact et compte les ennemis éliminés."""
        if ennemi.subir_impact():
            self.flotte.ennemis.remove(ennemi)
            self.score += 1

    def ennemis_avant_mine(self):
        """Compte les éliminations qui manquent pour une mine.

        :return: Le nombre restant, ou zéro si la recharge est prête.
        :rtype: int
        """
        return max(0, self.score_prochaine_mine - self.score)

    def tirer_normal(self, joueur):
        """Tire vers le haut depuis le milieu du vaisseau.

        Le tir est compté seulement si la partie est en cours et si
        aucun tir
        normal du joueur n'est actif.

        :param joueur: Vaisseau qui déclenche le tir.
        :type joueur: Vaisseau
        """
        if self.etat == EtatPartie.EN_COURS and not self.projectiles:
            x = joueur.x + joueur.largeur // 2
            self.projectiles.append(Projectile(x, joueur.y))
            self.tirs_normaux += 1
            self._evenements.append(EvenementPartie.TIR_JOUEUR)

    def tirer_mine(self, joueur, hauteur_ecran):
        """Lance une mine disponible vers le milieu du terrain.

        Il faut une partie en cours, une recharge prête et aucune mine
        posée.
        Un lancement déclenche une nouvelle recharge de cinq
        éliminations.

        :param joueur: Vaisseau depuis lequel la mine est lancée.
        :type joueur: Vaisseau
        :param hauteur_ecran: Hauteur du terrain en pixels.
        :type hauteur_ecran: int
        """
        if (
            self.etat == EtatPartie.EN_COURS
            and self.mine is None
            and self.ennemis_avant_mine() == 0
        ):
            x = joueur.x + joueur.largeur // 2
            self.mine = Mine(x, joueur.y, hauteur_ecran // 2)
            self.mines_lancees += 1
            self._evenements.append(EvenementPartie.MINE_LANCEE)
            self.score_prochaine_mine = self.score + 5

    def actualiser_mine(self):
        """Fait avancer la mine et vérifie son déclenchement.

        Chaque ennemi dans le rayon d'explosion subit un impact. Le
        cercle
        utilisé par le rendu reste affiché pendant douze tours.
        """
        if self.tours_explosion_mine > 0:
            self.tours_explosion_mine -= 1
            if self.tours_explosion_mine == 0:
                self.explosion_mine = None

        mine = self.mine
        if mine is None:
            return

        mine.avancer()
        if not mine.armee:
            return

        if not any(
            mine.dans_rayon(ennemi.zone_collision(), mine.rayon_detection)
            for ennemi in self.flotte.ennemis
        ):
            return

        self.mine = None
        self.explosion_mine = (mine.centre, mine.rayon_explosion)
        self.tours_explosion_mine = 12
        self._evenements.append(EvenementPartie.EXPLOSION_MINE)

        for ennemi in self.flotte.ennemis[:]:
            if mine.dans_rayon(ennemi.zone_collision(), mine.rayon_explosion):
                self._appliquer_impact(ennemi)

    def retirer_projectiles_hors_ecran(self):
        """Supprime les tirs normaux sortis par le haut."""
        for projectile in self.projectiles[:]:
            if projectile.est_sorti_par_le_haut():
                self.projectiles.remove(projectile)

    def verifier_fin_vague(self):
        """Avance d'une vague ou déclare la victoire."""
        if self.flotte.ennemis:
            return

        vague_suivante = self.niveau + 1

        if vague_suivante in VAGUES:
            self.flotte = Flotte(VAGUES[vague_suivante])
            self.niveau = vague_suivante
            self.tours_avant_bonus = None
            if self.niveau in BONUS_PAR_VAGUE:
                self.tours_avant_bonus = randint(120, 300)
        else:
            self._terminer(EtatPartie.VICTOIRE)

    def verifier_defaite(self, joueur):
        """Vérifie les deux conditions de défaite.

        :param joueur: Vaisseau dont les vies et la hauteur servent au
            contrôle.
        :type joueur: Vaisseau
        """
        if joueur.vies == 0:
            self._terminer(EtatPartie.DEFAITE)
            return

        for ennemi in self.flotte.ennemis:
            bas_ennemi = ennemi.y + ennemi.hauteur
            if bas_ennemi >= joueur.y:
                self._terminer(EtatPartie.DEFAITE)
                return

    def actualiser_tirs_ennemis(self, hauteur_ecran):
        """Crée, déplace et retire les projectiles ennemis.

        :param hauteur_ecran: Hauteur du terrain en pixels.
        :type hauteur_ecran: int
        """
        for ennemi in self.flotte.ennemis:
            tirs = ennemi.tirer()
            self.projectiles_ennemis.extend(tirs)
            if any(isinstance(tir, ProjectileBarrage) for tir in tirs):
                self._evenements.append(EvenementPartie.BARRAGE_BOSS)

        for projectile in self.projectiles_ennemis[:]:
            projectile.avancer()

            if projectile.est_sorti_par_le_bas(hauteur_ecran):
                self.projectiles_ennemis.remove(projectile)

    def gerer_impacts_joueur(self, joueur):
        """Applique les impacts des tirs ennemis sur le joueur.

        :param joueur: Vaisseau qui peut subir les impacts.
        :type joueur: Vaisseau
        """
        for projectile in self.projectiles_ennemis[:]:
            if rectangles_se_chevauchent(projectile.zone_collision(), joueur.zone_collision()):
                self.projectiles_ennemis.remove(projectile)
                joueur.subir_impact()
                self._evenements.append(EvenementPartie.IMPACT_JOUEUR)

    def actualiser_bonus(self, joueur, largeur_ecran, hauteur_ecran):
        """Gère l'apparition, la chute et le ramassage du bonus.

        Le bonus apparaît près de l'abscisse du joueur. Il disparaît dès
        qu'il est ramassé ou qu'il sort par le bas.

        :param joueur: Vaisseau qui peut ramasser le bonus.
        :type joueur: Vaisseau
        :param largeur_ecran: Largeur du terrain en pixels.
        :type largeur_ecran: int
        :param hauteur_ecran: Hauteur du terrain en pixels.
        :type hauteur_ecran: int
        """
        if self.tours_avant_bonus is not None:
            self.tours_avant_bonus -= 1

            if self.tours_avant_bonus == 0:
                type_bonus = BONUS_PAR_VAGUE[self.niveau]
                milieu = joueur.x + (joueur.largeur - type_bonus.largeur) // 2
                gauche = max(0, milieu - 160)
                droite = min(largeur_ecran - type_bonus.largeur, milieu + 160)

                self.bonus = type_bonus(randint(gauche, droite), 0)
                self.tours_avant_bonus = None

        if self.bonus is None:
            return

        self.bonus.avancer()

        if rectangles_se_chevauchent(
            self.bonus.zone_collision(), joueur.zone_collision()
        ):
            self.bonus.appliquer(joueur)
            self._evenements.append(EvenementPartie.BONUS_RAMASSE)
            self.bonus = None
        elif self.bonus.est_sorti_par_le_bas(hauteur_ecran):
            self.bonus = None
