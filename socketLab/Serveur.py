# -*- coding:Utf8 -*-

host, port = '0.0.0.0', 2010
largeur, hauteur = 700, 400

# dimensions de l'espace de jeu

from tkinter import *
import socket, sys, threading, time

class ThreadConnexion(threading.Thread):
    """objet thread gestionnaire d'une connexion client"""
    def __init__(self, boss, conn):
        threading.Thread.__init__(self)
        self.connexion = conn           # réf. du socket de connexion
        self.app = boss
        # réf. de la fenêtre application


    def run(self):
        "actions entreprises en réponse aux messages reçus du client"
        nom = self.getName()            # id. du client = nom du thread
        while 1:
            msgClient = self.connexion.recv(1024).decode("Utf8")
            print("**{}** de {}".format(msgClient, nom))
            deb = msgClient.split(',')[0]
            if deb == "fin" or deb =="":
                self.app.enlever_canon(nom)
                # signaler le départ de ce canon aux autres clients :
                self.app.verrou.acquire()
                for cli in self.app.conn_client:
                    if cli != nom:
                        message = "départ_de,{}".format(nom)
                        self.app.conn_client[cli].send(message.encode("Utf8"))
                self.app.verrou.release()
                # fermer le présent thread :
                break
            elif deb=='11' :
                self.app.verrou.acquire()
                message = "touché"
                self.app.conn_client[nom].send(message.encode("Utf8"))
                self.app.verrou.release()
            elif deb=='22' :
                self.app.verrou.acquire()
                for cli in self.app.conn_client:
                    if cli != nom:
                        message = "bateau coulé "
                        self.app.conn_client[cli].send(message.encode("Utf8"))
                self.app.verrou.release()
            elif deb=='33' :
                self.app.verrou.acquire()
                message = "a l'eau"
                self.app.conn_client[nom].send(message.encode("Utf8"))
                self.app.verrou.release()


        # Fermeture de la connexion :
        self.connexion.close()          # couper la connexion
        del self.app.conn_client[nom]   # suppr. sa réf. dans le dictionn.
        self.app.afficher("Client %s déconnecté.\n" % nom)
        # Le thread se termine ici




class ThreadClients(threading.Thread):

    """objet thread gérant la connexion de nouveaux clients"""
    def __init__(self, boss, connex):
        threading.Thread.__init__(self)
        self.boss = boss                # réf. de la fenêtre application
        self.connex = connex


    def run(self):
        "attente et prise en charge de nouvelles connexions clientes"
        txt ="Serveur prêt, en attente de requêtes ...\n"
        #self.boss.afficher(txt)
        self.connex.listen(5)
        # Gestion des connexions demandées par les clients :

        while 1:
            var = self.boss.recupvar()
            if var !=0 :
                nouv_conn, adresse = self.connex.accept()
                var = self.boss.decrevar()
                print(var)
                # Créer un nouvel objet thread pour gérer la connexion :
                th = ThreadConnexion(self.boss, nouv_conn)
                th.start()
                it = th.getName()        # identifiant unique du thread
                # Mémoriser la connexion dans le dictionnaire :
                self.boss.enregistrer_connexion(nouv_conn, it)
                # Afficher :
                txt = "Client %s connecté, adresse IP %s, port %s.\n" %\
                       (it, adresse[0], adresse[1])
                self.boss.afficher(txt)
                # Commencer le dialogue avec le client :
                nouv_conn.send("serveur OK".encode("Utf8"))

class AppBN(Frame):
    '''Fenêtre principale de l'application'''
    def __init__(self, larg_c, haut_c):
        Frame.__init__(self)
        self.pack()
        self.xm, self.ym = larg_c, haut_c
        self.bTir = Button(self, text="Send", command=self.envoyermsg)
        self.bTir.pack(side=BOTTOM, padx=5, pady=5)
        self.textlabel = StringVar()
        self.label = Label(self,textvariable= self.textlabel)
        self.textlabel.set("Bonjour")
        self.label.pack(side=BOTTOM, padx=4, pady=6)
        self.specificites()

    def specificites(self):
        print()



class AppServeur(AppBN):

    """fenêtre principale de l'application (serveur ou client)"""
    def __init__(self, host, port, larg_c, haut_c):
        self.host, self.port = host, port
        AppBN.__init__(self, larg_c, haut_c)
        self.active =1
        # témoin d'activité
        #self.bind('<Destroy>',self.fermer_threads)


    def envoyermsg (self):
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
                self.textlabel.set(3)
                self.accueil = ThreadClients(self, connexion)
                self.accueil.start()

    def enregistrer_connexion(self, conn, it):
        "Mémoriser la connexion dans un dictionnaire"
        self.conn_client[it] = conn

    def afficher(self, txt):
        "afficher un message dans la zone de texte"
        self.avis.insert(END, txt)
    def decrevar (self) :
        self.textlabel.set(int(self.textlabel.get())-1)
    def recupvar(self):
        return  int(self.textlabel.get())




if __name__ =='__main__':
    AppServeur(host, port, largeur, hauteur).mainloop()