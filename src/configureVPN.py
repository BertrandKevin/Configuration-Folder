#!/usr/bin/python

############################
# Librairies import
############################
import os

############################
# Functions
############################
def install_snap_vpn():
	try:
		p = os.system("sudo snap install /home/dev/Configuration-Folder/easy-openvpn_8.snap -- dangerous -- devmode")
	except:
		print("Impossible d'installer le snap \"easy-openvpn\"!")

def configure_snap():
	while True:
		answer = input("Encodez le nom exacte du client VPN (ex: client1.ovpn) ou \"exit\" pour annuler: ")

		if answer == "exit":
			break
		else:
			filePath = ""

			for root, dir, files in os.walk("/"):
				if answer in files:
					filePath = os.path.join(root, answer)
					break

			if filePath != "":
				write_openvpn_service(filePath)
				break
			else:
				print("Aucun service VPN avec le nom \"" + answer + "\" n'a ete trouve")

def write_openvpn_service(filePath):
	toWrite = "#!/bin/bash\n"
	toWrite += "ping -c4 10.1.91.50 >/dev/null\n"
	toWrite += "PINGINTERNET=$?\n"
	toWrite += "ping -c4 10.1.91.250 >/dev/null\n"
	toWrite += "PINGSERVEUR=$?\n\n"
	toWrite += "if [ $PINGINTERNET -eq 0 ] && [ ! -d /sys/class/net/tun0 ]; then\n"
	toWrite += "{\n"
	toWrite += "\tVAR=`pgrep -f \"sudo snap run easy-openvpn.connect-server /home/dev/\"`\n"
	toWrite += "\tif pgrep -f \"sudo snap run easy-openvpn.connect-server /home/dev/\"; then kill -9 $VAR; fi\n\n"
	toWrite += "\tsudo snap run easy-openvpn.connect-server " + filepath + "\n"
	toWrite += "}\n"
	toWrite += "elif [ $PINGSERVEUR -eq 1 ]  && [ -d /sys/class/net/tun0 ]; then\n"
	toWrite += "{\n"
	toWrite += "\tsudo reboot now\n"
	toWrite += "}\n"
	toWrite += "fi\n"
	toWrite += "exit 0"

	scriptPath = "/home/dev/Configuration-Folder/restartOpenVPN.sh"

	with open(scriptPath, "w") as file:
		file.write(toWrite)
