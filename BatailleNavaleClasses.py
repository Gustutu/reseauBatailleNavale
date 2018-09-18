
import pygame

# utilisation de set pour list de bateau par client


class Bateau:

    instanceTab = []

    def __init__(self, size, _Xpos=None, _Ypos=None, _rotation=None):
        self.instanceTab.append(self)
        self.size = size
        self.etat = [1]*size
        self.placeBoat(_Xpos, _Ypos, _rotation)
        # pygame.sprite.Sprite.__init__(self)
        # self.image, self.rect = load_png('ball.png')

    def placeBoat(self, _Xpos=None, _Ypos=None, _rotation=None):
        self.Xpos = _Xpos
        self.Ypos = _Ypos
        self.rotation = _rotation

    def __str__(self):
        return "size:{},Xpos:{},Ypos:{},rotation{}".format(self.size,self.Xpos,self.Ypos,self.rotation)
           


class client:
    def __init__(self, name):
        self.name = name
        self.Boats = []

    def addBoat(self, boat):
        self.Boats.append(boat)

    def __str__(self):

        toreturn=""
        for boat in self.Boats:
            toreturn+=str(boat)+"\n"
        return "nom:{} \n {}".format(self.name,toreturn)


class BoardGame:
    listClient = [None]
    # boardTab[][]
    def __init__(self, size):
        # creation d'un tableau 2D de zeros de taille size
        self.boardTab = [[0] * size for _ in range(size)]

    def addClient(self, client):
        self.listClient.append(client)

    def renderBoats(self, bateau):
        if bateau.rotation == 0:
            for i in range(-1, 1):
                if(self.boardTab[bateau.Ypos][bateau.Xpos] == 1):
                    break

            i = -1
            for caseEtatBateau in bateau.etat:
                self.boardTab[bateau.Ypos][bateau.Xpos+i] = caseEtatBateau
                i = i+1

        else:
            i = -1
            for caseEtatBateau in bateau.etat:
                self.boardTab[bateau.Ypos+i][bateau.Xpos] = caseEtatBateau
                i = i+1

    def print(self):  # affiche le tableau boardTab a la maniere d'un tableau
        for c in self.boardTab:
            print(*c, sep='  ')

    # def addClient(self, client):

        # def placeBoat(self,bateau):
        # placer un bateau dans la board
