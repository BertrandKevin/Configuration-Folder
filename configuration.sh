#!/bin/bash

expect -c 'spawn su - ssn -c "bash /home/dev/Configuration-Folder/installationAndConfiguration.sh"; expect "Password:"; send "Xf@9=qZc\n"; interact'
echo "L'installation est terminée, le routeur va redémarrer automatiquement dans 1 minute!"
