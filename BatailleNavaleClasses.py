

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
        return "size:{},Xpos:{},Ypos:{},rotation{}".format(self.size,self.Xpos+1,self.Ypos+1,self.rotation)
           


"""class socketManager() : #la calsse socket manager hérite du module socket

    import socket 
    import select
    hote = ''
    port = 12800

    connexion_principale = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    connexion_principale.bind((hote, port))
    connexion_principale.listen(5)
    print("Le serveur écoute à présent sur le port {}".format(port))

    serveur_lance = True
    clients_connectes = []
    while serveur_lance:
        # On va vérifier que de nouveaux clients ne demandent pas à se connecter
        # Pour cela, on écoute la connexion_principale en lecture
        # On attend maximum 50ms
        connexions_demandees, wlist, xlist = select.select([connexion_principale],
            [], [], 0.05)
        
        for connexion in connexions_demandees:
            connexion_avec_client, infos_connexion = connexion.accept()
            # On ajoute le socket connecté à la liste des clients
            clients_connectes.append(connexion_avec_client)
        
        # Maintenant, on écoute la liste des clients connectés
        # Les clients renvoyés par select sont ceux devant être lus (recv)
        # On attend là encore 50ms maximum
        # On enferme l'appel à select.select dans un bloc try
        # En effet, si la liste de clients connectés est vide, une exception
        # Peut être levée
        clients_a_lire = []
        try:
            clients_a_lire, wlist, xlist = select.select(clients_connectes,
                    [], [], 0.05)
        except select.error:
            pass
        else:
            # On parcourt la liste des clients à lire
            for client in clients_a_lire:
                # Client est de type socket
                msg_recu = client.recv(1024)
                # Peut planter si le message contient des caractères spéciaux
                msg_recu = msg_recu.decode()
                print("Reçu {}".format(msg_recu))
                client.send(b"5 / 5")
                if msg_recu == "fin":
                    serveur_lance = False

    print("Fermeture des connexions")
    for client in clients_connectes:
        client.close()

    connexion_principale.close()"""

class gameMaster:
    def __init__(self, name):
        self.name = name
        self.Boats = []

    def addBoat(self, boat):
        self.Boats.append(boat)

    def __str__(self):

        toreturn=""
        for boat in self.Boats:
            toreturn+=str(boat)+"\n"
        return "nom:{} \n {}".format(self.name,toreturn)



#class client :
    

class BoardGame:
    listClient = [None]
    # boardTab[][]
    def __init__(self, size):
        # creation d'un tableau 2D de zeros de taille size
        self.boardTab = [[0] * size for _ in range(size)]

    def addClient(self, client):
        self.listClient.append(client)

    def renderBoats(self, bateau, sizeboard):
        #horizontal
        if bateau.rotation == 0:
            #Verification collision
            if bateau.Xpos+bateau.size > sizeboard:
                print("out of range")
                return 0

            for i in range(0, bateau.size-1):
                if self.boardTab[bateau.Ypos][bateau.Xpos+i] == 1:
                    print("there is another boat here (Pos: X Y)", bateau.Xpos+1, bateau.Ypos+1)
                    return 0

            #i = 0
            # Mise des cases à 1
                else:
                        for caseEtatBateau in bateau.etat:
                            self.boardTab[bateau.Ypos][bateau.Xpos+i] = caseEtatBateau
                            i = i+1
        #vertical
        else:
            #Verification collision
            if bateau.Ypos+bateau.size > sizeboard:
                print("out of range")
                return 0

            for i in range(0, bateau.size-1):
                if self.boardTab[bateau.Ypos+i][bateau.Xpos] == 1:
                    print("there is another boat here (Pos: X Y)", bateau.Xpos, bateau.Ypos)
                    return 0
                #i = 0
            # Mise des cases à 1
                else:
                    for caseEtatBateau in bateau.etat:
                        self.boardTab[bateau.Ypos+i][bateau.Xpos] = caseEtatBateau
                        i = i+1

    def print(self):  # affiche le tableau boardTab a la maniere d'un tableau
        for c in self.boardTab:
            print(*c, sep='  ')

    # def addClient(self, client):

        # def placeBoat(self,bateau):
        # placer un bateau dans la board
