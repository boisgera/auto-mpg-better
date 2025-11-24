# auto-mpg

## Création d'un projet pixi

pixi, conda-forge (vs uv et pypi).

## On spécifie toutes nos dépendances dans le `pixi.toml`:

```toml
[dependencies]
python = ">=3.13.2,<3.14"
jupyterlab = ">=4.3.5,<5"
matplotlib = ">=3.10.0,<4"
numpy = ">=2.2.3,<3"
pandas = ">=2.2.3,<3"
seaborn = ">=0.13.2,<0.14"
tectonic = ">=0.15.0,<0.16"
watchexec = ">=2.2.0,<3"
```

Evoquer `pixi.lock`.

## Notebook

hybride; distinguer source et produit. Artefact en soit ET génération des images
utilisées par l'article!

tâche : dépendances et sorties sont bien spécifiées

```toml
[tasks.exec]
cmd = "jupyter execute --output=notebook.ipynb notebook-src.ipynb"
inputs = ["auto-mpg.csv", "notebook-src.ipynb"]
outputs = ["notebook.ipynb", "images/prediction.png", "images/error.png"]
```

# LaTeX

La pile latex est une horreur. `tectonic` simplifie cela et est packagée
par conda-forge. Tâche:

```toml
[tasks.build]
cmd = "tectonic article.tex"
inputs = ["article.tex", "references.bib", "images/prediction.png", "images/error.png"]
outputs = ["article.pdf"]
depends-on = ["exec"]
```

