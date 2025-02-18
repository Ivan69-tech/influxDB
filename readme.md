Le but de ce projet est de déployer une base de données locale influx et de la connecter avec une database influx sur mon serveur.
Il faut créer un ficher .env a la racine du docker compose qui donnera les identifiants de la base locale et ceux de la base remote.

(donner un exemple du .env) 

le docker compose implémente un conteneur telegraf afin de recuperer les donnees d'un serveur modbus.
le repo contient un fichier de configuration dans le quel on configure les registres que l'on souhaite poller.

(expliquer comment configurer telegraf)

Un programme python s'occupe de synchroniser les deux databases. Dès que la connexion est perdue, la date du dernier succès de push est sauvegardée dans un volume docker.

Dès que la connexion est revenue, les donnees sont requetées à la base locale depuis la derniere successful date puis les pousse au serveur.

 