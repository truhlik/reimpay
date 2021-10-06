# Rmotor management Nuxt app

> Nuxt.js

## Install a build

### Spuštění lokálně

nejdřív nainstaluj dependencies
``` bash
npm install
```

nastav si env, např
```.env
export API_URL=http://localhost:8000/api/v1
```

vývojové spuštění s hotreloadem na portu 3000
```
npm run dev
```

### Produkční build a spuštění
- uprav si `API_URL`
- uprav si složku, odkud bude nginx servírovat web 
- nastav nginx conf jako pro klasický statický web s index.html
- všechny dotazy na `/_nuxt/` musí směřovat do `/var/www/html/reimpay_front` 
(nebo složky, kterou jsi zvolil pro servírování nginxem) 
- všechny dotazy na `/icons/` musí směřovat do `/var/www/html/reimpay_front/icons`
```
cd src
export API_URL=http://localhost:8000/api/v1
npm install
npm run build
mv dist /var/www/html/reimpay_front
```

### Spuštění v dockeru

Vybuildi image se správnou API_URL

``` bash
docker build --build-arg API_URL=http://localhost:8000/api/v1 -t reimpay_front .
```

Spuštění containeru
```
docker run -it --name reimpay_front -p 8080:80 reimpay_front
```

Spuštění containeru na pozadí
``` bash
docker run -d --name reimpay_front -p 8080:80 reimpay_front
```

## Vývoj 

### Generování TS tříd

TS types, classes a interfaces se generují z JSON předpisu Swaggeru,
který je referencovaný skriptem v `types`, vše je obaleno npm příkazem

```
npm run generate-api
```
