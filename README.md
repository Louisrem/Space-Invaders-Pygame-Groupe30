# Space Invaders (Groupe 30)

Projet de Programmation intermédiaire (HELMo, Bloc 2 IA).
Tu pilotes un vaisseau avec trois vies et tu dois détruire trois vagues
d'ennemis. La dernière vague contient un boss.
C'est une version orientée objet du [Space Invaders de départ](https://github.com/attreyabhatt/Space-Invaders-Pygame).

Ce README est fait pour quelqu'un qui n'a **jamais** utilisé Git ni lancé un
projet Python. Suis les étapes dans l'ordre, sans en sauter.

## Sommaire

1. [Vérifier et installer les outils](#étape-1--vérifier-et-installer-les-outils)
2. [Récupérer le projet](#étape-2--récupérer-le-projet)
3. [Préparer le projet](#étape-3--préparer-le-projet)
4. [Lancer le jeu](#étape-4--lancer-le-jeu)
5. [Comprendre les dossiers](#étape-5--comprendre-les-dossiers)
6. [Modifier le jeu](#étape-6--modifier-le-jeu)
7. [Vérifier que rien n'est cassé](#étape-7--vérifier-que-rien-nest-cassé)
8. [En cas de problème](#étape-8--en-cas-de-problème)

---

## Étape 1 : vérifier et installer les outils

Tu as besoin de deux programmes : **Git** (pour récupérer le projet) et
**Python 3.12** (pour le faire tourner). Ils sont peut-être déjà sur ton
ordinateur. On vérifie d'abord, et on installe seulement ce qui manque.

### 1.1 Ouvrir un terminal

Un terminal est une fenêtre où on tape des commandes au lieu de cliquer.

- **Windows** : touche Windows, tape « PowerShell », Entrée.
- **macOS** : Cmd + Espace, tape « Terminal », Entrée.
- **PyCharm** : onglet **Terminal** en bas de la fenêtre (icône `>_` à gauche).
- **VS Code** : menu *Terminal > New Terminal*.

> 💡 Si tu utilises **PyCharm** ou **VS Code**, tape toutes les commandes de ce
> README dans leur terminal intégré. Une fois le projet ouvert, ce terminal est
> déjà placé dans le bon dossier.

### 1.2 Vérifier ce que tu as déjà

Tape chaque commande puis appuie sur Entrée.

**Git**

| Système | Commande |
| --- | --- |
| Windows, macOS, Linux | `git --version` |

- Tu vois `git version 2.xx.x` : ✅ Git est installé, saute l'étape 1.3.
- Tu vois une erreur (« n'est pas reconnu », « command not found ») : ❌ fais l'étape 1.3.

**Python 3.12**

| Système | Commande |
| --- | --- |
| Windows | `py --list` |
| macOS ou Linux | `python3.12 --version` |

- Windows : la liste contient une ligne avec **3.12** : ✅ saute l'étape 1.4.
- macOS ou Linux : tu vois `Python 3.12.x` : ✅ saute l'étape 1.4.
- Tu vois une erreur, ou seulement d'autres versions (3.11, 3.13, 3.14...) : ❌ fais l'étape 1.4.

> ℹ️ Pourquoi 3.12 et pas la plus récente ? Le jeu utilise pygame 2.6.1, qui ne
> s'installe pas encore avec Python 3.14 sur macOS. Avec 3.12, tout le monde
> a la même version et tout marche.

### 1.3 Installer Git (seulement s'il manque)

**Windows**

- Par le terminal : `winget install --id Git.Git -e`
- Ou par le site : télécharge l'installateur sur <https://git-scm.com/download/win>,
  lance-le et clique sur « Next » à chaque écran. Les choix par défaut conviennent.

**macOS**

Tape `git --version`. macOS propose d'installer les outils pour développeurs.
Clique sur « Installer » et attends la fin.

**Linux (Ubuntu)** : `sudo apt install git`

Ferme et rouvre le terminal, puis refais `git --version`.

### 1.4 Installer Python 3.12 (seulement s'il manque)

Si tu as déjà une autre version (3.13, 3.14...), **garde-la**. Python 3.12
s'installe **à côté**. Les deux versions vivent ensemble sans problème.

**Option A : par le terminal**

- **Windows (PowerShell)** :

  ```powershell
  winget install Python.Python.3.12
  ```

  Réponds `Y` si on te demande d'accepter les conditions.

- **macOS** : il faut Homebrew. Vérifie avec `brew --version`. S'il manque,
  installe-le avec la commande donnée sur <https://brew.sh>. Ensuite :

  ```bash
  brew install python@3.12
  ```

- **Linux (Ubuntu)** :

  ```bash
  sudo apt install python3.12 python3.12-venv
  ```

**Option B : par le site**

1. Va sur <https://www.python.org/downloads/>.
2. Descends jusqu'à « Looking for a specific release ? » et choisis la
   dernière version **3.12.x**.
3. Télécharge l'installateur pour ton système et lance-le.
4. **Sous Windows**, coche la case **« Add python.exe to PATH »** sur le
   premier écran avant de cliquer sur « Install Now ».

Ferme et rouvre le terminal, puis vérifie :

| Système | Commande | Résultat attendu |
| --- | --- | --- |
| Windows | `py -3.12 --version` | `Python 3.12.x` |
| macOS ou Linux | `python3.12 --version` | `Python 3.12.x` |

> ⚠️ Dans tout ce README, écris toujours `py -3.12` (Windows) ou `python3.12`
> (macOS, Linux), **jamais** juste `python`. Sinon ton ordinateur prend
> peut-être une autre version.

---

## Étape 2 : récupérer le projet

« Cloner » veut dire télécharger une copie du projet avec tout son historique.

1. Ouvre un terminal.
2. Va dans le dossier où tu veux ranger le projet, par exemple tes Documents :

   ```bash
   cd Documents
   ```

3. Clone le projet :

   ```bash
   git clone https://github.com/Louisrem/Space-Invaders-Pygame-Groupe30.git
   ```

4. Entre dans le dossier créé :

   ```bash
   cd Space-Invaders-Pygame-Groupe30
   ```

**Vérifier :** la commande `ls` (macOS) ou `dir` (Windows) doit montrer
`main.py`, `jeu`, `interface`, `assets` et `tests`.

**Ou directement dans ton éditeur** (Git doit quand même être installé) :

- **PyCharm** : sur l'écran d'accueil, *Clone Repository* (ou menu *File >
  New > Project from Version Control*). Colle l'adresse
  `https://github.com/Louisrem/Space-Invaders-Pygame-Groupe30.git`, choisis un
  dossier et clique sur *Clone*. Le projet s'ouvre tout seul.
- **VS Code** : sur l'écran d'accueil, *Clone Git Repository* (ou Ctrl + Maj + P,
  tape « Git: Clone »). Colle la même adresse, choisis un dossier, puis clique
  sur *Open* quand VS Code le propose.

---

## Étape 3 : préparer le projet

On crée un **environnement virtuel** (`.venv`). C'est un dossier qui contient
une copie de Python rien que pour ce projet, avec pygame dedans. Ça évite de
mélanger avec les autres projets de ton ordinateur.

Toutes les commandes se tapent **dans le dossier du projet**. Dans PyCharm ou
VS Code, utilise le terminal intégré (il est déjà dans le bon dossier).

**Windows (PowerShell)**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

**macOS ou Linux**

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

**Vérifier :** la dernière ligne doit contenir `Successfully installed pygame-2.6.1`.

Tu ne fais cette étape **qu'une seule fois**.

---

## Étape 4 : lancer le jeu

| Système | Commande |
| --- | --- |
| Windows | `.\.venv\Scripts\python main.py` |
| macOS ou Linux | `.venv/bin/python main.py` |

Une fenêtre s'ouvre avec « SPACE INVADERS ». Appuie sur **Entrée** pour jouer.

### Commandes du jeu

| Touche | Action |
| --- | --- |
| ← / → | Déplacer le vaisseau |
| Espace | Tir normal (un seul à l'écran à la fois) |
| X | Lancer une mine (une seule à la fois) |
| Entrée | Jouer ou rejouer |

La mine monte jusqu'au milieu de l'écran, s'arrête, puis explose quand un
ennemi passe près d'elle. Elle touche tous les ennemis autour.
Tu perds si tu n'as plus de vie ou si la flotte arrive à ton vaisseau.

### Lancer le jeu depuis PyCharm ou VS Code

Il faut d'abord dire à l'éditeur d'utiliser le Python du dossier `.venv`
(celui qui contient pygame). Sinon il souligne `import pygame` en rouge et le
jeu ne démarre pas. À faire une seule fois, après l'étape 3.

**PyCharm**

1. Clique sur le nom de l'interpréteur en bas à droite de la fenêtre (ou menu
   *Settings > Project > Python Interpreter*).
2. *Add Interpreter > Add Local Interpreter*.
3. Choisis *Select existing* (ou *Existing environment*) et indique le fichier :
   - Windows : `.venv\Scripts\python.exe`
   - macOS ou Linux : `.venv/bin/python`
4. Valide avec *OK*. En bas à droite, tu dois voir `Python 3.12 (.venv)`.
5. Clic droit sur `main.py` puis *Run 'main'*. Les fois suivantes, le bouton
   ▶ vert en haut à droite suffit.

**VS Code**

1. Installe l'extension **Python** de Microsoft (icône des carrés à gauche,
   cherche « Python »).
2. Ctrl + Maj + P (Cmd + Maj + P sur macOS), tape « Python: Select
   Interpreter » et choisis la ligne qui contient `.venv`.
3. Ouvre `main.py` et clique sur le bouton ▶ en haut à droite
   (*Run Python File*).

---

## Étape 5 : comprendre les dossiers

```
Space-Invaders-Pygame-Groupe30/
├── main.py              ▶ point de départ : ouvre la fenêtre, lit le clavier, fait tourner la boucle
├── requirements.txt     liste des bibliothèques à installer (pygame)
├── jeu/                 ★ les RÈGLES du jeu. Aucun Pygame ici.
│   ├── constantes.py    taille du terrain (800 x 600), états de la partie, événements
│   ├── entite.py        classe mère Entite : position, taille, collisions
│   ├── vaisseau.py      Vaisseau du joueur (vies, déplacement)
│   ├── ennemis.py       Ennemi, Tireur, Boss + comportements de tir
│   ├── flotte.py        CATALOGUE_ENNEMIS (lettre -> classe) et Flotte
│   ├── vagues.py        dessin des vagues avec des lettres
│   ├── projectiles.py   les armes : Projectile (tir normal), Mine
│   └── partie.py        Partie : chef d'orchestre (tirs, collisions, score, victoire)
├── interface/           ★ tout ce qui se VOIT et s'ENTEND (Pygame)
│   ├── affichage.py     charge les images et dessine l'écran
│   └── sons.py          quel son pour quel événement
├── assets/              images (.png) et sons (.wav)
│   ├── images/ennemis/       une image par type d'ennemi
│   ├── images/projectiles/   une image par type de tir
│   └── sons/effets/          les bruitages
└── tests/               tests automatiques (unittest)
```

**La règle la plus importante :** `jeu/` décide, `interface/` montre.
Un fichier de `jeu/` ne fait jamais `import pygame`.

### Comment un tour de jeu se passe (60 fois par seconde)

1. `main.py` lit le clavier et appelle `partie.tirer(...)` ou `partie.deplacer_joueur(...)`.
2. `main.py` appelle `partie.actualiser()` : la flotte bouge, les tirs avancent, les collisions sont testées.
3. `main.py` donne les événements à `sons.py` qui joue les bruitages.
4. `main.py` appelle `dessiner_partie(...)` qui dessine tout.

---

## Étape 6 : modifier le jeu

Le projet a été pensé pour que tu **ajoutes** des classes au lieu de
**modifier** celles qui existent. Voici les cas les plus courants.

### 6.1 Ajouter un type d'ennemi

Exemple : un ennemi « Robuste » qui résiste à 2 tirs et rapporte 3 points.

**Fichier 1 : `jeu/ennemis.py`**, ajoute à la fin :

```python
class Robuste(Ennemi):
    """Ennemi qui encaisse deux tirs avant d'être éliminé."""

    POINTS = 3

    def __init__(self, x, y):
        """Crée un ennemi robuste avec 2 points de vie."""
        super().__init__(x, y, pv=2)
```

**Fichier 2 : `jeu/flotte.py`**, importe la classe et donne-lui une lettre :

```python
from .ennemis import Boss, Ennemi, Robuste, Tireur

CATALOGUE_ENNEMIS = {
    "N": Ennemi,
    "T": Tireur,
    "B": Boss,
    "R": Robuste,   # nouvelle ligne
}
```

**Fichier 3 : `jeu/vagues.py`**, utilise la lettre dans une vague :

```python
VAGUES = {
    1: ("NNNNN", "NNNNN"),
    2: ("NTNTN", "NRNRN"),   # des Robustes dans la vague 2
    3: ("..B..", "TNTNT", "NNNNN"),
}
```

**Fichier 4 (facultatif) : son image.** Sans rien faire, Robuste prend
l'image de sa classe mère (Ennemi). Pour lui donner la sienne :

1. Mets un PNG de **40 x 25 pixels** dans `assets/images/ennemis/robuste.png`.
2. Dans `interface/affichage.py`, importe `Robuste` et ajoute une ligne dans `IMAGES` :

   ```python
   from jeu.ennemis import Boss, Ennemi, Robuste, Tireur

   IMAGES = {
       Ennemi: "simple",
       Tireur: "tireur",
       Boss: "boss",
       Robuste: "robuste",   # nom du fichier sans .png
       ...
   }
   ```

Tu n'as **pas** besoin de toucher `partie.py` : la partie appelle
`subir_impact()` et lit `POINTS` pour n'importe quel ennemi.

### 6.2 Ajouter une arme

Exemple : un « Tir lourd », plus large et plus lent, qui touche **tous** les
ennemis qu'il traverse au moment de l'impact.

**Fichier 1 : `jeu/projectiles.py`**, ajoute à la fin :

```python
class TirLourd(Projectile):
    """Tir large et lent qui touche tous les ennemis qu'il chevauche."""

    LARGEUR = 14
    HAUTEUR = 20
    VITESSE = 5

    def ennemis_touches(self, ennemis):
        """Renvoie tous les ennemis touchés, pas seulement le premier."""
        return [ennemi for ennemi in ennemis if self.touche(ennemi)]
```

**Fichier 2 : `main.py`**, associe une touche à l'arme :

```python
from jeu.projectiles import Mine, Projectile, TirLourd

ARMES = {
    pygame.K_SPACE: Projectile,
    pygame.K_x: Mine,
    pygame.K_c: TirLourd,   # touche C
}
```

**Fichier 3 (facultatif) : son image**, comme pour un ennemi mais dans
`assets/images/projectiles/` (PNG de 14 x 20 pixels) et une ligne
`TirLourd: "tir_lourd"` dans `IMAGES`.

Ce que tu peux redéfinir dans une arme :

| Attribut ou méthode | Effet |
| --- | --- |
| `LARGEUR`, `HAUTEUR` | taille de la zone de collision |
| `VITESSE` | pixels parcourus par tour |
| `avancer()` | la façon de bouger (la Mine s'arrête au milieu) |
| `ennemis_touches(ennemis)` | quels ennemis sont touchés |
| `EVENEMENT_TIR` | le son joué au lancement |
| `EVENEMENT_IMPACT` | le son joué à l'impact (ou `None`) |

> ℹ️ `Partie.tirer()` n'autorise qu'**un exemplaire de chaque arme** à l'écran.

### 6.3 Changer la façon dont un ennemi tire

Les ennemis délèguent leur tir à un objet `ComportementTir` (composition).
Exemple : un tir double, dans `jeu/ennemis.py` :

```python
class TirDouble(TirSimple):
    """Comme TirSimple, mais lance deux projectiles côte à côte."""

    ECART = 10

    def tirer(self, ennemi):
        """Double chaque tir du comportement de base."""
        tirs = super().tirer(ennemi)
        if tirs:
            tir = tirs[0]
            tirs = [
                Projectile(tir.x - self.ECART, tir.y, direction=1),
                Projectile(tir.x + self.ECART, tir.y, direction=1),
            ]
        return tirs


class Mitrailleur(Ennemi):
    """Ennemi qui tire deux projectiles à la fois."""

    def __init__(self, x, y):
        super().__init__(x, y, comportement_tir=TirDouble(delai=90))
```

Puis ajoute `"M": Mitrailleur` dans le catalogue (comme en 6.1).

### 6.4 Ajouter ou changer une vague

Tout se passe dans `jeu/vagues.py`. Une chaîne = une rangée. Un point = une
case vide. Une lettre = un ennemi du catalogue.

```python
VAGUES = {
    1: ("NNNNN", "NNNNN"),
    2: ("NTNTN", "NNNNN"),
    3: ("..B..", "TNTNT", "NNNNN"),
    4: ("RMRMR", "NRNRN"),   # nouvelle vague, numéro suivant
}
```

Garde des rangées de **7 cases maximum**, sinon la flotte dépasse de l'écran.

### 6.5 Ajouter un son

1. Mets le fichier `.wav` dans `assets/sons/effets/`.
2. Dans `jeu/constantes.py`, ajoute un nom dans `EvenementPartie`, par exemple `TIR_LOURD = auto()`.
3. Dans ta classe, écris `EVENEMENT_TIR = EvenementPartie.TIR_LOURD`.
4. Dans `interface/sons.py`, ajoute `EvenementPartie.TIR_LOURD: "tir_lourd.wav",` dans `SONS`.

### 6.6 Ce qu'il vaut mieux ne pas toucher

| Fichier | Pourquoi |
| --- | --- |
| `jeu/entite.py` | tout hérite d'Entite. Une erreur ici casse le vaisseau, les ennemis et les tirs. |
| `jeu/partie.py` | c'est le cœur des règles. Change-le seulement si ta fonctionnalité invente une **nouvelle règle** (bonus, bouclier, pause...). |
| `LARGEUR_TERRAIN`, `HAUTEUR_TERRAIN` | toutes les positions en dépendent. |
| les noms des PNG existants | `affichage.py` les cherche par leur nom. |
| ajouter `import pygame` dans `jeu/` | la logique doit rester séparée de l'affichage. |

### 6.7 Idées qui demandent de modifier un peu plus

| Idée | Fichiers à modifier |
| --- | --- |
| Bonus qui tombe (vie en plus) | nouvelle classe dans `jeu/`, `partie.py` (liste de bonus + collision avec le joueur), `affichage.py` |
| Bouclier du joueur | `vaisseau.py`, `partie.py` (dans `_actualiser_projectiles_ennemis`) |
| Pause | `constantes.py` (nouvel état), `partie.py`, `main.py`, `affichage.py` |
| Meilleur score sauvegardé | nouveau fichier dans `jeu/`, `main.py`, `affichage.py` |

---

## Étape 7 : vérifier que rien n'est cassé

Lance les tests après **chaque** modification :

| Système | Commande |
| --- | --- |
| Windows | `.\.venv\Scripts\python -m unittest discover -s tests` |
| macOS ou Linux | `.venv/bin/python -m unittest discover -s tests` |

Aujourd'hui, **24 tests** passent. Tu dois voir `OK` à la fin.

Dans **PyCharm**, tu peux aussi faire un clic droit sur le dossier `tests` puis
*Run 'Python tests in tests'*. Dans **VS Code**, le plus simple est de taper la
commande ci-dessus dans le terminal intégré.

Pour tester ton nouvel ennemi, crée par exemple le fichier
`tests/test_extensions.py`. Il sera trouvé tout seul par la commande au-dessus
(son nom commence par `test_`).

```python
"""Tests de nos nouvelles fonctionnalités."""

import unittest

from jeu.ennemis import Robuste


class TestRobuste(unittest.TestCase):
    """Tests de l'ennemi Robuste."""

    def test_robuste_resiste_a_un_tir(self):
        """Il faut deux tirs pour éliminer un Robuste."""
        robuste = Robuste(0, 0)
        self.assertFalse(robuste.subir_impact())
        self.assertTrue(robuste.subir_impact())
```

Puis joue une partie complète pour vérifier à l'œil.

### Mesurer la couverture des tests (facultatif)

`coverage` indique quel pourcentage des lignes de `jeu/` est exécuté par les
tests (environ 98 % aujourd'hui). Il n'est pas nécessaire pour jouer.

```bash
.venv/bin/pip install coverage
.venv/bin/python -m coverage run --source=jeu -m unittest discover -s tests
.venv/bin/python -m coverage report
```

Sous Windows, remplace `.venv/bin/` par `.\.venv\Scripts\`.

---

## Étape 8 : en cas de problème

| Message | Solution |
| --- | --- |
| `git` n'est pas reconnu | Git n'est pas installé, ou ferme et rouvre le terminal. |
| `python3.12: command not found` / `py -3.12` ne marche pas | Python 3.12 n'est pas installé (étape 1.4). |
| `No module named pygame` | Tu as lancé avec un autre Python. Utilise `.venv/bin/python` ou `.\.venv\Scripts\python`. |
| `import pygame` souligné en rouge dans PyCharm ou VS Code | L'éditeur n'utilise pas le Python du `.venv`. Refais « Lancer le jeu depuis PyCharm ou VS Code » (étape 4). |
| `No module named jeu` | Tu as lancé un autre fichier. Lance toujours `main.py`. |
| pip échoue en compilant pygame | Ton `.venv` utilise Python 3.13 ou 3.14. Supprime `.venv` et refais l'étape 3 avec 3.12. |
| Pas de son | Pas grave, le jeu fonctionne sans carte son. |
| `KeyError: Pas d'image pour ...` | Ta classe n'hérite ni d'Ennemi ni de Projectile. |
