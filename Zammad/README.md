# Ticketing documentatie
Het Claritas project vereist een robuust systeem on tickets aan te kunnen maken om problemen te die zich voordoen in de infrustructuur van het project te melden. 

Als achterliggende software werd Zammad (https://zammad.com/en) gekozen. De tool is lokaal installeerbaar, wat het gebruik van kostelijke cloudoplossingen niet nodig maakt. Het heeft ook een uitgebreide api die met andere componenten van Claritas kan communiceren. Tickets en gebruikers kunnen programmatisch worden aangemaakt en bekeken, alsook andere handige features waar we gebruik van maakte: 

- **Tags** 
Het toewijzen van tags aan tickets voor overzichtelijkheid. 

 

- **Triggers** 
Voorgeprogrammeerde acties kunnen automatisch worden uitgevoerd wanneer bepaalde condities overeenkomen. 

 

- **Scheduler** 
Hiermee kunnen acties worden uitgevoerd op basis van de tijd, hiermee kunnen bijvoorbeeld tickets die aan bepaalde criteria voldoen eender welke trigger laten uitvoeren, zoals een alarm laten afgaan. 

 

- **Webhooks** 
Er kunnen webhooks worden ingesteld om andere api’s aan te roepen, deze webhooks kunnen vervolgens worden uitgevoerd door een trigger. 
 

- **SLA’s (Service Level Agreements)** 
Hiermee wordt een timeframe ingesteld om systeembeheerders aan te sporen om tickets – al dan niet afhankelijk van hun prioriteit – binnen een bepaald timeframe een antwoord te geven. Het is deels overbodig aangezien we ook gebruikmaken van de scheduler, maar de scheduler heeft een minieme handicap waarmee hij slechts kan worden uitgevoerd op bepaalde ingestelde tijdstippen van de dag, terwijl een SLA kan worden ingesteld om bijvoorbeeld twee uur na het aanmaken van een ticket kan worden uitgevoerd, wat het een handige extra feature maakt. 
