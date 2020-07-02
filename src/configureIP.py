#!/usr/bin/python

############################
# Librairies import
############################
import os

import checkUserInput

############################
# Functions
############################
def confirmation_address(address, what):
	confirmation = False

	if checkUserInput.question_and_verification("Confirmez-vous l'adresse " + address + " pour " + what + "\n[Y]: Oui\n[n]: Non\n[exit]: Quitter le programme\nReponse: ") == "y":
		print("L'adresse " + address + " pour " + what + " a ete confirmee avec succes!")
		confirmation = True
	else:
		print("L'adresse n'a pas ete confirmee! Veuillez la changer!")

	return confirmation

def check_array_input(array):
	for byte in array:
		if len(byte) > 3 or byte == "":
			print("L'adresse encodee n'est pas conforme!")
			correctInput = False
			break
		else:
			try:
				int(byte)
				correctInput = True
			except:
				print("L'adresse encodee n'est pas conforme!")
				correctInput = False
				break

	return correctInput

def check_input(type, what):
	while True:
		try:
			userInput = input("Encodez l'adresse" + type + "pour " + what + ": ")
			arrayInput = userInput.split(".")
		except:
			print("Une erreur s'est produite!")
			arrayInput = []

		if len(arrayInput) == 4:
			correctInput = check_array_input(arrayInput)
		else:
			print("L'adresse encodee n'est pas conforme!")
			correctInput = False

		if correctInput:
			confirmation = confirmation_address(userInput, what)

			if confirmation:
				return arrayInput

def confirm_dhcp_address(dhcpAddress, place, goodAddress):
	confirmation = False

	if goodAddress:
		confirmation = confirmation_address('.'.join(dhcpAddress), "la " + place + " address du DHCP ")

	if goodAddress == False or confirmation == False:
		print("Veuillez encodez manuellement la " + place + " addresse du range DHCP!")
		dhcpAddress = checkInput("", place + " client du range DHCP")

	return dhcpAddress

def calculate_dhcp(ipAddress, netmask):
	networkAddress = []
	broadcastAddress = []
	index = 0
	goodAddress = True

	for byte in netmask:
		if int(byte) == 255:
			networkAddress.append(str(ipAddress[index]))
			broadcastAddress.append(str(ipAddress[index]))
		elif int(byte) == 0:
			networkAddress.append(str(0))
			broadcastAddress.append(str(255))
		else:
			rangeAddress = 255 - int(byte)
			trySubNetwork = 0
			nbSubNetwork = 255/rangeAddress

			while trySubnetwork < nbSubNetwork:
				networkAddressByte = trySubNetwork * nbSubNetwork
				broadcastAddressByte = (trySubNetwork + 1) * nbSubNetwork

				if int(byte) >= networkAddress and int(byte) <= broadcastAddress:
					networkAddress.append(str(networkAddressByte))
					broadcastAddress.append(str(broadcastAddressByte))
					break

	firstDhcpAddress = networkAddress
	lastDhcpAddress = broadcastAddress

	try:
		firstDhcpAddress[3] = str(int(firstDhcpAddress[3]) + 1)
		lastDhcpAddress[3] = str(int(lastDhcpAddress[3]) - 1)
	except:
		goodAddress = False

	firstDhcpAddress = confirm_dhcp_address(firstDhcpAddress, "premiere", goodAddress)
	lastDhcpAddress = confirm_dhcp_address(lastDhcpAddress, "derniere", goodAddress)

	return firstDhcpAddress, lastDhcpAddress


def configure_dhcp(ipAddress, netmask):
	try:
		print("Enable dnsmasq")
		p = os.system("systemctl enable dnsmasq")
		print("Start dnsmasq")
		p = os.system("systemctl start dnsmasq")
	except:
		print("L'activation du service DHCP a echoue!")

	firstDhcpAddress, lastDhcpAddress = calculate_dhcp(ipAddress, netmask)

	# Prepare DHCP file
	line = "dhcp-range=" + '.'.join(firstDhcpAddress) + "," + '.'.join(lastDhcpAddress) + "," + '.'.join(netmask) + ",12h"

	try:
		path = "/home/dev/Configuration-Folder/51-dhcp-range.conf"

		with open(path, "w") as file:
			file.write(line)

	except:
		print("Impossible d'enregistrer le fichier de configuration!")

def configure_ipv6():
	if checkUserInput.question_and_verification("Voulez-vous utiliser le prefixe IPv6 par defaut d'EVESA: \"FD05:A40B:6F6::/48\" ?\n[Y]: Oui\n[n]: Non\n[exit]: Quitter le programme\nReponse: ") == "y":
		ipv6Prefix = "FD05:A40B:6F6::/48"

	else:
		while True:
			answer = input("Encodez le prefixe IPv6 sous la forme xxxx:xxxx:xxxx:xxxx/yy\nPrefixe: ")

			if confirmation_address(answer, "le prefixe IPv6"):
				ipv6Prefix = answer
				break

	try:
		commandLine = "sudo netmgr -i iotr network_prefix set " + ipv6Prefix
		print("Set IPv6 prefixe")
		p = os.system(commandLine)
	except:
		print("Le prefixe IPv6 n'a pas pu etre encode!")

def search_network_informations(ipAddress, netmask, searchPath, filename):
	try:
		for root, dir, files in os.walk(searchPath):
			if filename in files:
				with open(os.path.join(root, filename), "r") as file:
					previousLine = ""
					ipv6Address = ""

					for line in file:
						if "iface eth0 inet6 static" in previousLine and "address" in line:
							ipv6Address = line

						previousLine = line

				macAddress = (':'.join(['{:02x}'.format((uuid.getnode() >> element) & 0xff) for element in range(0,8*6,8)][::-1]))
				line = "# Wired adapter #1\nauto eth0\niface eth0 inet static\n"
				line += "\taddress " + '.'.join(ipAddress) + "\n"
				line += "\tnetmask " + '.'.join(netmask) + "\n"
				line += "\thwaddress ether " + macAddress + "\n"

				if ipv6Address != "" :
					line += "\tiface eth0 inet6 static\n"
					line += ipv6Address

				line += "\tnetmask 64\n\n"
				line += "# Local loopback/n"
				line += "auto lo\n"
				line += "\tiface lo inet loopback"

				path = "/home/dev/Configuration-Folder/interfaces_static"

				with open(path, "w") as file:
					file.write(line)

				break
	except:
		print("Un probleme est survenu lors de la configuration des parametres du reseau!")

############################
# Main program
############################
def main():
	ipAddress = check_input(" ip ", "le routeur")
	netmask = check_input(" ", "le masque reseau")

	if checkUserInput.question_and_verification("Voulez-vous utiliser le service DHCP du routeur?\n[Y]: Oui\n[n]: Non\n[exit]: Quitter le programme\nReponse: ") == "y":
		configure_dhcp(ipAddress, netmask)
	else:
		try:
			print("Stop dnsmasq")
			p = os.system("systemctl stop dnsmasq")
			print("Disable dnsmasq")
			p = os.system("systemctl disable dnsmasq")
		except:
			print("La desactivation du service DHCP a echoue!")

	if checkUserInput.question_and_verification("Voulez-vous utilisez les adresses IPv6?\n[Y]: Oui\n[n]: Non\n[exit]: Quitter le programme\nReponse: ") == "y":
		configure_ipv6()

	search_network_informations(ipAddress, netmask, "/var/snap/ssnmode", "interfaces_static")
