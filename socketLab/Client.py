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
    def id(self,mdp,login):
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
            t=msg_recu.split(',')
            if t[0] =="FIN":
                self.app.setbouton(False)
            elif t[0] =="serveur OK":
                self.connexion.send("client OK".encode("Utf8"))
            elif t[0] =="A toi de jouer" :
                self.app.setbouton(True)
            elif t[0] =="Le score":
                self.app.setscore(msg_recu)
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

    def recoie_msg(self):
        return self.connexion.recv(1024).decode("Utf8")

class AppAdmin(AppServeur) :
    CX = 0
    CY = 0
    def __init__(self, host, port, larg_c, haut_c,login,mdp):
        AppServeur.__init__(self, host, port, larg_c, haut_c)
        self.login = login
        self.mdp = mdp

    def specificites(self):
        "préparer les objets spécifiques de la partie client"
        self.jeu = Canvas(self, width=self.xm, height=self.ym,
                          bg='ivory', bd=3, relief=SUNKEN)
        self.jeu.pack(padx=4, pady=4, side=TOP)

        self.jeu.bind("<Button-1>", self.Clic)
        self.texttour = StringVar()
        self.lab = Label(self, textvariable=self.texttour)
        self.texttour.set("Debut")
        self.lab.pack(side=BOTTOM, padx=5, pady=7)
        self.oui = Button(self, text="OUI", command=self.envoyeroui)
        self.oui.pack(side=BOTTOM, padx=7, pady=8)
        self.non = Button(self, text="NON", command=self.envoyernon)
        self.non.pack(side=BOTTOM, padx=10, pady=8)
        self.debutX = None
        self.finX = None
        self.debutY = None
        self.finY = None
        self.horiverti = None
        self.taille = None

        #self.textscore = StringVar()
        #self.score = Label(self, textvariable=self.textscore)
        #self.lab.pack(side=BOTTOM, padx=1, pady=5)

        x = 0
        while (x <= NB_DE_CASES):
            self.jeu.create_line(MARGE,MARGE+PAS*x,MARGE+COTE,MARGE+PAS*x,fill='black')
            self.jeu.create_line(MARGE + PAS * x, MARGE, MARGE + PAS * x,MARGE+COTE, fill='black')
            x = x + 1

        self.master.title('<<< ADMIN >>>')
        self.connex =ThreadSocket(self, self.host, self.port)

        if(self.connex.id(mdp,login) == True ) :
            self.destroy()
            self.quit()
            exit()
        self.id =None

    def envoyeroui(self):
         #self.connex.envoie_msg("OUI")
         self.texttour.set("Debut")
         self.connex.envoie_msg(str(int(self.debutX)) + ";" + str(int(self.debutY)) + ";" + str(self.horiverti) + ";" + str(self.taille) + ";" + "1")
         msg_recu = self.connex.recoie_msg()
         if msg_recu == 'NOK' :
             if self.debutX >= self.finX:
                 for case in range(self.finX, self.debutX + 1):
                     self.jeu.create_rectangle(MARGE + (case - 1) * PAS, MARGE + (self.debutY - 1) * PAS,
                                               PAS + MARGE + (case - 1) * PAS, PAS + MARGE + (self.debutY - 1) * PAS,
                                               fill='ivory',outline='black')
             elif self.debutX < self.finX:
                 for case in range(self.debutX, self.finX + 1):
                     self.jeu.create_rectangle(MARGE + (case - 1) * PAS, MARGE + (self.debutY - 1) * PAS,
                                               PAS + MARGE + (case - 1) * PAS, PAS + MARGE + (self.debutY - 1) * PAS,
                                               fill='ivory',outline='black')
         elif self.horiverti == 1:
             if self.debutY >= self.finY:
                 for case in range(self.finY, self.debutY + 1):
                     self.jeu.create_rectangle(MARGE + (self.debutX - 1) * PAS, MARGE + (case - 1) * PAS,
                                               PAS + MARGE + (self.debutX - 1) * PAS, PAS + MARGE + (case - 1) * PAS,
                                               fill='ivory',outline='black')

             elif self.debutY < self.finY:
                 for case in range(self.debutY, self.finY + 1):
                     self.jeu.create_rectangle(MARGE + (self.debutX - 1) * PAS, MARGE + (case - 1) * PAS,
                                               PAS + MARGE + (self.debutX - 1) * PAS, PAS + MARGE + (case - 1) * PAS,
                                               fill='ivory',outline='black')



    def envoyernon(self):
        # self.connex.envoie_msg("NON")
        self.texttour.set("Fin de l'initialisation")
        self.connex.envoie_msg(str(int(self.debutX)) + ";" + str(int(self.debutY)) + ";" + str(self.horiverti) + ";" + str( self.taille) + ";" + "0")
        msg_recu = self.connex.recoie_msg()
        print(msg_recu)

    def envoyermsg(self):
        if self.texttour.get() == "Debut" :
            self.debutX = int(self.CX) +1
            self.debutY = int(self.CY) +1
            print("debut : " + str(self.debutX) + str(self.debutY))
            self.texttour.set("Fin")
        elif self.texttour.get() == "Fin" :
            self.finX = int(self.CX)+1
            self.finY = int(self.CY)+1
            print("fin : " + str(self.finX) + str(self.finY))
            if self.debutX == self.finX :
                self.horiverti = 1
            elif self.debutY == self.finY :
                self.horiverti = 0

            if self.horiverti == 0 :
                if self.debutX >= self.finX :
                   self.taille =  (self.debutX - self.finX)+1
                   for case in range(self.finX,self.debutX+1) :
                       self.jeu.create_rectangle(MARGE + (case -1) * PAS , MARGE + (self.debutY-1) * PAS ,
                                                 PAS + MARGE + (case-1) * PAS, PAS + MARGE + (self.debutY-1) * PAS ,
                                                 fill='red')
                elif self.debutX < self.finX :
                    self.taille = (self.finX - self.debutX) +1
                    for case in range(self.debutX, self.finX+1):
                        self.jeu.create_rectangle(MARGE + (case - 1) * PAS, MARGE + (self.debutY - 1) * PAS,
                                                  PAS + MARGE + (case - 1) * PAS, PAS + MARGE + (self.debutY - 1) * PAS,
                                                  fill='red')
            elif self.horiverti == 1:
                if self.debutY >= self.finY :
                   self.taille =  self.debutY - self.finY + 1
                   for case in range(self.finY, self.debutY + 1):
                       self.jeu.create_rectangle(MARGE + (self.debutX - 1) * PAS, MARGE + (case - 1) * PAS,
                                                 PAS + MARGE + (self.debutX - 1) * PAS, PAS + MARGE + (case - 1) * PAS,
                                                 fill='blue')

                elif self.debutY < self.finY:
                    self.taille = self.finY - self.debutY + 1
                    for case in range(self.debutY, self.finY + 1):
                        self.jeu.create_rectangle(MARGE + (self.debutX - 1) * PAS, MARGE + (case - 1) * PAS,
                                                  PAS + MARGE + (self.debutX - 1) * PAS, PAS + MARGE + (case - 1) * PAS,
                                                  fill='blue')

            self.connex.envoie_msg(str(int(self.debutX)) +";"+ str(int(self.debutY)) +";"+ str(self.horiverti) +";"+ str(self.taille)+";"+"1")
            print(str(int(self.debutX)) + str(int(self.debutY)) + str(self.horiverti) + str(self.taille))

            self.texttour.set("Voulez vous ajouter un bateau?")



    def setbouton(self,bool):
        if bool ==True :
            self.texttour.set("A toi de jouer")
        elif bool == False :
            self.texttour.set("FIN DU JEU")


    def Clic(self,evt):
        # position du pointeur de la souris
        if ((self.CX < NB_DE_CASES ) and (self.CY < NB_DE_CASES )):
            self.jeu.create_rectangle(MARGE + self.CX * PAS, MARGE + self.CY * PAS, PAS + MARGE + self.CX * PAS, PAS + MARGE + self.CY * PAS, outline='black')
        self.CX =float(evt.x)//PAS
        self.CY =float(evt.y)//PAS
        print(self.CX,self.CY)
        if ((self.CX < NB_DE_CASES ) and (self.CY < NB_DE_CASES )):
            self.jeu.create_rectangle(MARGE + self.CX * PAS, MARGE + self.CY * PAS, PAS + MARGE + self.CX * PAS, PAS + MARGE + self.CY * PAS, outline='red')
            self.textlabel.set(str(int(self.CX)+1)+str(int(self.CY)+1))

    def dessiner(self,CX,CY,message):
        if message == "Touché":
            self.jeu.create_rectangle(MARGE + CX * PAS, MARGE + CY * PAS, PAS + MARGE + CX * PAS,
                                      PAS + MARGE + CY * PAS, fill='orange')
        elif message == "Loupé":
            self.jeu.create_rectangle(MARGE + CX * PAS, MARGE + CY * PAS, PAS + MARGE + CX * PAS,
                                      PAS + MARGE + CY * PAS, fill='blue')


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

        x = 0
        while (x <= NB_DE_CASES):
            self.jeu.create_line(MARGE,MARGE+PAS*x,MARGE+COTE,MARGE+PAS*x,fill='black')
            self.jeu.create_line(MARGE + PAS * x, MARGE, MARGE + PAS * x,MARGE+COTE, fill='black')
            x = x + 1

        self.master.title('<<< Client >>>')
        self.connex =ThreadSocket(self, self.host, self.port)

        if(self.connex.id(mdp,login) == True ) :
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

    def setscore(self, msg):
        self.textscore = StringVar()
        self.lab1 = Label(self, textvariable=self.textscore)
        self.textscore.set(msg)
        self.lab1.pack(side=RIGHT, padx=5, pady=2)




if __name__ =='__main__':
    login = input("login : ")
    mdp = input("mdp : ")
    if login == "admin" and mdp == "admin" :
        AppAdmin(host, port, largeur, hauteur,login,mdp).mainloop()
    elif login == "user" and mdp == "toto" :
        AppClient(host, port, largeur, hauteur).mainloop()
    else :
        print( "Wrong Login")