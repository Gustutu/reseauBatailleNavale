
import time
import BatailleNavaleClasses as BatNav
import pygame
print("coucou")


petitBateau = BatNav.Bateau(3, 2, 2, 1)
moyenBateau = BatNav.Bateau(4, 2, 2, 1)
boardGame = BatNav.BoardGame(10)

hugo=BatNav.client("Hugo")

hugo.addBoat(petitBateau)
hugo.addBoat(moyenBateau)
print(hugo)





#print ("".join(str(boardGame.boardTab)))

#print ('\n'.join(''.join(*zip(*row)) for row in boardGame.boardTab))



boardGame.renderBoats(petitBateau)
boardGame.print()
time.sleep(5)
