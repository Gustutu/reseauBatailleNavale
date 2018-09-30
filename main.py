import time
from socketLab import BatailleNavaleClasses as BatNav

SIZE: int = 10

#petitBateau = BatNav.Bateau(3, 6, 6, 0)
#moyenBateau = BatNav.Bateau(4, 2, 2, 1)
# grandBateau = BatNav.Bateau(5, 2, 7, 0)
boardGame = BatNav.BoardGame(10)

# hugo=BatNav.client("Hugo")


name = input("Quel est ton nom? ")
gameManager = BatNav.gameManager(name)
gameManager.numberOfPlayer = input("combien ya t il de joueurs? ")


again = 'ok'

while again == 'ok':
    taille = input("Quelle taille fait votre bateau? ")
    posX = input("Quelle coordonnée X ? ")
    posY = input("Quelle coordonnée Y ? ")
    orientation = input("Quelle orientation (horizontal=0/vertical=1)? ")
    gameManager.tryAddBoat(BatNav.Bateau(
        int(taille), int(posX), int(posY), int(orientation)))
    again = input("Voulez vous faire un autre bateau (ok/no) ? ")

    print("nb de case", len(BatNav.BoardGame.bateauxList[0].cases))

print(gameManager)

boardGame.print()

time.sleep(1)
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


while not(gameManager.endOfGame):
    X = input("Rentrez la première coordonnée ")
    Y = input("Maintenant la seconde coordonnée ")

    X = int(X)
    Y = int(Y)

    gamePlayer.shoot(X, Y)
    boardGame.print()
    print("end of game in main", gameManager.endOfGame)

#print ("".join(str(boardGame.boardTab)))

#print ('\n'.join(''.join(*zip(*row)) for row in boardGame.boardTab))
