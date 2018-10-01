

# utilisation de set pour list de bateau par client
import socket
import select
import weakref
from collections import namedtuple
import pprint


class case:
    X = None
    Y = None
    etat = None

    def __init__(self, _X, _Y, _etat, _parent):
        self.parent = _parent
        self.X = _X
        self.Y = _Y
        self.etat = _etat

    def setEtatCase(self, _etat):
        self.etat = _etat
        # print("any case alive?", any(case.etat == 1 for case in self.parent.cases))
        if not(any(case.etat == 1 for case in self.parent.cases)):
            self.parent.enVie = False
            print("boat is dead")

        if not(any(bateau.enVie == 1 for bateau in gameManager.Boats)):
            print("end of game all boats dead")
            gameManager.endOfGame = True


class Bateau(case):
    cases = []

    # case = namedtuple("case", "X" "Y" "state")
    # cases=

    def __init__(self, size, _Xpos=None, _Ypos=None, _rotation=None):

        self.size = size
        self.cases = []
        print("nbcases here", len(self.cases))
        self.etat = [1]*size
        self.placeBoat(_Xpos, _Ypos, _rotation)
        self.enVie = 1
        # pygame.sprite.Sprite.__init__(self)s
        # self.image, self.rect = load_png('ball.png')

    def placeBoat(self, _Xpos=None, _Ypos=None, _rotation=None):
        self.Xpos = _Xpos-1
        self.Ypos = _Ypos-1
        self.rotation = _rotation
        if self.rotation == 0:
            for i in range(0, self.size):
                print("adding case", i)
                self.cases.append(case((self.Xpos)+i, self.Ypos, 1, self))

        else:
            for i in range(0, self.size):
                self.cases.append(case(self.Xpos, (self.Ypos)+i, 1, self))

    def __str__(self):

        return "size:{},Xpos:{},Ypos:{},rotation{}".format(self.size, self.Xpos+1, self.Ypos+1, self.rotation)


class gameManager:

    Boats = []
    endOfGame = False

    def __init__(self, name):
        self.name = name
        self.playerList = []
        self.numberOfPlayer = None

    def tryAddBoat(self, boat):
        val = BoardGame.tryAndAddBoat(boat)
        if val == 1:
            self.Boats.append(boat)
        return val


    def __str__(self):

        toreturn = ""
        for boat in self.Boats:
            toreturn += str(boat)+"\n"
        return "nom:{} \n {}".format(self.name, toreturn)

    def addPlayer(self, _name):
        playerList.addPlayer


class gamePlayer:
    def __init__(self, name):
        self.name = name
        self.score = 0

    def shoot(self, Xpos, Ypos):
        if BoardGame.handlePlayerShot(Xpos, Ypos) == 1:
            print("Touché", Xpos, Ypos)
            self.score = self.score + 1
            return ("Touché")
        elif BoardGame.handlePlayerShot(Xpos, Ypos) == 2:
            print("Coulé", Xpos, Ypos)
            return ("Coulé")
        elif BoardGame.handlePlayerShot(Xpos, Ypos) == 0:
            print("Loupé", Xpos, Ypos)
            return ("Loupé")
        else:
            print("Error")
            return ("Error")



class BoardGame:
    listClient = []
    bateauxList = []
    size = 0
    boardTab = [0][0]

    def __init__(self, size):
        # creation d'un tableau 2D de zeros de taille size
        BoardGame.boardTab = [[0] * size for _ in range(size)]
        BoardGame.size = size

  #  def renderAllBoats(self, BoatList):
   #     for boat in BoatList:
    #        self.renderBoats(boat)

    def tryAndAddBoat(bateau):
        # horizontal
        if bateau.rotation == 0:
            # Verification collision
            if bateau.Xpos + bateau.size > BoardGame.size:
                print("out of range")
                return 0

            for i in range(0, bateau.size):
                if BoardGame.boardTab[bateau.Ypos][bateau.Xpos + i] == 1:
                    print("there is another boat here (Pos: X Y)", bateau.Xpos + 1, bateau.Ypos + 1)
                    return 0
            # Mise des cases à 1
            for i in range(0, bateau.size):
                for caseEtatBateau in bateau.etat:
                    BoardGame.boardTab[bateau.Ypos][bateau.Xpos + i] = caseEtatBateau
            BoardGame.bateauxList.append(bateau)
            return 1
        # vertical
        else:
            # Verification collision
            if bateau.Ypos + bateau.size > BoardGame.size:
                print("max boat is ", bateau.Ypos + bateau.size)
                print("boardSize is ", BoardGame.size)
                print("out of range")
                return 0

            for i in range(0, bateau.size):
                if BoardGame.boardTab[bateau.Ypos + i][bateau.Xpos] == 1:
                    print("there is another boat here (Pos: X Y)",
                          bateau.Xpos, bateau.Ypos)
                    return 0

            # Mise des cases à 1
            for i in range(0, bateau.size):
                for caseEtatBateau in bateau.etat:
                    BoardGame.boardTab[bateau.Ypos + i][bateau.Xpos] = caseEtatBateau

            BoardGame.bateauxList.append(bateau)
            return 1

    def handlePlayerShot(xpos, ypos):
        print("etat boardtab:", "x:", xpos, "y", ypos,
              BoardGame.boardTab[ypos-1][xpos-1])
        if BoardGame.boardTab[ypos-1][xpos-1] == 1:
            BoardGame.boardTab[ypos-1][xpos-1] = 0
            bateau = BoardGame.aQuelBateauxEstCetteCase(xpos, ypos)
            print("nb case", len(bateau.cases))
            for acase in bateau.cases:
                pprint.pprint(acase)
                if((acase.X == xpos-1) & (acase.Y == ypos-1)):
                    acase.setEtatCase(0)
                    return 1

            if bateau.enVie == 0:
                return 2

        else:
            return 0

    def aQuelBateauxEstCetteCase(_X, _Y):
        for bateau in BoardGame.bateauxList:
            for acase in bateau.cases:
                if (acase.X == _X-1) & (acase.Y == _Y-1):
                    return bateau

        return 0

    def print(self):  # affiche le tableau boardTab a la maniere d'un tableau
        for c in BoardGame.boardTab:
            print(*c, sep='  ')

    # def addClient(self, client):

        # def placeBoat(self,bateau):
        # placer un bateau dans la board
