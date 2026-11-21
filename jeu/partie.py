"""Règles d'une partie : déplacements, tirs, collisions, vagues et fin."""

from .constantes import HAUTEUR_TERRAIN, LARGEUR_TERRAIN, EtatPartie, EvenementPartie
from .flotte import Flotte
from .vagues import VAGUES
from .vaisseau import Vaisseau


class Partie:
    """Gère une partie et applique ses règles à chaque tour.

    La partie ne connaît pas Pygame : main.py lui transmet les actions
    du joueur, et l'interface lit son état pour l'afficher.
    """

    Y_JOUEUR = HAUTEUR_TERRAIN - 50   # hauteur du vaisseau sur l'écran

    def __init__(self, vagues=VAGUES, etat_initial=EtatPartie.MENU):
        """Prépare le vaisseau et la première vague.

        :param vagues: Formations à jouer, numérotées à partir de 1.
        :type vagues: dict[int, tuple[str, ...]]
        :param etat_initial: État de départ.
        :type etat_initial: EtatPartie
        """
        self._vagues = vagues
        self._niveau = 1
        self._flotte = Flotte(vagues[1])
        self._joueur = Vaisseau(LARGEUR_TERRAIN // 2 - Vaisseau.LARGEUR // 2, self.Y_JOUEUR)
        self._projectiles_joueur = []
        self._projectiles_ennemis = []
        self._etat = etat_initial
        self._score = 0
        self._evenements = []

    # Lecture seule depuis l'extérieur : seules les méthodes de Partie
    # modifient l'état du jeu (encapsulation, cours 04).

    @property
    def score(self):
        """Points gagnés : 1 par ennemi, plus pour le boss."""
        return self._score

    @property
    def etat(self):
        """État actuel de la partie (EtatPartie)."""
        return self._etat

    @property
    def niveau(self):
        """Numéro de la vague en cours."""
        return self._niveau

    @property
    def flotte(self):
        """Flotte de la vague en cours."""
        return self._flotte

    @property
    def joueur(self):
        """Vaisseau du joueur."""
        return self._joueur

    @property
    def projectiles_joueur(self):
        """Copie des tirs du joueur en vol (tuple : non modifiable)."""
        return tuple(self._projectiles_joueur)

    @property
    def projectiles_ennemis(self):
        """Copie des tirs ennemis en vol (tuple : non modifiable)."""
        return tuple(self._projectiles_ennemis)

    def __str__(self):
        """Résumé lisible, par exemple « Vague 2 · score 7 · 3 vies »."""
        return f"Vague {self._niveau} · score {self._score} · {self._joueur.vies} vies"

    def demarrer(self):
        """Passe du menu à la partie en cours."""
        if self._etat == EtatPartie.MENU:
            self._etat = EtatPartie.EN_COURS

    def deplacer_joueur(self, sens):
        """Déplace le vaisseau si la partie est en cours.

        :param sens: -1 vers la gauche, 1 vers la droite.
        :type sens: int
        """
        if self._etat == EtatPartie.EN_COURS:
            self._joueur.deplacer(sens * Vaisseau.VITESSE, LARGEUR_TERRAIN)

    def tirer(self, type_projectile):
        """Lance une arme depuis le vaisseau.

        Chaque arme est limitée à un exemplaire à l'écran. Toute sous-classe
        de Projectile peut être utilisée sans modifier cette méthode.

        :param type_projectile: Classe de l'arme (Projectile, Mine, ...).
        :type type_projectile: type[Projectile]
        """
        if self._etat != EtatPartie.EN_COURS:
            return
        if any(type(p) is type_projectile for p in self._projectiles_joueur):
            return

        x = self._joueur.x + self._joueur.largeur // 2
        self._projectiles_joueur.append(type_projectile(x, self._joueur.y))
        self._evenements.append(type_projectile.EVENEMENT_TIR)

    def actualiser(self):
        """Fait avancer la partie d'un tour."""
        if self._etat != EtatPartie.EN_COURS:
            return

        self._flotte.deplacer(LARGEUR_TERRAIN)
        self._actualiser_projectiles_joueur()
        self._actualiser_projectiles_ennemis()
        self._verifier_fin()

    def recuperer_evenements(self):
        """Renvoie les événements du tour et vide la liste."""
        evenements, self._evenements = self._evenements, []
        return evenements

    def _actualiser_projectiles_joueur(self):
        """Déplace les armes du joueur et applique leurs impacts.

        Chaque arme décide elle-même quels ennemis elle touche
        (polymorphisme de ennemis_touches()).
        """
        for projectile in self._projectiles_joueur[:]:
            projectile.avancer()
            touches = projectile.ennemis_touches(self._flotte)

            if touches:
                self._projectiles_joueur.remove(projectile)
                if projectile.EVENEMENT_IMPACT is not None:
                    self._evenements.append(projectile.EVENEMENT_IMPACT)
                for ennemi in touches:
                    if ennemi.subir_impact():
                        self._flotte.retirer(ennemi)
                        self._score += ennemi.POINTS
            elif projectile.est_sorti():
                self._projectiles_joueur.remove(projectile)

    def _actualiser_projectiles_ennemis(self):
        """Fait tirer les ennemis, déplace leurs tirs et touche le joueur."""
        for ennemi in self._flotte:
            tirs = ennemi.tirer()
            if tirs:
                self._projectiles_ennemis.extend(tirs)
                self._evenements.append(EvenementPartie.TIR_ENNEMI)

        for projectile in self._projectiles_ennemis[:]:
            projectile.avancer()
            if projectile.touche(self._joueur):
                self._projectiles_ennemis.remove(projectile)
                self._joueur.perdre_vie()
                self._evenements.append(EvenementPartie.IMPACT_JOUEUR)
            elif projectile.est_sorti():
                self._projectiles_ennemis.remove(projectile)

    def _verifier_fin(self):
        """Gère la défaite, le passage de vague et la victoire."""
        flotte_en_bas = any(
            e.y + e.hauteur >= self._joueur.y for e in self._flotte
        )
        if self._joueur.vies == 0 or flotte_en_bas:
            self._terminer(EtatPartie.DEFAITE, EvenementPartie.DEFAITE)
        elif len(self._flotte) == 0:
            if self._niveau + 1 in self._vagues:
                self._niveau += 1
                self._flotte = Flotte(self._vagues[self._niveau])
                self._projectiles_joueur.clear()
                self._projectiles_ennemis.clear()
            else:
                self._terminer(EtatPartie.VICTOIRE, EvenementPartie.VICTOIRE)

    def _terminer(self, etat_final, evenement):
        """Applique l'état de fin et signale l'événement correspondant."""
        self._etat = etat_final
        self._evenements.append(evenement)
