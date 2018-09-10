
import pygame




class Bateau:
    # Xpos=None
    # Ypos=None
    
    instanceTab=[]
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

    


class client:
    # bateau[]=Null
    def __init__(self, name):
        self.name = name
        self.Boats=None


class BoardGame:
    # listClient[]
    # boardTab[][]
    def __init__(self, size):
        self.boardTab = [[0] * size for _ in range(size)]

    def renderBoats(self, bateau):
        if bateau.rotation == 0:
            for i in range(-1,1):
                if(self.boardTab[bateau.Ypos][bateau.Xpos]==1):
                    break

            
            i = -1
            for caseEtatBateau in bateau.etat:
                self.boardTab[bateau.Ypos][bateau.Xpos+i] = caseEtatBateau
                i = i+1

        else:
            i = -1
            for caseEtatBateau in bateau.etat:
                self.boardTab[bateau.Ypos+i][bateau.Xpos]=caseEtatBateau
                i=i+1


    def print(self):
        for c in self.boardTab:
            print(*c, sep='  ')

    # def addClient(self, client):

        # def placeBoat(self,bateau):
        # placer un bateau dans la board
