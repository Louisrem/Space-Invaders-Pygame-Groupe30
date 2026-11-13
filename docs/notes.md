**Problème 1 :** Incompatibilité entre Python 3.14 et pygame 2.6.1 sur MacOS

**Quand ?** Lors de la création de l'environnement virtuel (`uv venv`) et de l'installation des dépendances (`uv pip install pygame`)
**Pourquoi ?** uv utilise Python 3.14 par défaut, pour lequel pygame 2.6.1 n'a pas encore de version précompilée sur macOS

**--> C'est pour ça qu'on va forcer Python 3.12**

**Problème 2 :** SyntaxWarning lors de l'exécution de `main.py`(`is` au lieu de `==`)

**Quand ?** Lors du lancement du jeu.
**Où ?** main.py, lignes 121 et 177 --> `if bullet_state is "ready":`ou `is "fire":`
**Erreur :** `SyntaxWarning: "is" with 'str' literal. Did you mean "=="?`

**Pourquoi ?**

* `is` = opérateur d'identité qui vérifie si 2 variables pointent vers le même emplacement de mémoire
* `==` compare la valeur du texte.

Python émet un avertissement car `is` sur du texte fonctionne par hasard (si Python réutilise la même case mémoire) mais peut échouer si une nouvelle chaîne identique est créée ailleurs. Après recherche, Python utilise une optimisation interne (*string interning*) : pour les mots courts écrits dans le code (comme "ready"), il ne crée souvent qu'une seule boîte et fait pointer les deux variables dessus. `is` renvoie `True` par pur hasard.

C'est d'ailleurs un défaut de conception si on fait POO. Car le programme ne crée qu'une seule fois les variables pour la position de la balle (`bulletX` et `bulletY`). Il n'y a pas de liste donc on peut ya voir qu'une seule fois les coordonnées X et Y. Lorsqu'on appuie une fois sur espace

```python
if bullet_state is "ready":
    bulletX = playerX
    fire_bullet(bulletX, bulletY)
```

La balle part vers le haut et bullet_state vaut "fire". Mais si on rappuie directement après sur Espace (alors que la première balle est tjrs en route). Comme bullet_state vaut "fire" et pas "ready", la condition est fausse du coup le bloc est ignoré. Si on supprimait le if, la nouvelle balle écraserait l'ancienne. Donc avec ce code, il est impossible d'avoir 2 balles visibles car 1 seul emplacement de mémoire.

DONC ! Si on veut ajouter des ennemis qui tirent, on est bloqué. Il faudrait une liste d'objets "tirs" par exemple. Et si on veut garder la règle "1 tir à la fois", on définira la règle aux entités concernées.

**Solution :**

- **Correction syntaxique :** Toujours utiliser `==` pour comparer des valeurs textuelles et réserver `is` aux comparaisons d'identité (`None`, `True`, `False`).
- **Refonte POO :** Supprimer les variables globales `bullet_state`, `bulletX` et `bulletY`. Créer une classe `Tir` (avec ses propres attributs `x`, `y`, `speed`, `owner`) et stocker les tirs actifs dans une liste (`Tirs = []`). La règle « 1 tir à la fois » devient alors une simple condition propre au joueur (`len(player_tirs) < 1`), ce qui permet aussi d'ajouter des tirs ennemis ou des armes multiples sans modifier la boucle principale.

**Problème 3** : Le jeu continue de tourner après le Game Over

**Quand ?** : Lorsqu'un ennemi touche le bas de l'écran.
Où ? : `main.py` (boucle principale `while running:`)

```python
# Enemy Movement
    for i in range(num_of_enemies):

        # Game Over
        if enemyY[i] > 440:
            for j in range(num_of_enemies):
                enemyY[j] = 2000
            game_over_text()
            break
```

**Pourquoi ?** Il n'y aucune séparation entre les états. (`MENU`,`PLAYING`,`PAUSE`, ...)
Lorsqu'un ennemi franchit la limite basse, tous les ennemis sont téléportés hors de l'écran (`enemyY[j] = 2000`) et d'afficher GAME OVER, mais la boucle continue, on peut toujours déplacer le vaisseau, et on entend toujours le son. Mais impossible de relancer.

**Solution possible** :

Ajouter une variable pour l'état du jeu dans la classe principale du jeu pour indiquer à quel phase le joueur se trouve.
