#!/usr/bin/python

import os
import sys
from random import randint
from threading import Thread
import time

n_param = 0

#si on ne fournit pas les bons arguments, on stoppe le programme
if (len(sys.argv) > 1):
	if (sys.argv[1] == '-n'):
		if(len(sys.argv) < 3):
			print("erreur : l'option -n necessite un parametre de type int")
			exit(0)

		n_param = int(sys.argv[2])

#----------Lancement des processus fils---------------

print "Nombre de pieces a usiner : {}".format(n_param)

#lancement de la machine 1
m1pid = os.fork()

if m1pid == 0:
	os.execl("./machine1.py","a")
	

#lancement de la machine 2
m2pid = os.fork()

if m2pid == 0:
	os.execl("./machine2.py","a")
	

#lancement du robot
botpid = os.fork()

if botpid == 0:
	os.execl("./robot.py","a")


#---------Lancement de la generation de pieces---------
time.sleep(1)

nb_pieces_generees = 0

while nb_pieces_generees <= n_param:
	#generer piece de facon aleatoire
	r_gen = randint(1,3)

	if r_gen == 1:
		#generer piece a
		print 'A'
	elif r_gen == 2:
		#generer piece b
		print "B"
	else:
		#generer piece c
		print "C"
	
	time.sleep(1)