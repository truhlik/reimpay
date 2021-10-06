Ansible role pro základní nastavení serveru.

# Základní infromace
- REDIS - spuštěný a běží na socketu i TCP
127.0.0.1:6379   
'/var/run/redis/redis.sock'

- na FW povoleny jen 3 porty: 22, 80, 443

## Backup
- cron, který pouští BACKUP skript každý den
- dělá dump DB a posílá soubory skrze FTP na backup server (mail.eupolymer.cz) 
- používá balíček DUPLY