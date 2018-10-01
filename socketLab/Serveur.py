# -*- coding:Utf8 -*-
from tkinter import *
import socket
import threading
from socketLab import BatailleNavaleClasses as BatNav
import time

host, port = '0.0.0.0', 2010
largeur, hauteur = 700, 400

# dimensions de l'espace de jeu


class ThreadConnexion(threading.Thread):
    """objet thread gestionnaire d'une connexion client"""

    def __init__(self, boss, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        self.app = boss

        # réf. de la fenêtre application


    def veriflogin(self):
        msgClient = self.connexion.recv(1024).decode("Utf8")
        print("ref" + msgClient)
        if msgClient == 'usertoto':
            return True
        else:
            return False

    def closeth(self):
        self.connexion.close()


class ThreadClients(threading.Thread):

    """objet thread gérant la connexion de nouveaux clients"""

    def __init__(self, boss, connex):
        threading.Thread.__init__(self)
        self.boss = boss                # réf. de la fenêtre application
        self.connex = connex
        self.connexion = []

    def run(self):
        "attente et prise en charge de nouvelles connexions clientes"
        txt = "Serveur prêt, en attente de requêtes ...\n"
        # self.boss.afficher(txt)
        self.connex.listen(5)
        # Gestion des connexions demandées par les clients :
        co = 1
        while co:
            var = self.boss.recupvar()
            if var != 0:
                nouv_conn, adresse = self.connex.accept()
                # Créer un nouvel objet thread pour gérer la connexion :
                th = ThreadConnexion(self.boss, nouv_conn)
                if th.veriflogin() == True:
                    var = self.boss.decrevar()
                    #th.start()
                    it = th.getName()        # identifiant unique du thread
                    # Mémoriser la connexion dans le dictionnaire :
                    self.connexion.append(nouv_conn)
                    self.boss.enregistrer_connexion(nouv_conn, it)
                    # Afficher :
                    txt = "Client %s connecté, adresse IP %s, port %s.\n" %\
                        (it, adresse[0], adresse[1])
                    self.boss.afficher(txt)
                    # Commencer le dialogue avec le client :
                    nouv_conn.send("serveur OK".encode("Utf8"))
                else:
                    nouv_conn.send("wrong login".encode("Utf8"))
                    th.closeth()
            else:
                self.boss.initjeux()
                co = 0
                self.boss.joueur()

    def returncoor(self,numjoueur):
        msgClient = self.connexion[numjoueur].recv(1024).decode("Utf8")
        return msgClient
    def broadcast (self,msg) :
        for y in self.connexion :
           y.send(msg.encode("Utf8"))

class AppBN(Frame):
    '''Fenêtre principale de l'application'''

    def __init__(self, larg_c, haut_c):
        Frame.__init__(self)
        self.pack()
        self.xm, self.ym = larg_c, haut_c
        self.bTir = Button(self, text="Send", command=self.envoyermsg)
        self.bTir.pack(side=BOTTOM, padx=5, pady=5)
        self.textlabel = StringVar()
        self.label = Label(self, textvariable=self.textlabel)
        self.textlabel.set("Bonjour")
        #modifié
        self.label.pack()
        #side=BOTTOM, padx=4, pady=6
        self.specificites()

    def specificites(self):
        print()


class AppServeur(AppBN):
    gameMaster = BatNav.gameManager("nom")
    boardGame = None
    nbjou = None

    """fenêtre principale de l'application (serveur ou client)"""

    def __init__(self, host, port, larg_c, haut_c):
        self.host, self.port = host, port
        AppBN.__init__(self, larg_c, haut_c)
        self.active = 1
        # témoin d'activité
        # self.bind('<Destroy>',self.fermer_threads)

    def envoyermsg(self):
        for cli in self.conn_client:
            print(cli)
        self.textlabel.set(0)

    def specificites(self):
        "préparer les objets spécifiques de la partie serveur"
        self.master.title('SERVEUR')

        # widget Text, associé à une barre de défilement :
        st = Frame(self)
        self.avis = Text(st, width=65, height=5)
        self.avis.pack(side=LEFT)
        scroll = Scrollbar(st, command=self.avis.yview)
        self.avis.configure(yscrollcommand=scroll.set)
        scroll.pack(side=RIGHT, fill=Y)
        st.pack()

        # partie serveur réseau :
        self.conn_client = {}  # dictionn. des connexions clients
        self.verrou = threading.Lock()  # verrou pour synchroniser threads
        # Initialisation du serveur - Mise en place du socket :
        connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            connexion.bind((self.host, self.port))

        except socket.error:
            txt = "La liaison du socket à l'hôte %s, port %s a échoué.\n" % \
                  (self.host, self.port)
            self.avis.insert(END, txt)
            self.accueil = None
        else:
            txt = "Serveur up \n"
            self.avis.insert(END, txt)
            # démarrage du thread guettant la connexion des clients :
            nb = input("nb de joueur ?")
            self.nbjou = int(nb)
            self.textlabel.set(nb)
            self.accueil = ThreadClients(self, connexion)
            self.accueil.start()

    def enregistrer_connexion(self, conn, it):
        "Mémoriser la connexion dans un dictionnaire"
        self.conn_client[it] = conn

    def afficher(self, txt):
        "afficher un message dans la zone de texte"
        self.avis.insert(END, txt)

    def decrevar(self):
        self.textlabel.set(int(self.textlabel.get())-1)

    def recupvar(self):
        return int(self.textlabel.get())

    def initjeux(self):
        # petitBateau = BatNav.Bateau(3, 6, 6, 0)
        # moyenBateau = BatNav.Bateau(4, 2, 2, 1)
        # grandBateau = BatNav.Bateau(5, 2, 7, 0)
        boardGame = BatNav.BoardGame(10)

        # hugo=BatNav.client("Hugo")

        name = input("Quel est ton nom? ")
        gameMaster = BatNav.gameManager(name)
        again = 'ok'
        i = 0

        while again == 'ok':
            taille = input("Quelle taille fait votre bateau? ")
            posX = input("Quelle coordonnée X ? ")
            posY = input("Quelle coordonnée Y ? ")
            orientation = input(
                "Quelle orientation (horizontal=0/vertical=1)? ")
            gameMaster.tryAddBoat(BatNav.Bateau(
                int(taille), int(posX), int(posY), int(orientation)))
            again = input("Voulez vous faire un autre bateau (ok/no) ? ")
            i = i + 1

        print(gameMaster)

        boardGame.print()

    def joueur(self):
        joueurs = []
        numjoueur = 0
        print(self.nbjou)
        for num in range(0,self.nbjou) :
            joueurs.append(BatNav.gamePlayer(num))
        while self.gameMaster.endOfGame == False:
              time.sleep(2)
              print("num : " + str(numjoueur))
              self.accueil.connexion[numjoueur].send("A toi de jouer".encode("Utf8"))
              msgClient = self.accueil.returncoor(numjoueur)
              tab=msgClient.split(";")
              x = tab[0]
              y = tab[1]
              print(x, y)
              res = joueurs[numjoueur].shoot(int(x), int(y))
              self.accueil.broadcast(x+';'+y+';'+res)
              if numjoueur == self.nbjou - 1:
                  numjoueur = 0
              else :
                numjoueur = numjoueur + 1
        self.accueil.broadcast("FIN")


      #jeux


if __name__ == '__main__':
    AppServeur(host, port, largeur, hauteur).mainloop()
