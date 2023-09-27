import pyxel, random
# test push3


class Vaisseau:
    def __init__(self, x, y):
        self.vaisseau_x = x
        self.vaisseau_y = y
        self.vies = 5
        # initialisation des tirs
        self.tirs_liste = []

    def vaisseau_deplacement(self):
        """déplacement avec les touches de directions"""

        if pyxel.btn(pyxel.KEY_RIGHT) and self.vaisseau_x < 120:
            self.vaisseau_x += 1
        if pyxel.btn(pyxel.KEY_LEFT) and self.vaisseau_x > 0:
            self.vaisseau_x += -1
        if pyxel.btn(pyxel.KEY_DOWN) and self.vaisseau_y < 120:
            self.vaisseau_y += 1
        if pyxel.btn(pyxel.KEY_UP) and self.vaisseau_y > 0:
            self.vaisseau_y += -1

    def tirs_creation(self):
        """création d'un tir avec la barre d'espace"""

        if pyxel.btnr(pyxel.KEY_SPACE):
            self.tirs_liste.append([self.vaisseau_x + 4, self.vaisseau_y - 4])
            pyxel.play(1, 1)

    def tirs_deplacement(self):
        """déplacement des tirs vers le haut et suppression s'ils sortent du cadre"""

        for tir in self.tirs_liste:
            tir[1] -= 1
            if tir[1] < -8:
                self.tirs_liste.remove(tir)

    def afficher(self):
        #pyxel.rect(self.vaisseau_x, self.vaisseau_y, 8, 8, 1)
        pyxel.blt(self.vaisseau_x, self.vaisseau_y, 0, 0, 0, 8, 8)


class Jeu:
    def __init__(self):

        # taille de la fenetre 128x128 pixels
        # ne pas modifier
        pyxel.init(128, 128, title="Nuit du c0de")

        # position initiale du vaisseau
        # (origine des positions : coin haut gauche)
        self.vaisseau1 = Vaisseau(60, 60)
        self.vaisseau2 = Vaisseau(100, 100)
        self.speed_ennemis = 1
        self.ennemis_liste = []

        # initialisation des explosions
        self.explosions_liste = []

        # chargement des images
        pyxel.load("test.pyxres", True, True, False, False)
        #pyxel.load("son.pyxres", False, False, True, True)

        #pyxel.playm(0, loop=True)

        pyxel.run(self.update, self.draw)

    def ennemis_creation(self):
        """création aléatoire des ennemis"""

        # un ennemi par seconde
        if (pyxel.frame_count % 30 == 0):
            self.ennemis_liste.append([random.randint(0, 120), 0])

    def ennemis_deplacement(self):
        """déplacement des ennemis vers le haut et suppression s'ils sortent du cadre"""

        for ennemi in self.ennemis_liste:
            ennemi[1] += self.speed_ennemis
            if ennemi[1] > 128:
                self.ennemis_liste.remove(ennemi)

    def vaisseau_suppression(self):
        """disparition du vaisseau et d'un ennemi si contact"""

        for ennemi in self.ennemis_liste:
            if ennemi[0] <= self.vaisseau1.vaisseau_x + 8 and ennemi[
                    1] <= self.vaisseau1.vaisseau_y + 8 and ennemi[
                        0] + 8 >= self.vaisseau1.vaisseau_x and ennemi[
                            1] + 8 >= self.vaisseau1.vaisseau_y:
                self.ennemis_liste.remove(ennemi)
                self.explosions_creation(self.vaisseau1.vaisseau_x,
                                         self.vaisseau1.vaisseau_y)
                self.vaisseau1.vies -= 1

    def ennemis_suppression(self):
        """disparition d'un ennemi et d'un tir si contact"""

        for ennemi in self.ennemis_liste:
            for tir in self.vaisseau1.tirs_liste:
                if ennemi[0] <= tir[0] + 1 and ennemi[0] + 8 >= tir[
                        0] and ennemi[1] + 8 >= tir[1]:
                    self.ennemis_liste.remove(ennemi)
                    self.vaisseau1.tirs_liste.remove(tir)

    def explosions_creation(self, x, y):
        """explosions aux points de collision entre deux objets"""
        self.explosions_liste.append([x, y, 0])

    def explosions_animation(self):
        """animation des explosions"""
        for explosion in self.explosions_liste:
            explosion[2] += 1
            if explosion[2] == 12:
                self.explosions_liste.remove(explosion)

    # =====================================================
    # == UPDATE
    # =====================================================
    def update(self):
        """mise à jour des variables (30 fois par seconde)"""

        # deplacement du vaisseau
        self.vaisseau1.vaisseau_deplacement()
        self.vaisseau2.vaisseau_deplacement()

        # creation des tirs en fonction de la position du vaisseau
        self.vaisseau1.tirs_creation()
        self.vaisseau2.tirs_creation()

        # mise a jour des positions des tirs
        self.vaisseau1.tirs_deplacement()
        self.vaisseau2.tirs_deplacement()

        # creation des ennemis
        self.ennemis_creation()

        # mise a jour des positions des ennemis
        self.ennemis_deplacement()

        # suppression des ennemis et tirs si contact
        self.ennemis_suppression()

        # suppression du vaisseau et ennemi si contact
        self.vaisseau_suppression()

        if pyxel.btn(pyxel.KEY_A):
            self.speed_ennemis += 1
            print(self.speed_ennemis)
        if pyxel.btn(pyxel.KEY_Z):
            self.speed_ennemis -= 1
            print(self.speed_ennemis)

        # evolution de l'animation des explosions
        self.explosions_animation()

    # =====================================================
    # == DRAW
    # =====================================================
    def draw(self):
        """création et positionnement des objets (30 fois par seconde)"""

        # vide la fenetre
        pyxel.cls(0)

        # vaisseau (carre 8x8)
        self.vaisseau1.afficher()
        self.vaisseau2.afficher()

        # si le vaisseau possede des vies le jeu continue
        if self.vaisseau1.vies > 0 and self.vaisseau2.vies > 0:
            # tirs
            for tir in self.vaisseau1.tirs_liste:
                pyxel.rect(tir[0], tir[1], 1, 4, 10)
            for tir in self.vaisseau2.tirs_liste:
                pyxel.rect(tir[0], tir[1], 1, 4, 10)

            # ennemis
            for ennemi in self.ennemis_liste:
                #pyxel.rect(ennemi[0], ennemi[1], 8, 8, 8)
                #pyxel.blt(ennemi[0], ennemi[1], 0, 8, 0, 8, 8)
                coef = pyxel.frame_count // 2 % 2
                pyxel.blt(ennemi[0], ennemi[1], 0, 0, 8 + 8 * coef, 8, 8)

            # explosions (cercles de plus en plus grands)
            for explosion in self.explosions_liste:
                pyxel.circb(explosion[0] + 4, explosion[1] + 4,
                            2 * (explosion[2] // 4), 8 + explosion[2] % 3)

            # sinon: GAME OVER
        else:

            pyxel.text(50, 64, 'GAME OVER', 7)


Jeu()
