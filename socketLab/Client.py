# -*- coding:Utf8 -*-

from tkinter import *
import socket, sys, threading, time
from Serveur import AppServeur
host, port = '0.0.0.0', 2010
largeur, hauteur = 700, 400
COTE = 400
NB_DE_CASES = 10
PAS = COTE/NB_DE_CASES
MARGE = 5


class ThreadSocket(threading.Thread):
    """objet thread gérant l'échange de messages avec le serveur"""
    def __init__(self, boss, host, port):
        threading.Thread.__init__(self)
        self.app = boss            # réf. de la fenêtre application
        # Mise en place du socket - connexion avec le  serveur :
        self.connexion = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.connexion.connect((host, port))
        except socket.error:
            print("La connexion a échoué.")
            sys.exit()
        print("Connexion établie avec le serveur.")
    def id(self):
        login = input("login :")
        mdp = input("mdp:")
        self.connexion.send(login.encode("Utf8") + mdp.encode("Utf8"))
        msg_recu = self.connexion.recv(1024).decode("Utf8")
        if msg_recu == 'wrong login':
            print("wrong login")
            return True
    def run(self):
        while 1:
            msg_recu = self.connexion.recv(1024).decode("Utf8")
            print("*%s*" % msg_recu)
            # le message reçu est d'abord converti en une liste :
            t =msg_recu.split(',')
            if t[0] =="FIN":
                self.app.setbouton(False)
            elif t[0] =="serveur OK":
                self.connexion.send("client OK".encode("Utf8"))
            elif t[0] =="A toi de jouer" :
                self.app.setbouton(True)
            else :
                tab = msg_recu.split(";")
                cx = int(tab[0])
                cy = int(tab[1])
                message = tab[2]
                print(cx, cy, message)
                self.app.dessiner(cx - 1, cy - 1, message)



        # Le thread <réception> se termine ici.
        print("Client arrêté. Connexion interrompue.")
        self.connexion.close()

    def envoie_msg(self,msg):
        print("tir")
        self.connexion.send(msg.encode("Utf8"))

class AppClient(AppServeur):
    CX = 0
    CY = 0

    def __init__(self, host, port, larg_c, haut_c):
        AppServeur.__init__(self, host, port, larg_c, haut_c)



    def Clic(self,evt):
        # position du pointeur de la souris
        if ((self.CX < NB_DE_CASES ) and (self.CY < NB_DE_CASES )):
            self.jeu.create_rectangle(MARGE + self.CX * PAS, MARGE + self.CY * PAS, PAS + MARGE + self.CX * PAS, PAS + MARGE + self.CY * PAS, outline='black')
        self.CX =float(evt.x)//PAS
        self.CY =float(evt.y)//PAS
        print(self.CX,self.CY)
        if ((self.CX < NB_DE_CASES ) and (self.CY < NB_DE_CASES )):
            self.jeu.create_rectangle(MARGE + self.CX * PAS, MARGE + self.CY * PAS, PAS + MARGE + self.CX * PAS, PAS + MARGE + self.CY * PAS, outline='red')
            #modifié
            self.textlabel.set(str(int(self.CX)+1)+';'+str(int(self.CY)+1))

    def dessiner(self,CX,CY,message):
        if message == "Touché":
            self.jeu.create_rectangle(MARGE + CX * PAS, MARGE + CY * PAS, PAS + MARGE + CX * PAS,
                                      PAS + MARGE + CY * PAS, fill='orange')
        elif message == "Loupé":
            self.jeu.create_rectangle(MARGE + CX * PAS, MARGE + CY * PAS, PAS + MARGE + CX * PAS,
                                      PAS + MARGE + CY * PAS, fill='blue')

    def specificites(self):
        "préparer les objets spécifiques de la partie client"
        self.jeu = Canvas(self, width=640, height=self.ym,
                          bg='ivory', bd=3, relief=SUNKEN)
        self.jeu.pack(padx=1, pady=1, side=LEFT)

        self.jeu.bind("<Button-1>", self.Clic)

        self.texttour = StringVar()
        self.lab = Label(self, textvariable=self.texttour)
        self.texttour.set("")
        self.lab.pack()
        #side = BOTTOM, padx = 5, pady = 7
        #Score
        self.textscore = StringVar()
        self.lab1 = Label(self, textvariable=self.textscore)
        self.textscore.set("SCORE DES JOUEURS:")
        self.lab1.pack(side=RIGHT, padx=5, pady=2)
        #self.textscore = StringVar()
        #self.score = Label(self, textvariable=self.textscore)
        #self.lab.pack(side=BOTTOM, padx=1, pady=5)

        x = 0
        while (x <= NB_DE_CASES):
            self.jeu.create_line(MARGE,MARGE+PAS*x,MARGE+COTE,MARGE+PAS*x,fill='black')
            self.jeu.create_line(MARGE + PAS * x, MARGE, MARGE + PAS * x,MARGE+COTE, fill='black')
            x = x + 1

        self.master.title('<<< Client >>>')
        self.connex =ThreadSocket(self, self.host, self.port)

        if(self.connex.id() == True ) :
            self.destroy()
            self.quit()
            exit()
        self.connex.start()
        self.id =None


    def envoyermsg(self):
        if self.texttour.get() == "A toi de jouer" :
            self.connex.envoie_msg(str(int(self.CX)+1)+';'+str(int(self.CY)+1))
            self.texttour.set("Patienter")

    def setbouton(self,bool):
        if bool ==True :
            self.texttour.set("A toi de jouer")
        elif bool == False :
            self.texttour.set("FIN DU JEU")



if __name__ =='__main__':
    AppClient(host, port, largeur, hauteur).mainloop()