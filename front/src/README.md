# Rmotor management Nuxt app

> Nuxt.js

```

## Install a build

``` bash
# nejdřív nainstaluj
$ npm install

# vývojové spuštění s hotreloadem na portu 3000
$ npm run dev

# produkční build a spuštění
$ npm run build
$ npm start
```

Pro lokální vývoj se podívej do skaffold.yaml a nastav si podle něj 
env proměnné (např. v Pycharmu Edit configurations)

For detailed explanation on how things work, checkout [Nuxt.js docs](https://nuxtjs.org).

## Using global SCSS variables
Variables can be defined in assets/scss/partials/variables.scss, thanks to nuxt
resource loader it is available in all templates

## ENV
Nastav si envy podle skaffold.json (např. ve svém IDE)

## Spuštění v dockeru
Vybuildění image a spuštění containeru

``` bash
docker build -t car_nuxt .
docker run -it --name car_nuxt -p 8088:8088 car_nuxt
```
Spuštění containeru na pozadí

``` bash
docker run -d --name car_nuxt -p 8088:8088 car_nuxt
```
Spuštění všech services clusteru
``` bash
cd ..
docker-compose up
```
Spuštení pouze těch services, které jsou nutné pro běh front appky
``` bash
cd ..
docker-compose up car-front
# může být potřeba přebuildit nějaké images
docker-compose up --build car-front
```

## Generování TS tříd
TS types, classes a interfaces se generují z JSON předpisu Swaggeru,
který je referencovaný skriptem v `types`, vše je obaleno npm příkazem

```
npm run generate_types
```
