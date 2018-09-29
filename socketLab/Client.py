# -*- coding:Utf8 -*-

from tkinter import *
import socket, sys, threading, time
from Serveur import AppServeur
host, port = '0.0.0.0', 2010
largeur, hauteur = 700, 400
COTE=400
NB_DE_CASES=10
PAS= COTE/NB_DE_CASES
MARGE=5


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
            if t[0] =="" or t[0] =="fin":
                # fermer le présent thread :
                break
            elif t[0] =="serveur OK":
                self.connexion.send("client OK".encode("Utf8"))

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
            self.textlabel.set(str(int(self.CX))+str(int(self.CY)))



    def specificites(self):
        "préparer les objets spécifiques de la partie client"
        self.jeu = Canvas(self, width=self.xm, height=self.ym,
                          bg='ivory', bd=3, relief=SUNKEN)
        self.jeu.pack(padx=4, pady=4, side=TOP)
        self.jeu.bind("<Button-1>", self.Clic)
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
        self.connex.envoie_msg(str(int(self.CX))+str(int(self.CY)))






if __name__ =='__main__':
    AppClient(host, port, largeur, hauteur).mainloop()