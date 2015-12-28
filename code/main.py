#!/usr/bin/python

# Classe principal, a appeler pour lancer la simulation
#
# CHABOISSIER Maxime
# MARTEAUX Anais
# PAPELIER Romain
# ROLLINGER Jerome
#
# Projet SE 2015 - Simulation d'usinage en temps reel

import os
import sys
from random import randint
from threading import Thread
from threading import Lock
import Queue
import time
import GenerateurObjet
from Machine import Machine
import signal
from robot import Robot

#----variables globales (parmetres de simulation)-----

#nombre de pieces a usiner
n_param = 5

#temps de generation par piece
tempsGen = 0.5

#temps d'usinage des pieces A par la machine 1
tempsM1a = 1
#temps d'usinage des pieces B par la machine 1
tempsM1b = 1

#temps d'usinage des pieces B par la machine 2
tempsM2b = 1
#temps d'usinage des pieces C par la machine 2
tempsM2c = 1

#temps de rangement des pieces A
tempsRA = 1
#temps de rangement des pieces B
tempsRB = 1
#temps de rangement des pieces C
tempsRC = 1

#definit si on affiche uniquement le rangement des pieces
dock_only = False

#params_ok = False


#----analyse des arguments----
i = 1
while i < len(sys.argv):
	arg = sys.argv[i]

	if arg == "-nbp":
		n_param = int(sys.argv[i+1])
		i+=1
	elif arg == "-tgen":
		tempsGen = float(sys.argv[i+1])
		i+=1
	elif arg == "-tu1a":
		tempsM1a = float(sys.argv[i+1])
		i+=1
	elif arg == "-tu1b":
		tempsM1b = float(sys.argv[i+1])
		i+=1
	elif arg == "-tu2b":
		tempsM2b = float(sys.argv[i+1])
		i+=1
	elif arg == "-tu2c":
		tempsM2c = float(sys.argv[i+1])
		i+=1
	elif arg == "-tra":
		tempsRA = float(sys.argv[i+1])
		i+=1
	elif arg == "-trb":
		tempsRB = float(sys.argv[i+1])
		i+=1
	elif arg == "-trc":
		tempsRC = float(sys.argv[i+1])
		i+=1
	elif arg == "--patrick-sebastien":
		print "Ha qu'est-ce qu'on est serres !"
		time.sleep(1.4)
		print "Au fond de cette boiteuh !"
		time.sleep(1.4)
		print "chantent les sardineuh !"
		time.sleep(1.4)
		print "chantent les sardineuh !"
		exit(0)
	elif arg == '--dock-only':
		dock_only = True
	else:
		print "Erreur : L'argument {} n'est pas reconnu".format(arg)
		exit(1)
	i+=1

#----------Lancement des processus fils---------------

print "Nombre de pieces a usiner : {}".format(n_param)

#file des pieces a usiner pour la machine 1
queueM1 = Queue.Queue()
#file des pieces a usiner pour la machine 2
queueM2 = Queue.Queue()
#file des pieces a ranger pour le robot
queueR = Queue.Queue()

#entrepots 
listeA = []
listeB = []
listeC = []

#lancement du robot
Rob = Robot(queueR,listeA, listeB, listeC,tempsRA,tempsRB,tempsRC, n_param)
Rob.start()

#lancement de la machine 1
M1 = Machine(1,["A","B"],queueM1,queueM2,queueR,tempsM1a, tempsM1b,0,Rob, dock_only)
M1.start()

#lancement de la machine 2
M2 = Machine(2,["B","C"],queueM2,queueM1,queueR,0,tempsM2b,tempsM2c,Rob,dock_only)
M2.start()

#---------Lancement de la generation de pieces---------

print("GENERATION LANCEE !")
gen = GenerateurObjet.GenerateurObjet(queueM1, queueM2, "Generateur", n_param, tempsGen, M1,M2,dock_only)
gen.start()

#enregistrement de la date de debut de fabrication
chronoDeb = time.time()

Rob.join()

#enregistrement de la date de fin de rangement
chronoFin = time.time()

M1.join()
M2.join()
gen.join()

histo1 = M1.getHisto()
histo2 = M2.getHisto()
histoRob = Rob.getHisto()
histoGen = gen.getHisto()

#---recapitulatif de production----

print "\n---SUIVI DE FABRICATION---"
print "Pieces generees: {}".format(histoGen)
print ""
print "Pieces usinees par M1: {}".format(histo1)
print "Pieces usinees par M2: {}".format(histo2)
print "\n---ETAT ENTREPOT---"

print "Entrepot A : {} pieces".format(len(listeA))
print "Entrepot B : {} pieces".format(len(listeB))
print "Entrepot C : {} pieces".format(len(listeC))
print "\nTemps de production total : {} s".format(round((chronoFin - chronoDeb),2))

exit(0)
