
import time
import BatailleNavaleClasses as BatNav
import pygame
print("coucou")


petitBateau = BatNav.Bateau(3, 2, 2, 1)
moyenBateau = BatNav.Bateau(4, 2, 2, 1)
boardGame = BatNav.BoardGame(5)


print(petitBateau.size)
print(petitBateau.etat)
print(len(BatNav.Bateau.instanceTab))

#print ("".join(str(boardGame.boardTab)))

#print ('\n'.join(''.join(*zip(*row)) for row in boardGame.boardTab))

print(BatNav.Bateau.instanceTab)

boardGame.renderBoats(petitBateau)
test = print(boardGame.boardTab)
boardGame.print()
time.sleep(5)
