import pyxel
from math import ceil

class PoliceBitmap:
    """Convertit un fichier TTF en glyphes utilisables avec Pyxel."""

    CARACTERES_PAR_DEFAUT = "".join(chr(code) for code in range(32, 127)) + (
        "éèêëàâùûôîïçÉÈÊËÀÂÙÛÔÎÏÇ"
    )

    def __init__(self,
        position_x: int,
        position_y: int,
        texte: str,
        couleur: int = 7,
        echelle: int = 1,
        chemin_police: str = "VCR_OSD_MONO.ttf",
        taille: int = 16,
        caracteres: str = CARACTERES_PAR_DEFAUT,
        colonnes: int = 16,
        ) -> None:

        self.position_x = position_x
        self.position_y = position_y
        self.texte = texte
        self.couleur = couleur
        self.echelle = echelle
        
        if taille <= 0:
            raise ValueError("La taille de la police doit être positive.")
        if colonnes <= 0:
            raise ValueError("Le nombre de colonnes doit être positif.")
        if not caracteres:
            raise ValueError("La liste des caractères ne peut pas être vide.")

        try:
            from PIL import Image, ImageDraw, ImageFont
        except ImportError as erreur:
            raise RuntimeError(
                "PoliceBitmap nécessite Pillow. Installez-le avec "
                "'python -m pip install Pillow'."
            ) from erreur

        caracteres = "".join(dict.fromkeys(caracteres))
        police = ImageFont.truetype(chemin_police, taille)
        ascension, descente = police.getmetrics()
        mesures = {}
        largeur_case = 1
        hauteur_case = ascension + descente

        for caractere in caracteres:
            boite = police.getbbox(caractere, anchor="ls")
            largeur = max(0, boite[2] - boite[0])
            avance = max(1, ceil(police.getlength(caractere)))
            mesures[caractere] = (boite, avance)
            largeur_case = max(largeur_case, largeur, avance)

        lignes = ceil(len(caracteres) / colonnes)
        largeur_atlas = colonnes * largeur_case
        hauteur_atlas = lignes * hauteur_case
        if largeur_atlas > 256 or hauteur_atlas > 256:
            raise ValueError(
                "L'atlas dépasse la taille maximale de 256 x 256 pixels. "
                "Réduisez la taille de la police ou le nombre de caractères."
            )

        atlas_pil = Image.new("L", (largeur_atlas, hauteur_atlas), 0)
        dessin = ImageDraw.Draw(atlas_pil)
        self.glyphes: dict[str, tuple[int, int, int, int, int]] = {}

        for index, caractere in enumerate(caracteres):
            colonne = index % colonnes
            ligne = index // colonnes
            x = colonne * largeur_case
            y = ligne * hauteur_case
            boite, avance = mesures[caractere]
            dessin.text(
                (x - boite[0], y + ascension),
                caractere,
                font=police,
                fill=255,
                anchor="ls",
            )
            self.glyphes[caractere] = (x, y, largeur_case, hauteur_case, avance)

        self.image = pyxel.Image(largeur_atlas, hauteur_atlas)
        pixels = atlas_pil.load()
        for y in range(hauteur_atlas):
            for x in range(largeur_atlas):
                if pixels[x, y] >= 128:
                    self.image.pset(x, y, 7)

        self.hauteur_ligne = hauteur_case

    def recuperer_element(self, caractere: str) -> tuple[int, int, int, int, int]:
        """Retourne u, v, largeur, hauteur et avance du caractère dans l'atlas."""
        if len(caractere) != 1:
            raise ValueError("Il faut fournir exactement un caractère.")
        try:
            return self.glyphes[caractere]
        except KeyError as erreur:
            raise ValueError(
                f"Le caractère {caractere!r} n'est pas présent dans cette police."
            ) from erreur

    def affichage(self) -> None:
        if not 0 <= self.couleur <= 15:
            raise ValueError("La couleur Pyxel doit être comprise entre 0 et 15.")
        if self.echelle <= 0:
            raise ValueError("L'échelle doit être positive.")

        position_x = self.position_x
        position_y = self.position_y
        pyxel.pal(7, self.couleur)
        try:
            for caractere in self.texte:
                if caractere == "\n":
                    position_x = self.position_x
                    position_y += self.hauteur_ligne * self.echelle
                    continue

                u, v, largeur, hauteur, avance = self.recuperer_element(caractere)
                if largeur and hauteur:
                    pyxel.blt(
                        position_x,
                        position_y,
                        self.image,
                        u,
                        v,
                        largeur,
                        hauteur,
                        colkey=0,
                        scale=self.echelle,
                    )
                position_x += avance * self.echelle
        finally:
            pyxel.pal()
