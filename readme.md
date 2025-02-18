Le but de ce répo est de déployer une base de données locale, alimentée par un serveur modbus, et de la synchroniser
avec une base de données hébergée sur un serveur. Il faut créer un ficher .env a la racine du docker compose qui donnera
les identifiants et infos de la base locale et ceux de la base remote. Toutes les variables d'environnement sont
définies dans le .env-example (utilisez et renommez ce fichier).

Le docker compose implémente un conteneur telegraf afin de récuperer les données d'un serveur modbus. Le repo contient
un fichier de configuration dans lequel on configure les registres que l'on souhaite poller. La configuration de
telegraf se fait dans le fichier ./telegraf/telegraf.conf. Adaptez cette partie du code :

```

[[inputs.modbus]]

name = "Device"
slave_id = 1
timeout = "1s"
interval = "2s"
controller = "tcp://modbus-server:1502"

holding_registers = [ { name = "register-1100", byte_order = "AB", data_type = "INT16", scale=1.0, address = [1100]}, ]
input_registers = [ { name = "registre-100", byte_order = "AB", data_type = "INT16", scale=1.0, address = [100]}, ]

```

Le docker compose embarque un petit serveur modbus en guise d'exemple (port 1502) avec le registre 1100 (holding,
uint16) et le registre 100 (input, uint16) dispo.

Un programme python s'occupe de synchroniser les deux databases. Dès que la connexion est perdue, la date du dernier
succès de synchronisation est sauvegardée dans un volume docker. Dès que la connexion est revenue, les données sont
requetées à la base locale depuis cette date sauvegardée puis les envoie au serveur.

Les images sont dispo ici : https://hub.docker.com/u/ivandecharbo

(projet non fini)
