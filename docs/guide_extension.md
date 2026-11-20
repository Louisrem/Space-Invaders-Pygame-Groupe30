# Reprendre le jeu

Depuis la racine du projet, lance `python main.py` dans l’environnement Python du jeu.

| Touche | Action |
| --- | --- |
| Entrée | Jouer ou rejouer |
| Flèches gauche et droite | Déplacer le vaisseau |
| Espace | Tirer |
| X | Lancer une mine |
| C | Ouvrir le classement depuis le menu |
| Échap | Revenir du classement au menu |

## Où modifier le jeu

| Ce que tu veux changer | Fichier de départ |
| --- | --- |
| Le contenu d’une vague | [vagues.py](../jeu/vagues.py) |
| Le placement ou le déplacement de la flotte | [flotte.py](../jeu/entites/ennemis/flotte.py) |
| Le tir d’un ennemi | [comportements_tir.py](../jeu/entites/ennemis/comportements_tir.py) |
| Les collisions, la progression ou la recharge de la mine | [partie.py](../jeu/partie.py) |
| Le terrain, les sprites ou le tableau de bord | [rendu.py](../interface/rendu.py) |
| Le menu ou le bilan | [ecrans.py](../interface/ecrans.py) |
| Le classement enregistré | [classement.py](../jeu/classement.py) |
| Les effets sonores | [sons.py](../interface/sons.py) |

[main.py](../main.py) lit le clavier et appelle `Partie.actualiser()` une fois par tour.
`Partie` applique les règles et l’interface lit l’état obtenu pour l’afficher.

## Exemple 1 · Changer la première vague

La vague 1 de [vagues.py](../jeu/vagues.py) contient deux chaînes, une par rangée.
Remplace la deuxième chaîne `"NNNNN"` par `"N.N.N"`. Relance le jeu pour voir
cinq ennemis en haut et trois en dessous.

Le [catalogue des ennemis](../jeu/entites/ennemis/catalogue.py) associe `N` à un
ennemi simple, `T` à un tireur, `R` à un rapide, `P` à un protégé et `B` au boss.
Un point représente une case vide. Les numéros de vagues se suivent.
Garde des rangées de cinq colonnes pour conserver le cadrage des vagues existantes.

## Exemple 2 · Accélérer les tirs d’un type d’ennemi

Dans le [catalogue](../jeu/entites/ennemis/catalogue.py), remplace `TirSimple()`
sur la ligne `"T"` par `TirSimple(delai=60)`. Ajoute un `T` dans la première
vague pour tester rapidement. Le délai est exprimé en tours de jeu et garde
sa part d’aléatoire.

Pour ajouter un nouveau comportement, crée une classe qui implémente
`ComportementTir.tirer(ennemi)` dans
[comportements_tir.py](../jeu/entites/ennemis/comportements_tir.py).
La méthode renvoie une liste de projectiles, éventuellement vide.
Crée une instance du comportement pour chaque ennemi concerné. Si tu ajoutes
une lettre au catalogue, indique le nom du sprite associé. Le chargeur cherche
ce PNG dans [assets/images/ennemis](../assets/images/ennemis/).

## Remplacer ou ajouter un son

Les effets sont des WAV dans [assets/sons/effets](../assets/sons/effets/).
Pour remplacer un son, garde le même nom de fichier. Pour un nouveau son,
déclare un événement dans [evenements_partie.py](../jeu/evenements_partie.py)
et signale-le dans la règle qui le déclenche. La valeur de l'événement
correspond au nom du WAV sans l'extension.

## Vérifier une modification

Exécute `python -m unittest discover -s tests` depuis la racine.
Les tests vérifient les règles sans ouvrir de fenêtre.
Lance ensuite le jeu pour vérifier la vague ou l’écran concerné. Pour un
changement de la fin de partie, vérifie aussi la relance et le classement.
