# Space Invaders · Groupe 30

Un jeu d’arcade en Python et Pygame. Pilote le Delta, termine les cinq vagues
et bats ton meilleur score.

## Installer et lancer le jeu

### 1. Récupérer le projet

Dans un terminal, lance ces commandes si tu as Git.

```bash
git clone https://github.com/Louisrem/Space-Invaders-Pygame-Groupe30.git
cd Space-Invaders-Pygame-Groupe30
```

Tu peux aussi télécharger le projet depuis **Code → Download ZIP** sur GitHub.
Décompresse le ZIP, puis ouvre un terminal dans le dossier qui contient
`main.py` et `requirements.txt`.

### 2. Préparer Python et Pygame

Installe [uv](https://docs.astral.sh/uv/getting-started/installation/) si besoin,
puis rouvre ton terminal. Depuis le dossier du projet, lance ces deux commandes.

```bash
uv venv --python 3.12
uv pip install --python .venv -r requirements.txt
```

`.venv` est l’environnement Python du jeu. Il contient Python 3.12 et la
version de Pygame indiquée dans `requirements.txt`.

### 3. Lancer le jeu

**macOS ou Linux**

```bash
.venv/bin/python main.py
```

**Windows · PowerShell**

```powershell
.\.venv\Scripts\python.exe main.py
```

Une fenêtre s’ouvre. Appuie sur **Entrée** pour commencer.
Si PyCharm affiche `No module named pygame`, utilise la commande de lancement
ci-dessus ou sélectionne le Python du dossier `.venv` comme interpréteur.

## Jouer

| Touche | Action |
| --- | --- |
| Entrée | Commencer ou rejouer après une victoire ou une défaite |
| ← et → | Déplacer le Delta |
| Espace | Tirer. Un seul tir normal peut être à l’écran à la fois |
| X | Lancer une mine quand le tableau de bord indique qu’elle est prête |
| C | Consulter le classement depuis le menu |
| Échap | Revenir au menu depuis le classement |

La mine s’arrête à mi-écran et explose quand un ennemi passe à proximité.
Après le lancement, élimine cinq ennemis pour la recharger.
Un cœur donne une vie et un bouclier absorbe un impact. La partie est perdue
si tu n’as plus de vies ou si la flotte atteint la ligne du vaisseau.
En vague 5, les lignes orange annoncent les colonnes du barrage du boss.

Le bilan affiche le score, le temps et le nombre de tirs et de mines utilisés.
Les résultats sont conservés sur ta machine dans `classement.json`.

## Reprendre le code

Commence par le [guide de reprise](docs/guide_extension.md). Il explique
comment modifier une vague, ajouter un comportement de tir et changer un son.

| Tu veux modifier… | Ouvre… |
| --- | --- |
| Les rangées d’une vague ou le bonus associé | [jeu/vagues.py](jeu/vagues.py) |
| Les types d’ennemis disponibles | [Le catalogue](jeu/entites/ennemis/catalogue.py) |
| La façon dont les ennemis tirent | [Les comportements de tir](jeu/entites/ennemis/comportements_tir.py) |
| Les collisions, le score ou la recharge de la mine | [jeu/partie.py](jeu/partie.py) |
| Le menu, les sprites ou les effets sonores | [interface/](interface/) et [assets/](assets/) |

Le [programme de départ](archive/) et les [notes d’analyse](docs/notes.md)
permettent de retrouver le point de départ du projet.

### Lancer les tests

Depuis le dossier du projet, exécute la commande de ton système. Les tests
vérifient les règles du jeu sans ouvrir de fenêtre.

**macOS ou Linux**

```bash
.venv/bin/python -m unittest discover -s tests
```

**Windows · PowerShell**

```powershell
.\.venv\Scripts\python.exe -m unittest discover -s tests
```
