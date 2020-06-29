#!/bin/bash
ping -c4 10.1.91.50 >/dev/null
PINGINTERNET=$?
ping -c4 10.1.91.250 >/dev/null
PINGSERVEUR=$?

## Si le routeur est connecté au serveur et qu’il n’y a pas de tunnel VPN ouvert:
if [ $PINGINTERNET -eq 0 ] && [ ! -d /sys/class/net/tun0 ]; then
{
        echo "*"
	## On vérifie si un script OpenVPN est déjà démarré, on l’arrête avant d’en lancer un nouveau
        VAR=`pgrep -f "sudo snap run easy-openvpn.connect-server /home/dev/"`
        if pgrep -f "sudo snap run easy-openvpn.connect-server /home/dev/"; then kill -9 $VAR; fi

	## On démarre le script openVPN
        sudo snap run easy-openvpn.connect-server /home/dev/Configuration-Folder/Kara-IOTR1.ovpn
}
## Si on n’arrive pas à joindre le serveur VPN mais qu’un tunnel est ouvert:
elif [ $PINGSERVEUR -eq 1 ]  && [ -d /sys/class/net/tun0 ]; then
{
        echo "**"
	## On redémarre le système
        sudo reboot now
}
fi
echo "***"
exit 0
