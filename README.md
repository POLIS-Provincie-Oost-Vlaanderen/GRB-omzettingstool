# GRB-omzettingstool

Doorheen de jaren zijn er in het Vlaamse GIS-landschap diverse basiskaarten gebruikt en de huidige basiskaart (GRB) kent vooralsnog geen 'rust in de kaart'. Een gevolg daarvan is o.a. dat thematische gegevens afgeleid van eerder kaartmateriaal niet langer perfect passen op een recente basiskaart. De kwaliteit van geodata neemt af en ruimtelijke analyse of bevraging worden bemoeilijkt.

[POLIS](https://oost-vlaanderen.be/bestuur-en-regio/wat-doet-het-provinciebestuur/e-government.html) heeft kennis en ervaring in huis om met deze uitdaging om te gaan. Thematische gegevens kunnen grotendeels automatisch worden afgestemd op een recente basiskaart Vlaanderen (GRB) met een tool die gebruik maakt van [QGIS](https://qgis.org).

Graag stelt POLIS de tool beschikbaar gesteld als:

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
  
## Documentation

Uitgebreidere informatie en een handleiding over de werking van de tool vind je [hier](https://linktodocumentation).


## Screenshots

Venster in QGIS

![App Screenshot](https://i.postimg.cc/C19npTC2/image.png)

## Video

[![GRB-omzettingstool](https://i.postimg.cc/2y5Kt5N4/image.png)](https://youtu.be/TmZXDBH5Q0A "GRB-omzettingstool")

## License

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html)

