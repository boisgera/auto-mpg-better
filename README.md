# Auto MPG

Nous présentons un microscopique projet de recherche en "machine learning" 
qui produit un prédicteur de la consommation d'un véhicule en fonction 
de son poids.

Ce projet n'est qu'un prétexte ! Peu importe ici le modèle simpliste utilisé
ou les méthodes mise en oeuvres qui sont très loin de l'état de l'art.
Nous allons nous intéresser au contraire à la gestion de tous les aspects 
"secondaires" du gestion du projet qui sont de nature à maximiser son utilité.

Nous considérerons les étapes suivantes :

 1. 🚀 [Projet original](auto-mpg-v1)

 2. 💦 [Fichiers sources et artefacts](auto-mpg-v2)

 3. 📚 [Documents](auto-mpg-v3)

 4. 🗄️ [Bibliographie et jeu de données](auto-mpg-v4)

 5. 📈 [Modèle et performances](auto-mpg-v5)

## Technologies

**Légende :**

 - 🏛️ : la solution classique, "ennuyeuse" mais éprouvée,

 - 🔥 : une solution plus moderne, voire si elle vous convient !

 - 👀 : sans doute un peu jeune mais prometteur, à garder à l'oeil !



### Systèmes de gestion de version distribués (DVCS) et forges

- 🏛️ [Git](https://git-scm.com/),

- [Mercurial](https://www.mercurial-scm.org/),

- 👀 [Jujutsu](https://www.jj-vcs.dev/latest/).

- 🏛️ [GitHub](https://github.com/),

- 🔥 [HuggingFace](https://huggingface.co/docs/hub/en/repositories),

- [GitLab](https://about.gitlab.com/),

- [Codeberg](https://codeberg.org/).

### Gestionnaires de paquetages

- 🔥 [pixi](https://pixi.sh/)

- 🏛️ [conda](https://anaconda.org/channels/anaconda/packages/conda/overview)

- [mamba](https://mamba.readthedocs.io/en/latest/)

- 🔥 [uv](https://docs.astral.sh/uv/)

- 🏛️ [pip](https://pip.pypa.io/en/stable/)

### Environnements projets

- 🔥 [pixi](https://pixi.sh/)

- 🔥 [uv](https://docs.astral.sh/uv/) (qui met en oeuvre [virtualenv](https://virtualenv.pypa.io/en/latest/))

### Exécuteurs de tâches

- 🔥 [pixi tasks](https://pixi.sh/dev/workspace/advanced_tasks/), intégré à pixi.

- [taskipy](https://github.com/taskipy/taskipy) 
(pour Python, en complément d'uv par exemple !)

- 🏛️ [Make](https://en.wikipedia.org/wiki/Make_(software)), l'original.

- [Task](https://taskfile.dev/), "The modern task runner".

- [Just](https://just.systems/), "Just a command runner".

### Documents

- 🏛️ [LaTeX](https://www.latex-project.org/), 
  "A document preparation system". "Moteurs" de compilation (La)TeX :

    - 🏛️ [pdfTeX](https://en.wikipedia.org/wiki/PdfTeX)

    - [LuaTeX](https://en.wikipedia.org/wiki/LuaTeX)

    - [XeTeX](https://en.wikipedia.org/wiki/XeTeX)

    - 🔥 [Tectonic](https://tectonic-typesetting.github.io/), 
        "a modernized, complete, self-contained TeX/LaTeX engine".

- 👀 [Typst](https://typst.app/), "a new markup-based typesetting system for the sciences." 

- 🏛️ [Markdown](https://en.wikipedia.org/wiki/Markdown), 
  "a lightweight markup language", utilisé dans

  - les notebooks Jupyter et Marimo,

  - les fichiers `README.md` GitHub / GitLab / Forgejo / ...

  - les générateurs de site Web dominés par le contenu,
    [astro](https://astro.build/), 
    [mkdocs](https://squidfunk.github.io/mkdocs-material/), 
    [docusaurus](https://docusaurus.io/),
    [vuepress](https://vuepress.github.io/guide/introduction.html), etc.

- 🔥 [Pandoc](https://pandoc.org/) "a universal document converter",
  permet de convertir du markdown en LaTeX, Typst, HTML, PDF, etc.


### Notebooks

- 🏛️ [Jupyter](https://jupyter.org/),

- 🔥 [Marimo](https://marimo.io/),

- 👀 [Livebook](https://livebook.dev/) + [Pythonx](https://github.com/livebook-dev/pythonx).