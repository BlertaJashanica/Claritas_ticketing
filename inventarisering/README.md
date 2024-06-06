# Inventarisering
Voor project Claritas willen wij een inventaris aan netwerkapparaten kunnen bijhouden. Dit houdt in dat we altijd een lijst kunnen bijhouden met online apparaten in het netwerk en deze op basis van enkele kenmerken kunnen categoriseren. 

De inventaris zal worden opgebouwd in Checkmk. We hebben hiervoor gekozen omdat Checkmk een uitgebreide toolkit aanbiedt relevant voor onze doeleinden alsook omdat we zo makkelijk met de Monitoring module van Claritas kunnen integreren, die ook gebruikmaken van Checkmk. 

Checkmk kan lokaal worden gebruikt en biedt een uitgebreide api aan. Verder biedt het ook functionaliteit aan om hostfolders aan te maken en om tags en labels aan hosts toe te wijzen. Dit staat toe dat we hosts makkelijk kunnen categoriseren en refereren, en de inventaris zorgvuldig kunnen ordenen. 

## Hostfolders 
![image](https://github.com/BlertaJashanica/Claritas_ticketing/assets/83902653/33606365-bb7f-4b8e-a384-266f2d7e0da7)

Deze folders worden gebruikt om hosts in op te slaan. Je kan individueel hosts aan een folder toevoegen of met behulp van de Network Scan functionaliteit automatisch online hosts laten ontdekken binnen een gespecifieerd netwerk en deze in de folder plaatsen. 

![image](https://github.com/BlertaJashanica/Claritas_ticketing/assets/83902653/21464e78-b2f4-4411-8734-9c0068f12b3f)

De Network Scan functie leek een goede oplossing voor onze eisen, we konden aan de hand van Checkmk hosts op het netwerk automatisch laten ontdekken zonder dat we er zelf al te veel moeite voor moesten doen. Jammergenoeg heeft deze functie een ingebouwde tijdslimiet van 110 seconden wat het niet mogelijk maakt om grotere netwerken te scannen. Hiervoor moesten we een workaround vinden. 

We hebben ervoor gekozen om gebruik te maken van een Python script dat nmap aanstuurt en de Checkmk api om online hosts zo automatisch mogelijk aan de inventaris toe te voegen. Nmap wordt gebruikt om op efficiënte wijze hosts te ontdekken en vervolgens worden er checks op uitgevoerd zoals hostname discovery en os detectie. Gevonden hosts worden vervolgens aan een folder toegevoegd en krijgen een label met het os dat erop draait. Verder zullen hosts worden gelinkt aan hun tickets die voor deze hosts werden aangemaakt, hierover later meer. 

 

## Configuratie 

Bij het initieel opzetten van de inventaris krijgt de klant de optie om mee te geven welke folders er moeten worden aangemaakt en welke netwerken deze folders zullen bevatten. Nadat de initiële configuratie wordt uitgevoerd en de gekozen folders worden aangemaakt wordt het discovery script dat hiervoor vermeld werd aangeroepen, en die zal vervolgens de folders vullen volgens de geconfigureerde regels. 

Configuratie kan worden meegegeven in het ansible script, in het formaat '*Management:10.180.122.0/24,Databases:10.180.14.0/24*'. 
Dit zal de gepaste folders in Checkmk aanmaken: 
![image](https://github.com/BlertaJashanica/Claritas_ticketing/assets/83902653/87770f19-b586-4460-9e26-9e454e6cb04e)

Vervolgens worden deze folders gevuld met hosts uit het meegegeven netwerk: 
![image](https://github.com/BlertaJashanica/Claritas_ticketing/assets/83902653/f5ea9c5d-a5fe-4aa3-8f3f-c5b5f0cff118)

De folders zijn zodanig geconfigureerd dat Checkmk automatisch op zoek gaat naar monitoring agents op de hosts zoals SNMP agents en Checkmk agents. Eens deze op een host beschikbaar zijn zal er op die host automatisch service discovery worden uitgevoerd. 

Er wordt een cronjob ingesteld om deze discovery dagelijks te laten uitvoeren. Indien je later de folders en netwerken wil aanpassen kan dit makkelijk via de Checkmk interface. 

 

## Integratie met ticketing 

Voor een goede workflow en compliance worden hosts en tickets relevant voor deze hosts aan elkaar gelinkt. Dit wordt gedaan door URL's naar Zammad met de juiste zoekterm als attribuut mee te geven. 

Hiervoor werd attribuut ‘Ticket Reference’ aangemaakt, deze kan programmatisch worden aangevuld en is dus ook een functie van het script. URL’s zijn in de vorm van http://localhost:8080/#search/<hostname>. 
![image](https://github.com/BlertaJashanica/Claritas_ticketing/assets/83902653/120d46b5-9171-445d-a6f5-4bb1b5ee5701)
