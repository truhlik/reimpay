# Instalace na lokalním prostředí

## Requirements
virtualenv
postgres unaccent extension

### Packages
python-3.7.3  

## Start project
I. stažení kódů a základní úpravy
```
git clone [projetct_name_git_url]
cd project_name
mkvirtualenv -p /usr/bin/python3.7 env
pip install -r requirements/local.pip
cp main/settings/local.py.sample main/settings/local.py
cp .env.sample .env
```    
II. Nastav si lokální settingy v souboru `main/settings/local.py` - volitelné.  
III. Nastav si proměnou prostředí DJANGO_SETTINGS_MODULE = main.setttings.localhost  
 - Pycharm - nastavení webserveru
 - Pycharm - preferences - Django
 - Pycharm - preferences - terminal     

III. Vytvoř si databázi v Postgresql, napr.:
```
sudo -u postgres psql
CREATE USER reimpay WITH PASSWORD 'reimpay';
CREATE DATABASE reimpay OWNER reimpay;
GRANT CONNECT ON DATABASE reimpay TO reimpay;
\c reimpay;
CREATE EXTENSION unaccent;
GRANT SELECT, INSERT, UPDATE, DELETE ON ALL TABLES IN SCHEMA public TO reimpay;
```
IV. Uprav si proměnné v souboru `.env` 
    - určitě bude potřeba nastavit DB připojení k tvé lokální postgres db
    - důležité je taky nastavení FIELD_ENCRYPTION_KEY - viz https://pypi.org/project/django-searchable-encrypted-fields/
    - pokud nepoužíváš smtp backend, tak nemusíš vyplňovat věci pro nastavení mailingu
    
V. Vytvoř si tabulky v DB `./manage.py migrate`

VI. Spusť projekt `./manage.py runserver`

## Front nuxt.js app
Readme v `front/README.md`


## Deploy
```
ansible-playbook deploy_develop.yml -u administrator
```

### Crontabs
- checking FIO bank account (every hour)  
`main.apps.fiobanka.cron.FioBankPairingPayments`
`main.apps.core.cron.FioBankProcessingPayments`
- generating Payments (jenom jeden den v měsíci dle nastavení constance)
`main.apps.payments.crons.GeneratingPayments`
- generate Comissions (jednou za týden)  `main.apps.credit.crons.GenerateCommissions`
- generate Invoices (poslední den v měsíci)  `main.apps.invoices.crons.GenerateInvoices`
- zavření Studie (jednou denně) `main.apps.core.cron.StudyCloseCron`

### Signals
- on approve PaymentVisitItem - approved signal emited which is handled by CreditBalance (create paycheck and commission)
