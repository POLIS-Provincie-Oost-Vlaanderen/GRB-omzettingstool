# Tool om thematische gegevens af te stemmen op een recente(re) basiskaart

Doorheen de jaren zijn er in het Vlaamse GIS-landschap diverse basiskaarten gebruikt en de huidige basiskaart (GRB) kent vooralsnog geen 'rust in de kaart'. Een gevolg daarvan is o.a. dat allerlei thematische gegevens en plannen afgeleid van eerder kaartmateriaal niet meer perfect passen op de recentste basiskaart. De kwaliteit van de geodata neemt af waardoor ruimtelijke analyses en bevraging wordt bemoeilijkt.

Manueel opsporen van fouten en correcties aanbrengen is een optie, maar een zeer arbeidsintensief, tijdrovend en eentonig proces. Gelukkig kan er e.e.a. worden geautomatiseerd.

De tool die binnen [POLIS](https://oost-vlaanderen.be/bestuur-en-regio/wat-doet-het-provinciebestuur/e-government.html) in gebruik is om met dit gegeven werkt op basis van een aantal kenmerken van de geometrieën (ligging, overlapping en oppervlakte).

Op deze pagina's wordt de tool toegelicht en beschikbaar gesteld als:

- model (binnen de model designer / graphical modeler van QGIS)
- script (in pyqgis)
- plugin binnen QGIS (work in progress)


## Features

- Thematische gegevens geënt op een eerdere percelenkaart aanpassen naar de recentste basiskaart (ADP uit GRB)
- Gebruiksvriendelijk en amper voorbereidingstijd
- Resultaten: ongeveer 85% wordt automatisch goedgelegd
- Minder handmatige correcties dankzij de suggesties van het model

## Requirements

QGIS 3.16 (minimum) met taalinstelling: English US (EN_us)

## Installatie

- het model (link naar download) openen in de Graphical modeler van QGIS (CTRL+ALT+G of via Processing => Graphical modeler)
- het pyqgis-script (een afgeleide van het model) openen in de Python Console van QGIS (CTRL+ALT+P)
- de plugin binnen QGIS (work in progress) wordt gepubliceerd op https://plugins.qgis.org/plugins/
  
## Documentatie

Uitgebreidere informatie en een handleiding over de werking van de tool vind je [hier](https://linktodocumentation).


## Screenshots

Venster in QGIS

![App Screenshot](https://i.postimg.cc/W1ns1JSn/image.png)

## Licentie

[GNU General Public License v3.0](https://www.gnu.org/licenses/gpl-3.0.html)



```
