
import time
import BatailleNavaleClasses as BatNav
import pygame
print("coucou")


petitBateau = BatNav.Bateau(3, 6, 6, 0)
moyenBateau = BatNav.Bateau(4, 2, 2, 1)
grandBateau = BatNav.Bateau(5, 2, 7, 0)
boardGame = BatNav.BoardGame(10)

hugo=BatNav.client("Hugo")

hugo.addBoat(petitBateau)
hugo.addBoat(moyenBateau)
hugo.addBoat(grandBateau)
print(hugo)





#print ("".join(str(boardGame.boardTab)))

#print ('\n'.join(''.join(*zip(*row)) for row in boardGame.boardTab))



boardGame.renderBoats(petitBateau)
boardGame.renderBoats(moyenBateau)
boardGame.renderBoats(grandBateau)
boardGame.print()
time.sleep(5)
