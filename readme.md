Le but de ce projet est de deployer une base de donnees locale influx et de la connecter avec une database influx sur mon serveur.
il faut creer un ficher .env a la racine du docker compose qui donnera les identifiants de la base locale et ceux de la base remote.

(donner un exemple du .env) 


il s'agit de recuperer les donnees d'un serveur modbus grace a telegraf.

(expliquer comment configurer telegraf)


un fichier python vient faire le lien entre les deux databases. Dès que la connexion est perdue, la derniere date du dernier succes de push est sauvegardé (dans un volume docker)

Dès que la connexion est revenue, les donnees sont requetées de la base locale depuis la derniere successful date puis les pousse au serveur.

 