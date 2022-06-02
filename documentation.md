## Functioneel

### Inleiding:
De doptrack.tudelft.nl server is een linux machine waarop de ontvanger en recorder is aangesloten.
Op deze machine draait een script dat bepaald wanneer een sateliet in de goede positie is om een opname te starten. Dit resulteert een opname planning, waarbij de recorder op de juiste momenten een opname maakt.

Deze webapplicatie sluit aan op deze bestaande werkwijze.
Een student kan dan zijn eigen opname plan toevoegen aan de bestaande plannen.

De applicatie kent de volgende gebruikers groepen.
	(Tussen haakjes staat de benodigde instelling bij de user.)

**Niet ingelogd = anononieme gebruiker**
- default word een cms pagina getoond, met informatie over bijvoorbeeld de hardwdare opstelling en wat je er mee kan.
- kan verzoek indienen via deze webapp. Dit verzoek word per email verstuurd naar alle superusers en de gebruiker krijgt op ingevoerde reply email adress een bevestiging.
Om te voorkomen dat deze website als spam verspreider word gebruikt moet een capcha worden ingevuld.
- Recordings die op de server verwerkt zijn tot images waarin het dopler effect te zien is kunnen worden bekeken via deze applicatie. Het duurt ongeveer 15 sec voor alle 2000 image en tumbnail urls teruggestuurd zijn. Daarna is deze info 1 uur aanwezig in de webapp cache.

**Docenten: (groep docent)**
- Een docent kan een course aanmaken met een start en einddatum.
    De start en einddatum kunnen elkaar niet overlappen, 
    Ook kan de tijdsduur van de tijdsloten worden ingevoerd.
- Daarna kunnen studenten worden toegewezen aan de course.
- Default kan een docent tijdsloten toekennen aan studenten. Dit gaat via een drag en drop.
- Als achteraf de start en eindtijd of de tijdslot afmeting worden aangepast, dan kunnen studenten hun toegewezen tijdslot kwijtraken.
- Een docent kan geen vakken bewerken van een andere docent.

**Studenten : (groep student)**
- Een student die toegevoegd is aan een course kan inloggen op de applicatie.
- een student kan toegekende tijdsloten vrijgeven, of andere aanvragen door erop te klikken (mits slot nog vrij is en totaal niet meer dan 2.)
- Alle aanwezige geschedulde recordings worden getoond in een grafische weergave en in een lijst.
- De student kan in zijn tijdslot record schedules toevoegen.
- Schedules aangemaakt in deze webapp, resulteren in een yml file in de corecte opmaak voor de server. Daarna word alles opnieuw ingescheduled.   
- 	Als de opname klaar is dan word dit getoond in de lijs
- De opname kan ingezipt worden, dit scheelt ongeveer 90%. op de server worden alle zip verzoeken verzameld in een werklijst, en slechts 1 word tegelijk verwerkt.
In de recording lijst is te zien welk record op dat moment gecomprimeerd word en welke in de wacht staan.
- Zodra zip klaar is kan deze worden gedownload, de zip bevat ook de yml file.
- Recordings die op de server verwerkt zijn tot images waarin het dopler effect te zien is kunnen worden bekeken via deze applicatie.


Voor beheer doeleinden zijn mogelijk:

**superuser: (groep superuser + vinkje ‘staff status’)**
- Een superuser kan alles wat een docent kan. En dat voor alle ingevoerde courses.
- Als email adres word ingevuld bij user dan krijgt deze ook de verzoeken ingevuld door anonieme gebruikers.
- Superuser heeft ook rechten om users aan te maken (zelfs een admin)
 
**cms content beheren : (cms groep + vinkje ‘staff status’)**
- Het cms is een standaard django module, en is te beheren in de django admin site.
- Deze gebruiker kan via de standaard admin interface cms pagina’s beheren. Dit gaat via een web editor die redelijk makkelijk te gebruiken is.
- Als dit de enigste toegekende groep is dan ziet deze gebruiker alleen de cms_admin_main  page en een logout menu optie.
- Ook rechten op treesite omdat daar de tekst van de menu items te veranderen is.  (LET OP: geen menu items verwijderen of url id’s veranderen)

Vlak voor het renderen van de pagina word een cms id bepaald via de id van de resolved url en de sitetree menu groep die gebruikt word. en als er onder dat id een cms pagina bestaat dan word die bovenaan de pagina getoond. Dus per url gebruikersgroep combinatie is de mogelijkheid om cms informatie te tonen.

Er is mathJax support toegevoegd dus als je $$LATEX$$ als tekst in cms plaatst, dan zal dit in de browser weergegeven worden als formule. $LATEX$ is inline tekst
Op internet zijn formule editors te vinden die de benodigde LATEX kunnen genereren.
(bijvoorbeeld:  https://www.codecogs.com/latex/eqneditor.php)

Het bepalen van een menu gaat in de volgorde:
	 student, docent/superuser, ‘staff status‘  en anders word anonomous menu getoond

http://docs.django-cms.org/en/latest/user/reference/index.html

Bewerken kan in deze webapplicatie onder de volgende url.
/admin/cms/page/

Dit zijn alle mogelijke id’s die gebruikt worden in de applicatie
- cms_student_main
- cms_student_course-list
- cms_student_requesttimeslot
- cms_student_servercontrol
- cms_student_downloadFiles
- cms_student_image_gallery

- cms_docent_main
- cms_docent_course-list
- cms_docent_course-new
- cms_docent_course-edit
- cms_docent_managetimeslots
- cms_docent_servercontrol
- cms_docent_downloadFiles
- cms_docent_image_gallery

- cms_admin_main (iedereen met vinkje ‘staff status’ ziet deze main pagina tenzij je ook groep - student of docent/superuser hebt)

- cms_anonymous_main		(deze pagina zie je als je op main url komt en je niet bent ingelogd)
- cms_anonymous_login		(deze pagina zie je bij de inlog pagina)
- cms_anonymous_request		
- cms_anonymous_downloadFiles   (menuitem is niet zichtbaar in menu)
- cms_anonymous_image_gallery




**Admin:**   (een gebruiker waarbij vinkje ‘staff status’ en ‘superuser status’ is gezet.)
- Een admin kan alles beheren, in de admin site, mocht er iets mis zijn dan kun je dat met de admin rechtzetten, verder zou ik hem niet gebruiken  
- admin krijgt in doptrack gedeelte het menu admin voorgeschoteld, met alleen een main page en een logout.

## TAB
### remote server gedeelte:
Op de doptrack.tudelft.nl server draait een service doptrackwebappserver
Deze service start/stop een python script waarop de webapplicatie een aantal operaties kan uitvoeren.  
Deze aanroep is beveiligd middels self signed client server certificaten.

### Installatie:
plaats de volgende bestanden op de server (te vinden in source code remote folder).
- DoptrackControlService.py
- ReceiverService.py	(word momenteel niet aangeroeppen)
- settings.py
- common.py
- server crt en key
- client crt

file  init.d/webappservercontrol  is het service shell script bovenaan staat in commentaar hoe deze service te activeren is.

Error logs:
	linux os service:		/var/log/doptrackwebappserver.log
	remote python script:		/var/log/pythonDoptrackServer.log

Verbinding testen:
Er is een kort testbestand aangemaakt die gebruikt kan worden om de verbinding van webapp naar server te testen   remote/test/DoptrackClient_testServerFiles.py

Belangrijk is dat de genoemde imports aanwezig zijn. (anders merk je dat wel aan de foutmelding)
en dat paden naar client en server certificaten kloppen.

Als de remote verbinding niet werkt, dan zijn in de webapp geen schedules, recordings of images te zien.




DEVELOPER
Begonnen is met een standaard django applicatie

remote server gedeelte
- Er bleek python een module te zijn rpyc waarmee remote python functies kunnen worden aangeroepen alsof deze lokaal staan. Tot nu toe ben ik er tevreden over.
- Omdat je ook python scripts kunt doorsturen en die op remote gedeelte kunt uitvoeren, moet de goed beveiligd zijn. Dit kan middels client server certificaten (self signed is goed genoeg)
- De doptrack .tudelft.nl server word elke dag herstart daarom is er een service die ervoor zorgd dat dit python script dan weer geactiveerd word.

huisstijl
- huisstijl heb ik ontvangen als zip, deze heb ik in de applicatie geplaatst en gebruikt.
- De huisstijl bevat top menu, kruimelpath, menu boom bottom menu. Op dit moment word alleen top menu gebruikt.

treesite
- Ik heb treesite control gebruikt opdat deze een admin module gedeelte heeft. Alles verder configureer werk. Het enigste werk is gebruiken op de goede plek en daarbij een template aanwijzen die de menu boom kan renderen in tudelft huisstijl.
- Bij renderen pagina word bepaald welk treesite menu gebruikt moet worden, elke gebruikers groep heeft zijn eigen menu. Hierna kunnen de menus gerenderd worden. En word de geselecteerde menu node bepaald via de url die gevraagd is (netjes via reverse url id zoals het hoort in django). Elke menu node bevat een titel en die word dan gebruikt in de browser.

Drag en drop tijdslot manage control voor docent.
- Toekenen van studenten aan een tijdslot door de docent word gedaan via redisp drag en drop javascript control.

Grafische weergave serveractiviteit:
- Serveractiviteit control bestaat uit divs (idee eerder geebruikt om in studigids grafisch weer te geven wanneer course gegeven word en wanneer tentame is) en de locaties daarvan worden berekend aan de hand van de schedules en recordings. In de view is de div generator, en de kleurtjes komen van een css.

Photoswipe image gallery
- Photoswipe image javascript library toegevoegd. Dit is een gallery met thumbnails en informatie over image. Als een image geselecteerd word, dan word deze vergroot weergegeven (werkt ook op mobiel door te swipen) images staan op de server, via remote control worden alle image namen opgehaald, eventueel word een thumbnail aangemaakt, en de webapp cached deze volledige set voor 1 uur. Als er minder

django cms
- standaard django cms toegevoegd

mathjax django module
- grafisch weergeven van formules in browser, middels LaTeX notatie.
Het javascript draait in browser en controleert gehele document op $$LATEX$$ of $LATEX$, als deze gevonden word dan word dit omgezet in een grafische formule.
$$ is appart centraal veld en $ is inline tekst.

(Dit is dus niet speciaal voor cms het werkt in gehele applicatie)





Database content

TODO EXPORT ALL
TODO export sitetree  (menu instellingen voor gebruikers groepen)


export cms (including media dir)
De python django code word beheerd door de developer, deze word geplaatst in de docker image.
De docker image kan dan overal gedraaid worden.

De data (database en media files) leeft in productie en moet verplaatst kunnen worden tussen de OTAP Omgevingen.  A --> P,   P--> A,  P --> O,     O -->T-->A-->P  
Dus plaatsen bij docker files, dan kun je ze overal inchecken of vervangen, of lokaal overzetten naar je ontwikkel omgeving






