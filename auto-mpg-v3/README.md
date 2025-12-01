# auto-mpg v3

Admettons :

  - qu'on ne soit pas un gros fan de LaTeX comme langage source en raison
    de sa complexité
    ... mais qu'on souhaite tout de même bénéficier des documents de grande 
    qualité que son algorithme de mise en page produit !

  - qu'on souhaiterait produire un article au format HTML en plus de la 
    version PDF.

La syntaxe [Markdown] pour les documents (syntaxe dans laquelle est par exemple
rédigée le fichier [README.md] que vous lisez) et l'outil [Pandoc] sont susceptibles
de nous aider.

Nous pouvons :

  - ajouter Pandoc comme dépendance de notre projet avec `pixi add pandoc`,

  - réécrire notre article [article.tex] en [article.md],

  - réécrire la commande `pdf` en:

    ```
    [tasks.pdf]
    cmd = """pandoc 
    --citeproc 
    --pdf-engine=tectonic 
    --bibliography=references.bib 
    -o article.pdf 
    article.md
    """
    inputs = ["article.md", "references.bib", "images/prediction.png", "images/error.png"]
    outputs = ["article.pdf"]
    depends-on = ["notebook"]
    ```

    Pandoc prendre le soin de générer un fichier intermédiaire LaTeX 
    à partir du fichier Markdown puis d'appeler tectonic.

  - ajouter une nouvelle tâche `html` :

    ```
    [tasks.html]
    cmd = """pandoc 
    --standalone 
    --citeproc 
    --bibliography=references.bib 
    -o article.html 
    article.md
    """
    inputs = ["article.md", "references.bib", "images/prediction.png", "images/error.png"]
    outputs = ["article.html"]
    depends-on = ["notebook"]
    ```

  - éventuellement, créer une tâche `all` dont la fonction est d'exécuter
    toutes les tâches (si nécessaire):

    ```
    [tasks.all]
    depends-on = ["pdf", "html"]
    ```

[Markdown]: https://en.wikipedia.org/wiki/Markdown
[Pandoc]: https://pandoc.org/
[README.md]: https://github.com/boisgera/auto-mpg-better/blob/main/auto-mpg-v3/README.md
[article.tex]: https://github.com/boisgera/auto-mpg-better/blob/main/auto-mpg-v2/article.tex
[article.md]: https://github.com/boisgera/auto-mpg-better/blob/main/auto-mpg-v3/article.tmd
