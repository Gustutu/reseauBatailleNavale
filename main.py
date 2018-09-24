import time
import BatailleNavaleClasses as BatNav

SIZE: int = 10

#petitBateau = BatNav.Bateau(3, 6, 6, 0)
#moyenBateau = BatNav.Bateau(4, 2, 2, 1)
#grandBateau = BatNav.Bateau(5, 2, 7, 0)
boardGame = BatNav.BoardGame(SIZE)

#hugo=BatNav.client("Hugo")




name=input("Quel est ton nom? ")
player=BatNav.gameMaster(name)
again='ok'
i=0
bateau=[]
while again == 'ok':
    taille = input("Quelle taille fait votre bateau? ")
    posX = input("Quelle coordonnée X ? ")
    posY = input("Quelle coordonnée Y ? ")
    orientation = input("Quelle orientation (horizontal=0/vertical=1)? ")
    bateau.append(BatNav.Bateau(int(taille), int(posX), int(posY), int(orientation)))
    again = input("Voulez vous faire un autre bateau (ok/no) ? ")
    i=i+1

for x in range(0, len(bateau)):
    player.addBoat(bateau[x])

print(player)

for x in range(0, len(bateau)):
    boardGame.renderBoats(bateau[x],SIZE)
    boardGame.print()




#print ("".join(str(boardGame.boardTab)))

#print ('\n'.join(''.join(*zip(*row)) for row in boardGame.boardTab))



time.sleep(5)
