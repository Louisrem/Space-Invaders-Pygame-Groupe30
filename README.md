# Space Invaders · Groupe 30

Projet de Programmation intermédiaire (HELMo, B2 IA). Version orientée objet
du [Space Invaders de départ](https://github.com/attreyabhatt/Space-Invaders-Pygame),
conservé dans [archive/](archive/).

Tu pilotes un vaisseau avec trois vies et tu dois détruire trois vagues
d'ennemis. La dernière vague contient un boss qui résiste à trois tirs et
rapporte 5 points (1 point pour les autres ennemis).

## Installation

Il faut **Python 3.12** (pygame 2.6.1 n'a pas encore de version prête pour
Python 3.14 sur macOS). Ouvre un terminal dans le dossier du projet.

**macOS ou Linux**

```bash
python3.12 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

**Windows (PowerShell)**

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\pip install -r requirements.txt
```

## Lancer le jeu

| Système | Commande |
| --- | --- |
| macOS ou Linux | `.venv/bin/python main.py` |
| Windows | `.\.venv\Scripts\python main.py` |

## Commandes

| Touche | Action |
| --- | --- |
| ← / → | Déplacer le vaisseau |
| Espace | Tir normal (un seul à la fois) |
| X | Lancer une mine (une seule à la fois) |
| Entrée | Jouer ou rejouer |

La mine monte jusqu'au milieu de l'écran, s'arrête, puis explose quand un
ennemi s'approche. Elle touche tous les ennemis dans son rayon.
La partie est perdue si tu n'as plus de vie ou si la flotte atteint ton
vaisseau.

## Organisation du code

```
main.py              boucle du jeu : lit le clavier, actualise, dessine
jeu/                 règles du jeu, sans Pygame
  constantes.py      taille du terrain, états et événements de la partie
  entite.py          classe mère Entite (position, taille, collisions)
  vagues.py          grilles des vagues d'ennemis
  partie.py          Partie : tirs, collisions, vagues, victoire/défaite
  vaisseau.py        Vaisseau du joueur
  projectiles.py     armes : Projectile, Mine
  ennemis.py         Ennemi, Tireur, Boss et comportements de tir
  flotte.py          catalogue des lettres et Flotte
interface/           tout ce qui utilise Pygame
  affichage.py       chargement des images et dessin
  sons.py            effets sonores (quel son pour quel événement)
tests/               tests unitaires de la logique
```

Pour ajouter :

- **un ennemi** : sa classe dans [ennemis.py](jeu/ennemis.py), une lettre dans
  `CATALOGUE_ENNEMIS` de [flotte.py](jeu/flotte.py), puis la lettre dans
  [vagues.py](jeu/vagues.py) ;
- **une arme** : une sous-classe de `Projectile` dans [projectiles.py](jeu/projectiles.py),
  puis une touche dans `ARMES` de [main.py](main.py) ;
- **un comportement de tir** : une sous-classe de `ComportementTir` dans
  [ennemis.py](jeu/ennemis.py).

Sans rien d'autre, une nouvelle classe prend l'image de sa classe mère. Pour
lui donner sa propre image, mets le PNG dans `assets/images/` et ajoute une
ligne dans `FICHIERS_IMAGES` et `IMAGES` de [affichage.py](interface/affichage.py).

## Tests

```bash
.venv/bin/python -m unittest discover -s tests
```

Sous Windows : `.\.venv\Scripts\python -m unittest discover -s tests`.

### Mesurer la couverture des tests

`coverage` indique quel pourcentage des lignes de `jeu/` est exécuté par les
tests (environ 96 % aujourd'hui). Il n'est pas nécessaire pour jouer.

```bash
.venv/bin/pip install coverage
.venv/bin/python -m coverage run --source=jeu -m unittest discover -s tests
.venv/bin/python -m coverage report
```

Sous Windows, remplace `.venv/bin/` par `.\.venv\Scripts\`.
