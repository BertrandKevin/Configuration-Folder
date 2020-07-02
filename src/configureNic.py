#!/usr/bin/python

############################
# Librairies import
############################
import os

import checkUserInput

############################
# Functions
############################
def set_nic_settings(aftr, countryCode):
	try:
		command = "sudo netmgr -i country_code set:" + countryCode
		p = os.system(command)
		print(p)
	except:
		print("Le country code n'a pas pu etre configure!")

	try:
		command = "sudo netmgr -i iotr aftr_address set " + aftr
		p = os.system(command)
		print(p)
	except:
		print("L'aftr n'a pas pu etre configure!")

def get_nic_settings():
	countryCode = 0
	aftr = ""

	while True:
		try:
			countryCode = int(input("Encodez le country code: "))
			question = "Validez-vous le country code " + str(countryCode) + " ?\n[Y]: Oui\n[n]: Non\n[exit]: Quitter le programme\nReponse: "

			if checkUserInput.question_and_verification(question) == "y":
				break
			else:
				print("Le country code n'a pas ete valide! Veuillez en encoder un nouveau!")
		except:
			print("Le country code n'est pas valide!")

	while True:
		aftr = input("Encodez l'AFTR: ")
		question = "Validez-vous l'AFTR " + aftr + " ?\n[Y]: Oui\n[n]: Non\n[exit]: Quitter le programme\nReponse:"

		if checkUserInput.question_and_verification(question) == "y":
			break
		else:
			print("L'AFTR n'a pas ete validee! Veuillez en encoder une nouvelle!")

	set_nic_settings(aftr, countryCode)
