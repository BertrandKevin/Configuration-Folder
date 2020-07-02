#!/usr/bin/python

############################
# Librairies import
############################
import os

import checkUserInput
import configureIP as confIP
import configureNic as confNIC
import configureVPN as confVPN

############################
# Functions
############################
def configure_or_reset():
	answer = 0

	while answer != 1 and answer != 2:
		try:
			answer = int(input("Voulez-vous: \n" +
				"[1]: Effectuer une configuration particuliere\n" +
				"[2]: Effectuer une restauration aux parametres par defaut\n" +
				"Reponse: "))

		except:
			print("La reponse n'est pas valide!")
	return answer

def configuration_program():
	# Check if the user want to configure the IP address of the router
	if checkUserInput.question_and_verification("Voulez-vous configurer l'adresse IP?\n[Y]: Oui\n[n]: Non\n[exit()]: Quitter le programme\nReponse: ") == "y":
		confIP.main()

	# Check if the user want to configure the NIC and if yes, if he want an automatic configuration for the city of Paris or if he want a manual configuration
	if checkUserInput.question_and_verification("Voulez-vous configurer le NIC radio?\n[Y]: Oui\n[n]: Non\n[exit()]: Quitter le programme\nReponse: ") == "y":
		if checkUserInput.question_and_verification("Voulez-vous realiser une configuration automatique pour la ville de Paris?\n[Y]: Oui\n[n]: Non, je veux effectuer une configuration manuelle\n[exit()]: Quitter le programme\nReponse: ") == "y":
			confNIC.set_nic_settings("fd05:a40b:b47d:7340::4", "1250")
		else:
			confNIC.get_nic_settings()

	# Check if the user want to configure a VPN
	if checkUserInput.question_and_verification("Voulez-vous configurer un VPN?\n[Y]: Oui\n[n]: Non\n[exit()]: Quitter le programme\nReponse: ") == "y":
		confVPN.install_snap_vpn()
		confVPN.configure_snap()

############################
# Main program
############################
configurationOption = configure_or_reset()
print(configurationOption)

# 1 = Configuration by the user
# 2 = Reset of the router
if configurationOption == 1:
	configuration_program()
elif configurationOption == 2:
	# Reset IP Addresses settings
	netmask = "255.255.255.0"
	ipAddress = "192.168.16.1"
	confIP.search_network_information(ipAddress, netmask, "/var/snap/ssnmode", "interfaces_static")

	# Reset NIC settings
	aftr = "fd1e:d0d6:d81d:e070::76"
	countryCode = "276"
	confNIC.set_nic_settings(aftr, countryCode)


#p = os.system("sudo reboot")

