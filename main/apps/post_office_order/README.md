
## Skript, který vytvaří soubory pro poštovní poukázky typu B

### Start
Skript obsahuje dvě funkce "create_vstupni_datovy_soubor" a "create_podaci_stvrzenka"
#### Vstupní datový soubor (create_vstupni_datovy_soubor(data, path))
parametry funkce 
```bash
data - python dict
path - cesta pro vzniklý soubor
```
#### Podací stvrzenka (create_podaci_stvrzenka(data, path))
parametry funkce 
```bash
data - python dict
path - cesta pro vzniklý soubor
```

### Zkratky
```bash
VDS - Vstupní datový soubor
PDS - Podací stvrzenka
SM - Sumační věta
PV - Položková věta
```

### Zkratky pro sumační větu
```bash
ID - polozkove vety musi mit stejne jako SMv
DateVDS - datum VDS 
SerialNumber - pradove cislo VDS 
SenderNumber - cislo odesilatele
BankNumber  - kod banky
AccountPrefix - predcisli cisla uctu
AccountNumber - cislouctu
VariableSymbol - variabilni symbol
ConstantSymbol - konstantni symbol
SpecificSymbol - specificky symbol
AmountSM - castka sumacni veta
PriceSM - cena sumacni veta
SentenceNumber - pocet vet
Validity - platnost
PaymentType - zpusob uhrady
BankCodeSender - kod banky - cena
AccountPrefixSender - predcisli cisla uctu - cena
AccountNumberSender - cislo uctu - cena
ConstantSymbolSender - konstatni symbol - cena
ListNumber - cislo seznamu

```               
### Zkratky pro položkovou větu
```bash
ID - id musi byt stejny jak prislusna SMv
SerialNumberPV - poradove cislo polozkove vety 
SpecificationSender - specifikace adresata
SenderInfo - oznaceni adresata
Street  - ulice
HouseNumber - cislo domovni
PartOfCity - cast obce
City - mesto
ZipCode - psc
Message - zprava
Services - sluzby
PaymentDeadline - termin vyplaty
AmountPV - castka polozkova veta
PricePV - cena polozkova veta
Podaci cislo - podaci cislo
DistrictStamp - okresni razitko
SubmissionDate - datum podani
```               




                                                                        