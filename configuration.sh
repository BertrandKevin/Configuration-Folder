#!/bin/bash

expect -c 'spawn su - ssn -c "python3 /home/dev/Configuration-Folder/src/app.py"; expect "Password:"; send "Xf@9=qZc\n"; interact'
echo "L'installation est terminée, le routeur va redémarrer automatiquement dans 1 minute!"
