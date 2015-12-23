#!/usr/bin/python

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

n_param = 0
params_ok = False

#si on ne fournit pas les bons arguments, on stoppe le programme
if (len(sys.argv) > 1):
	if (sys.argv[1] == '-n'):
		if(len(sys.argv) < 3):
			print("erreur : l'option -n necessite un parametre de type int")
			exit(0)

		n_param = int(sys.argv[2])
		params_ok = True


if params_ok == False:
	print("Erreur: arguments incorrects")
	exit(0)

#----------Lancement des processus fils---------------

print "Nombre de pieces a usiner : {}".format(n_param)

queueM1 = Queue.Queue()
queueM2 = Queue.Queue()
queueR = Queue.Queue()
queueA = Queue.Queue()
queueB = Queue.Queue()
queueC = Queue.Queue()


tempsGen = 0.5
tempsM1 = 1
tempsM2 = 1.5


#lancement de la machine 1
M1 = Machine(1,["A","B"],queueM1,queueM2,queueR,tempsM1)
M1.start()

#lancement de la machine 2
M2 = Machine(2,["B","C"],queueM2,queueM1,queueR,tempsM2)
M2.start()

#lancement du robot
Rob = Robot(queueR,queueA, queueB, queueC)
Rob.start()



#---------Lancement de la generation de pieces---------

print("generation lancee !")
gen = GenerateurObjet.GenerateurObjet(queueM1, queueM2, "Generateur", n_param, tempsGen, M1,M2)
gen.start()

M1.join()
M2.join()
gen.join()

exit(0)
