

# utilisation de set pour list de bateau par client
import socket
import select


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
        self.Xpos = _Xpos-1
        self.Ypos = _Ypos-1
        self.rotation = _rotation

    def __str__(self):
        return "size:{},Xpos:{},Ypos:{},rotation{}".format(self.size, self.Xpos+1, self.Ypos+1, self.rotation)


class gameMaster:
    def __init__(self, name):
        self.name = name
        self.Boats = []

    def tryAddBoat(self, boat):
        if BoardGame.tryAndAddBoat(boat) == 1:
            self.Boats.append(boat)

    def __str__(self):

        toreturn = ""
        for boat in self.Boats:
            toreturn += str(boat)+"\n"
        return "nom:{} \n {}".format(self.name, toreturn)


class gamePlayer:
    def __init__(self, name):
        self.name = name

    def tryFoundBoat(self, Xpos, Ypos):
        if BoardGame.tryFoundBoat(Xpos, Ypos) == 1:
            print("Touché", Xpos, Ypos)
        else:
            if BoardGame.tryFoundBoat(Xpos, Ypos) == 2:
                print("Coulé", Xpos, Ypos)
            else:
                if BoardGame.tryFoundBoat(Xpos, Ypos) == 0:
                    print("Loupé", Xpos, Ypos)
                else:
                    print("Error")


class BoardGame:
    listClient = [None]
    size = 0
    boardTab = [0][0]

    def __init__(self, size):
        # creation d'un tableau 2D de zeros de taille size
        BoardGame.boardTab = [[0] * size for _ in range(size)]
        BoardGame.size = size

    def addClient(self, client):
        self.listClient.append(client)

  #  def renderAllBoats(self, BoatList):
   #     for boat in BoatList:
    #        self.renderBoats(boat)

    def tryAndAddBoat(bateau):
        # horizontal
        if bateau.rotation == 0:
            # Verification collision
            if bateau.Xpos+bateau.size > BoardGame.size:
                print("out of range")
                return 0

            for i in range(0, bateau.size-1):
                if BoardGame.boardTab[bateau.Ypos][bateau.Xpos+i] == 1:
                    print("there is another boat here (Pos: X Y)",
                          bateau.Xpos+1, bateau.Ypos+1)
                    return 0

            # i = 0
            # Mise des cases à 1
                else:
                    for caseEtatBateau in bateau.etat:
                        BoardGame.boardTab[bateau.Ypos][bateau.Xpos +
                                                        i] = caseEtatBateau
                        i = i+1
                    return 1
        # vertical
        else:
            # Verification collision
            if bateau.Ypos+bateau.size > BoardGame.size:
                print("max boat is ", bateau.Ypos+bateau.size)
                print("boardSize is ", BoardGame.size)
                print("out of range")
                return 0

            for i in range(0, bateau.size-1):
                if BoardGame.boardTab[bateau.Ypos+i][bateau.Xpos] == 1:
                    print("there is another boat here (Pos: X Y)",
                          bateau.Xpos, bateau.Ypos)
                    return 0
                # i = 0
            # Mise des cases à 1
                else:
                    for caseEtatBateau in bateau.etat:
                        BoardGame.boardTab[bateau.Ypos +
                                           i][bateau.Xpos] = caseEtatBateau
                        i = i+1
                    return 1

    def tryFoundBoat(Xpos,Ypos):
        if BoardGame.boardTab[Xpos,Ypos]==1:
            return 1
        else:
            return 0






    def print(self):  # affiche le tableau boardTab a la maniere d'un tableau
        for c in BoardGame.boardTab:
            print(*c, sep='  ')

    # def addClient(self, client):

        # def placeBoat(self,bateau):
        # placer un bateau dans la board
