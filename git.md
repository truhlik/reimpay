# GIT 
Alokovaná jména pro základní branche:  
`master` - produkce  
`staging` - staging (server, který přesně kopíruje produkci, co jde na staging musí jít na produkci, slouží pro testování merge do produkce)  
`testing` - testovací server pro klienta  
`develop` - testovací server pro vývojáře  
  
<b>Všechny commity děláme v nových branches!</b>  
I. vytvoř branch  
    - Nové branch vychází vždy z `master`. Před vytvořením branche nezapomeň fetchnout.  
    - Pojmenování nových branchí  
`[hotfix/developer_name/task_name]` fix which should be merged to master ASAP  
`[fix/developer_name/task_name]` fix which should be merged to develop or testing server  
`[feature/developer_name/task_name]` feature which should by properly tested in develop branch  

II. programuj  

III. commituj po co nejmenších logických částech    
    - Commit message by měla obsahovat jako prefix název branche do které se dělá. Např.
`[feature/lubos/new-feature] this is first commit for new feature #slug`
    - v každé commit message by měl být obsažen #slug z clickupu aby se commity daly v clickupu trackovat

IV. nezapomeň dělat testy a pouštět testy  
`python manage.py test`

V. mergni hotovou branch zpět    
        - Ve chvíli, kdy je branch hotová, tak jí mergujeme do základních branches, podle pravidel pro jednotlivé branche.  
        - Před mergem je nutné fetchnout nové změny v dané větvi, abychom si byli jistí, že mergujeme do aktuálního kódu.    
        - Po namergování branch je nutné vyzkoušet migrace.  
    `./manage.py migrate` by mělo proběhnout bez konfliktů, pokud tam jsou tak musíme vyřešit merge migrací nebo manuálně a commitem už v aktuální základní branchi.  
        - Pokud se nám fetchly změny, tak je nutné kód znovu otestovat.  
        - Merge do masteru děláme přes MERGE REQUEST na gitlabu.

IV. pushni základní branch (kromě masteru)
  
V. deploy

# Deploy přes fabfile

I. Pro automatický deploy (do masteru) je potřeba mít nastavený správně fabfile
  
II. Do `.ssh/config` přidáme záznam o serveru na který budeme nasazovat:  
```
Host [zkratka_serveru]
   HostName [server.hostname]
   User [user]
   Port 22  # or another used for ssh
   ForwardAgent yes
```
IV. nasazení  
`./fab deploy_dev` - deployne na dev server  
`./fab deploy_test` - deployne na test server  
`./fab deploy_prod` - deployne na produkční server

# Deploy přes ansible

I. Je dobré dělat průběžně aktualizace rolí:
```
ansible-galaxy install -r requirements.yml --force
```   
(zatím nepotřebujeme a hlavně neumíme verzovat role :-) takže s přepínačem force).

II. Pak deploy takto:
```
ansible-playbook deploy_develop.yml -u administrator
```
nebo
```
ansible-playbook deploy_production.yml -u administrator
```