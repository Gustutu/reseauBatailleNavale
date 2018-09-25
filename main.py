import time
import BatailleNavaleClasses as BatNav

SIZE: int = 10

#petitBateau = BatNav.Bateau(3, 6, 6, 0)
#moyenBateau = BatNav.Bateau(4, 2, 2, 1)
#grandBateau = BatNav.Bateau(5, 2, 7, 0)
boardGame = BatNav.BoardGame(SIZE)

#hugo=BatNav.client("Hugo")




name=input("Quel est ton nom? ")
gameMaster=BatNav.gameMaster(name)
again='ok'
i=0

while again == 'ok':
    taille = input("Quelle taille fait votre bateau? ")
    posX = input("Quelle coordonnée X ? ")
    posY = input("Quelle coordonnée Y ? ")
    orientation = input("Quelle orientation (horizontal=0/vertical=1)? ")
    gameMaster.tryAddBoat(BatNav.Bateau(int(taille), int(posX), int(posY), int(orientation)))
    again = input("Voulez vous faire un autre bateau (ok/no) ? ")
    i=i+1


print(gameMaster)

boardGame.renderAllBoats(gameMaster.Boats)

#for x in range(0, len(bateaux)):
 #   boardGame.renderBoats(bateaux[x], SIZE)

#oardGame.print()

time.sleep(5)
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print(".")
print("C'est désormais le moment pour les joueurs de participer !")
#print ("".join(str(boardGame.boardTab)))

#print ('\n'.join(''.join(*zip(*row)) for row in boardGame.boardTab))




