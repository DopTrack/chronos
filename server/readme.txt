In deze map staat het server gedeelte wat geplaatste word op de  doptrack.tudelft.nl
 Plaatst deze bestanden op de remote server en start met restartService.sh  

Er is een MonitorService die gegevens doorstuurd naar client (op initiatief van server zelf als er iets veranderd).
En er is een ControlService die reageert zoals een normale service. (client vraagt en server antwoord)  
 
En omdat beide commando's sturen naar de receiver, en deze slechts door 1
   tegelijk gebruikt mag worden is er een RecieverService die dit correct regelt en intern door beide gebruikt word.
      (script op server vuurt commando's direct op hardware en kan dus problemen veroorzaken) 

De 2 Services zijn met certificaten beveiligd, 
Op de server is de client.key niet nodig en op de client is de server.key niet nodig 
 
 De ReceiverService heeft geen certificaten nodig, want die breekt alle verbindingen af anders dan 127.0.0.1, en is dus alleen intern te gebruiken.