# Ticketing documentatie

## Functies
Het Claritas project vereist een robuust systeem on tickets aan te kunnen maken om problemen te die zich voordoen in de infrustructuur van het project te melden. 

Als achterliggende software werd Zammad (https://zammad.com/en) gekozen. De tool is lokaal installeerbaar, wat het gebruik van kostelijke cloudoplossingen niet nodig maakt. Het heeft ook een uitgebreide api die met andere componenten van Claritas kan communiceren. Tickets en gebruikers kunnen programmatisch worden aangemaakt en bekeken, alsook andere handige features waar we gebruik van maakte: 

- **Tags**:
Het toewijzen van tags aan tickets voor overzichtelijkheid. 

 

- **Triggers**:
Voorgeprogrammeerde acties kunnen automatisch worden uitgevoerd wanneer bepaalde condities overeenkomen. 

 

- **Scheduler**:
Hiermee kunnen acties worden uitgevoerd op basis van de tijd, hiermee kunnen bijvoorbeeld tickets die aan bepaalde criteria voldoen eender welke trigger laten uitvoeren, zoals een alarm laten afgaan. 

 

- **Webhooks**:
Er kunnen webhooks worden ingesteld om andere api’s aan te roepen, deze webhooks kunnen vervolgens worden uitgevoerd door een trigger. 
 

- **SLA’s (Service Level Agreements)**:
Hiermee wordt een timeframe ingesteld om systeembeheerders aan te sporen om tickets – al dan niet afhankelijk van hun prioriteit – binnen een bepaald timeframe een antwoord te geven. Het is deels overbodig aangezien we ook gebruikmaken van de scheduler, maar de scheduler heeft een minieme handicap waarmee hij slechts kan worden uitgevoerd op bepaalde ingestelde tijdstippen van de dag, terwijl een SLA kan worden ingesteld om bijvoorbeeld twee uur na het aanmaken van een ticket kan worden uitgevoerd, wat het een handige extra feature maakt. 


## Tickets
Tickets hebben heel wat attributen en kenmerken die kunnen worden ingesteld en aangepast. Deze zijn als volgt: 

- **Title**: 
De titel van een ticket zorgen ervoor dat je in een enkel oogopslag kunt zien waar de ticket over gaat. 
 

- **Subject**: 
Het onderwerp van het ticket. 
 

- **Message**: 
Hierin wordt een meer gedetailleerde uitleg gegeven over het probleem gerelateerd aan het ticket. 
 

- **Customer**: 
Hier bepaal je de Zammad gebruiker die verantwoordelijk is voor het openen van het ticket. Binnen ons systeem zal de initiële gebruiker altijd de api gebruiker (api@claritas.net) zal zijn. 
 

- **Group**:
Hier bepaal je de groep waaraan het ticket wordt toegewezen, in de context van ons systeem zal dit altijd de api groep zijn. 
 

- **State**:
Een ticket heeft drie mogelijke states: New, Open en Closed. Een ticket is altijd in de New state wanneer hij wordt aangemaakt, vervolgens verandert dit naar Open wanneer er een antwoord op het ticket is gegeven, en uiteindelijk Closed wanneer het ticket is afgehandeld. Een ticket kan van de Closed state terug naar Open gaan indien het ticket wordt heropend. Een ticket zal normaalgezien nooit verwijderd worden. 
 

- **Priority**:
Een ticket moet altijd een prioriteit krijgen. Hiervoor zijn er drie mogelijke opties: 1 low, 2 normal en 3 high. 
 

- **Tag**:
Je kan een tag toewijzen om tickets te categoriseren. Dit zal onder anderen gebruikt worden om tickets aan specifieke machines te linken. 


## Api
Zammad beschikt over een uitgebreide api om te kunnen communiceren met andere componenten in het systeem. De api is beschikbaar op http://localhost:8080/api/v1. Een voorbeeld request om tickets te bekijken ziet er zo uit: 

curl -H "Authorization: Bearer TOKEN" http://localhost:8080/api/v1/tickets 

 

Een ticket kan je laten aanmaken door een POST request te sturen met een json body met alle nodige attributen, die zijn als volgt: 

(Verplichte attributen zijn aangeduid met een ‘*’) 
| Attribuut        | Beschrijving                                                                                                 | Waarden                                                                                 |
|------------------|-------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| **title**        | De titel van het ticket.                                                                                    | string                                                                                  |
| **customer**     | De verantwoordelijke voor het aanmaken van het ticket, dit is altijd api@claritas.net.                      | "api@claritas.net"                                                                      |
| **group**        | De groep waar het ticket aan toebehoort. Dit is altijd api.                                                 | "api"                                                                                   |
| **priority**     | De prioriteit van het ticket, kies tussen 1 low, 2 normal en 3 high.                                        | 1 low, 2 normal, 3 high                                                                 |
| **article**      | Hierin specifieer je attributen over de inhoud van het ticket, zoals subject en body.                       | article                                                                                 |
| **state**        | De state van het ticket, standaardwaarde is new, andere opties zijn open en closed.                         | new, open, closed                                                                       |

Bijkomende attributen voor het `article` attribuut:
| Attribuut        | Beschrijving                                                                                                 | Waarden                                                                                 |
|------------------|-------------------------------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| **subject**      | Het onderwerp van het ticket.                                                                               | string                                                                                  |
| **body**         | De inhoud van het ticket.                                                                                   | string                                                                                  |
| **type**         | Het type communicatie dat het ticket voortbrengt. Het type zal altijd note zijn.                            | "note"                                                                                  |
| **internal**     | Bepaal of het ticket zichtbaar is voor customers of niet. Mogelijkheden zijn true of false.                 | true, false                                                                             |


### Voorbeelden voor het werken met de api:
```curl -H "Authorization: Bearer TOKEN" http://localhost:8080/api/v1/tickets -H "Content-Type: application/json" -d '{ "title": "Help!!", "group": "api", "customer": "api@claritas.net", "priority": "3 high", "article": { "subject": "Onderwerp", "body": "Er is een groot probleem", "type": "note", "internal": false } }' ```

 

Door een PUT request te sturen naar een ticket kan je tickets updaten. Om een ticket te specifieren voeg je het ticket id toe achteraan de endpoint. Je hoeft enkel de attributen te specifiëren die je wilt aanpassen: 

```curl -X PUT -H "Authorization: Bearer TOKEN" http://192.168.1.101:8080/api/v1/tickets/33 -H "Content-Type: application/json" -d '{"title": "No help for you","group": "api","state": "open","priority": "3 high","article": { "subject": "Update via API", "body": "Reden voor update...", "internal": true}}'```

 

Alle tickets en hun id’s kunnen worden teruggevonden met de api call die hiervoor werd genoemd (curl -H "Authorization: Bearer TOKEN" http://localhost:8080/api/v1/tickets). Het is ook mogelijk om tickets te zoeken op basis van een zoek query. Hiermee kan je makkelijk tickets filteren op basis van titel, tag, inhoud, ...: 

```curl -H "Authorization: Bearer TOKEN " http://localhost:8080/api/v1/tickets/search?query=zoekopdracht&limit=10 ```

 

Ten slotte kan je tickets verwijderen door een DELETE request te sturen naar het endpoint met het ticket id dat je verwijdert wil. Tickets verwijderen is niet aangeraden en in de plaats wordt er verwacht dat tickets voor altijd in het systeem blijven staan om altijd weer geraadpleegd te kunnen worden. Dit is dan ook de enige manier om een ticket definitief te verwijderen: 

```curl -X DELETE -H "Authorization: Bearer TOKEN" http://localhost:8080/api/v1/tickets/2``` 
