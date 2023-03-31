# GRB-omzettingstool

Doorheen de jaren zijn er in het Vlaamse GIS-landschap diverse basiskaarten gebruikt en de huidige basiskaart (GRB) kent vooralsnog geen 'rust in de kaart'. Een gevolg daarvan is o.a. dat allerlei thematische gegevens en plannen afgeleid van eerder kaartmateriaal niet meer perfect passen op een recente basiskaart. De kwaliteit van de geodata neemt af en ruimtelijke analyse en bevraging worden bemoeilijkt.

Om met deze uitdaging om te gaan, werden binnen [POLIS](https://oost-vlaanderen.be/bestuur-en-regio/wat-doet-het-provinciebestuur/e-government.html) in de loop van de jaren diverse tools ontwikkeld om thematische gegevens af te stemmen op een recente(re) basiskaart Vlaanderen (GRB). De tool die momenteel gebruik wordt, maakt gebruik van QGIS en werkt op basis van een aantal kenmerken van de geometrieën (ligging, overlapping en oppervlakte).

Op deze pagina wordt de tool toegelicht en beschikbaar gesteld als:

- model (model designer/graphical modeler QGIS)
- script (pyqgis)
- plugin QGIS (work in progress)


## Features

- Geodata geënt op een eerdere percelenkaart aanpassen naar de recentste basiskaart (Adp uit GRB)
- Gebruiksvriendelijk en amper voorbereidingstijd
- Resultaten: ongeveer 85% wordt automatisch goedgelegd
- Minder handmatige correcties dankzij de suggesties van het model

## Requirements

Windows - QGIS 3.22 (met taalinstelling: English US (EN_us))

## Installation

Er zijn twee mogelijkheden om de tool te installeren en te openen.

- Download het [zip-bestand](https://github.com/POLIS-Provincie-Oost-Vlaanderen/GRB-omzettingstool/blob/main/GRB-omzettingstool.zip) met daarin het model en het pyqgis script. Pak de bestanden uit, sla deze lokaal op en vervolgens kan je deze toevoegen en openen in QGIS via de Processing toolbox.

  ![App Screenshot](https://i.postimg.cc/sx6TP25L/image.png)

- Download de plugin binnen QGIS op https://plugins.qgis.org/plugins/ (work in progress)
  
## Documentatie

Uitgebreidere informatie en een handleiding over de werking van de tool vind je [hier](https://linktodocumentation).


## Screenshots

Venster in QGIS

![App Screenshot](https://i.postimg.cc/C19npTC2/image.png)

#Voor

#![App Screenshot](https://i.postimg.cc/ZqBbNfyP/voor.jpg)

Na

#![App Screenshot](https://i.postimg.cc/vZS8cRDH/na.jpg)

Inhoudstafel na het uitvoeren van het model

#![App Screenshot](https://i.postimg.cc/wjkfVHDg/image.png)

## Video

[![Everything Is AWESOME](https://img.youtube.com/vi/StTqXEQ2l-Y/0.jpg)](https://www.youtube.com/watch?v=StTqXEQ2l-Y "Everything Is AWESOME")

## Licentie

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html)

