import time
import BatailleNavaleClasses as BatNav

SIZE: int = 10

#petitBateau = BatNav.Bateau(3, 6, 6, 0)
#moyenBateau = BatNav.Bateau(4, 2, 2, 1)
# grandBateau = BatNav.Bateau(5, 2, 7, 0)
boardGame = BatNav.BoardGame(10)

# hugo=BatNav.client("Hugo")


name = input("Quel est ton nom? ")
gameMaster = BatNav.gameMaster(name)
again = 'ok'
i = 0

while again == 'ok':
    taille = input("Quelle taille fait votre bateau? ")
    posX = input("Quelle coordonnée X ? ")
    posY = input("Quelle coordonnée Y ? ")
    orientation = input("Quelle orientation (horizontal=0/vertical=1)? ")
    gameMaster.tryAddBoat(BatNav.Bateau(
        int(taille), int(posX), int(posY), int(orientation)))
    again = input("Voulez vous faire un autre bateau (ok/no) ? ")
    i = i+1


print(gameMaster)

boardGame.print()

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

name = input("Quel est ton nom joueur 1? ")
gamePlayer = BatNav.gamePlayer(name)

print("Bonjour", name)

X = input("Rentrez la première coordonnée ")
Y = input("Maintenant la seconde coordonnée ")

X = int(X)
Y = int(Y)
gamePlayer.tryFoundBoat(X, Y)

#print ("".join(str(boardGame.boardTab)))

#print ('\n'.join(''.join(*zip(*row)) for row in boardGame.boardTab))
