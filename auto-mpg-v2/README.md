# auto-mpg v2

A cette étape, nous allons :

- [ ] **Sources.** Identifier (ou faire émerger) les fichers sources du projet,
  qui sont strictement nécessaires à la genération de l'ensemble du projet.
  Pour faciliter cette identification, nous allons exclure du projet tout
  fichier qui peut être généré.

- [ ] **Tâches.** Identifier toutes les tâches de production d'artefacts 
  numériques et leur dépendances les unes envers les autres.

- [ ] **Environnement.** Identifier les logiciels nécessaires à la bonne 
  exécution de chaque tâche et produire un environnement automatisant leur installation ainsi que l'exécution des tâches.

## Création d'un projet pixi

[pixi] est un outil de gestions de paquetages logiciels 

  - indépendant du language (il marche très bien avec Python, mais pas seulement !), 
  
  - multi-plateforme (Linux, Windows, Mac),

  - produisant des environnement isolés d'exécution,

  - servant de gestionnaire de tâches.

Ses logiciels sont issus de l'infrastructure [conda-forge].

> [!TIP]
> Pour un projet qui n'aurait besoin que de logiciels Python, nous aurions
> pu également considérer [uv] qui exploite [PyPi] au lieu de conda-forge,
> par exemple avec [taskipy] pour l'exécution des tâches. Malheureusement,
> nous avons besoin de LaTeX ...

[pixi]: https://pixi.sh
[conda-forge]: https://conda-forge.org/
[uv]: https://github.com/astral-sh/uv
[PyPi]: https://pypi.org/
[taskipy]: https://github.com/taskipy/taskipy

Dans notre dossier projet , la commande `pixi init` va créer un fichier
patron de configuration `pixi.toml` que nous pourrons soit éditer manuellement,
soit a travers l'exécution de commandes `pixi`.

Initialement, mon fichier `pixi.toml` est

```toml
[workspace]
authors = ["Sébastien Boisgérault <Sebastien.Boisgerault@gmail.com>"]
channels = ["conda-forge"]
name = "auto-mpg"
platforms = ["linux-64"]
version = "0.1.0"

[tasks]

[dependencies]
```

Je peux immédiatement le modifier pour m'assurer que tous les logiciels que
je vais installer sont supportés sur Linux, Windows et Mac, bien que je
ne travaille que sous Linux.

```toml
platforms = ["linux-64", "win-64", "osx-64", "osx-arm64"]
```


## Notebook Jupyter

En étudiant le notebook, on peut déterminer de quelles bibliothèques Python
(en plus de Python et de JupyterLab) il a besoin : `NumPy`, `Pandas`, 
`Matplotlib` et `Seaborn`.

Nous pouvons donc spécifier ces dépendances avec `pixi`:

```
pixi add python jupyterlab matplotlib numpy pandas seaborn
```

Cela va a la fois installer ces logiciels (dans le répertoire `.pixi`) 
et spécifier un jeu de versions compatibles dans le fichier `pixi.toml` :

```toml
[dependencies]
python = ">=3.13.2,<3.14"
jupyterlab = ">=4.3.5,<5"
matplotlib = ">=3.10.0,<4"
numpy = ">=2.2.3,<3"
pandas = ">=2.2.3,<3"
seaborn = ">=0.13.2,<0.14"
```

A noter que les versions précises de ces logiciels qui seront installées, 
ainsi que de tous les logiciels dont ils dépendent eux-mêmes, seront
enregistrés dans le fichier `pixi.lock`.

On peut alors lire et éditer note notebook Jupyter avec la commande 

```
pixi run jupyter lab
```

qui exécutera JupyterLab dans l'environnement logiciel que nous venons de
définir.

L'examen plus précis du notebook nous permet de réaliser deux choses :

  - Le fichier `noteboook.ipynb` n'est pas ni à 100% un fichier source ni
    à 100% un produit du projet, car il a été enregistré avec les résultats 
    de son exécution. Cela peut être pratique, mais nous allons faire le
    choix un peu radical de ne conserver une version "pure" `notebook-src.ipynb`, 
    sans les résultats de l'exécution (cela se discute ...).

  - Nous pouvons constater qu'en plus de permettre de visualiser des images,
    le notebook stocke ces images sous forme de fichiers et que ces images sont
    utilisées dans l'article !

Nous allons donc automatiser l'exécution du notebook source, pour produire le
notebook résultat, visualisable, ainsi que les images associées. Pour cela,
nous rajoutons au fichier de configuration `pixi.toml`:

```toml
[tasks.exec]
cmd = "jupyter execute --output=notebook.ipynb notebook-src.ipynb"
inputs = ["auto-mpg.csv", "notebook-src.ipynb"]
outputs = ["notebook.ipynb", "images/prediction.png", "images/error.png"]
```

Le notebook complet peut désormais être généré avec la commande :

```
pixi run exec
```

## Compilation de l'article

La même démarche peut désormais être utilisée pour la production de l'article
en PDF. 

  - Les fichiers utilisés pour produire l'article sont : la source 
    LaTeX `article.tex`, la bibliographie BibTeX`references.bib` ainsi
    que les fichier images `images/prediction.png` et `images/error.png`
    produit par l'exécution du notebook.

  - "Les outils de l'écosystème LaTeX" sont nécessaires, ce qui est une très
    mauvaise nouvelles car ces dépendances sont "à l'état des l'art des années
    80" (pour rester poli). Heureusement pour nous, [tectonic] qui modernise
    ces outils va parfaitement nous suffire ici, et il est [disponible sur
    conda-forge pour toutes les plate-formes qui nous intéressent](https://prefix.dev/channels/conda-forge/packages/tectonic). 

[tectonic]: https://tectonic-typesetting.github.io/en-US/

Ajoutons donc `tectonic` à nos dépendances (via `pixi add tectonic`) :


```toml
[dependencies]
tectonic = ">=0.15.0,<0.16"
```

et décrivons la tâche de compilation LaTeX.

```toml
[tasks.build]
cmd = "tectonic article.tex"
inputs = ["article.tex", "references.bib", "images/prediction.png", "images/error.png"]
outputs = ["article.pdf"]
depends-on = ["exec"]
```

A ce stade, la commande `pixi run build` va

  - installer les dépendances logicielles manquantes si nécessaire,

  - exécuter le notebook si nécessaire,

  - compiler l'article LaTeX.
