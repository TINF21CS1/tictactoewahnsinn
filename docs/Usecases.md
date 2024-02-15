**Use Case Template: Profilmanagement**

**Use Case ID:** UC1
**Use Case Name:** Profilmanagement
**Primary Actor:** Spieler  

**Stakeholders and Interests:**
- **Spieler:** Möchte ein Profil haben, um seine Spielerdaten zu verwalten.

**Preconditions:** Der Spieler hat die Anwendung gestartet.

**Success Guarantee (Postconditions):** Das Spielerprofil wurde erfolgreich erstellt, aktualisiert oder gelöscht.

**Main Success Scenario:**
1. Beim ersten Start der Anwendung wird ein Spielername abgefragt.
2. Der Spieler füllt die erforderlichen Felder aus.
3. Das System validiert die eingegebenen Informationen.
4. Das Spielerprofil wird erfolgreich erstellt und im System gespeichert.
5. Der Spieler wählt die Option, sein Profil einzusehen.
6. Das System zeigt dem Spieler alle relevanten Profilinformationen an.
7. Der Spieler wählt die Option, sein Profil zu aktualisieren.
8. Der Spieler ändert die gewünschten Informationen und speichert die Änderungen ab.
9. Das System validiert die aktualisierten Informationen.
10. Das Spielerprofil wird erfolgreich aktualisiert und im System gespeichert.
11. Der Spieler wählt die Option, sein Profil zu löschen.
12. Das System bestätigt die Löschung und löscht das Spielerprofil.
13. Alle damit verbundenen Daten und Statistiken werden ebenfalls gelöscht.
14. Der Spieler wird aufgefordert, einen neuen Spielernamen zu wählen.

Extensions (or Alternative flows):
*2/8. Wenn während des Erstellens oder Aktualisierens des Profils ungültige Informationen eingegeben werden:
	a. Das System zeigt eine Fehlermeldung an und fordert den Spieler auf, die Informationen zu korrigieren.
	b. Der Spieler korrigiert die Informationen gemäß den Anweisungen des Systems.
	c. Die Schritte für das Erstellen oder Aktualisieren des Profils werden fortgesetzt.

*11. Wenn der Spieler entscheidet, das Programm zu beenden, nachdem er das Profil gelöscht hat  aber noch keinen neuen Spielernamen gewählt hat:
	a. Das System startet so, als ob nie ein Profil vorhanden war und erwartet einen    Spielernamen vor dem Start der Anwendung.




**Use Case Template: Spiel Gegen KI**

**Use Case ID:** UC 2
**Use Case Name:** Spiel gegen KI 
**Primary Actor:** Spieler  

**Stakeholders and Interests:**
- **Spieler:** Möchte die Fähigkeiten gegen eine KI testen und sich selbst herausfordern, indem er unterschiedliche Schwierigkeitsgrade auswählt.

**Preconditions:** Der Spieler hat die Anwendung gestartet.

**Success Guarantee (Postconditions):** Der Spieler spielt ein Spiel gegen die KI.

**Main Success Scenario:**
1. Der Spieler wählt die Option, ein neues Spiel zu beginnen.
2. Der Spieler entscheidet sich für ein Spiel gegen die KI.
3. Der Spieler wählt den gewünschten Schwierigkeitsgrad der KI aus. 
4. Das System initialisiert ein neues Spielbrett.
5. Münzwurf, wer das Spiel beginnt – der Spieler oder die KI.
6. Das Spiel beginnt, und der gewählte Akteur macht den ersten Zug.
7. Der andere Akteur übernimmt den nächsten Spielzug. Dieser Schritt wird maximal 7 mal wiederholt.
8. Das Ergebnis wird ausgewertet.
9. Das Ergebnis des Spieles wird angezeigt.
10. Statistiken werden aktualisiert. 
11. Das Board wird beendet. 

Extensions (or Alternative flows):
*a. Jederzeit, wenn der Abbruch Button betätigt wird:
	1. Spiel wird als verloren gewertet.
	2. Statistiken werden aktualisiert. 
	3. Das Board wird beendet. 

**Technology and Data Variations List:**
- Die KI-Logik variiert je nach gewähltem Schwierigkeitsgrad, von einfachen bis hin zu komplexen, strategischen Entscheidungen.


**Use Case: Play Network Game**

**Use Case ID:** UC3
**Primary Actor:** Spieler 1 (Host), Spieler 2 (Gast)  

**Stakeholders and Interests:**
- **Spieler 1 (Host):** Möchte problemlos ein Spiel erstellen und spielen können.
- **Spieler 2 (Gast):** Beabsichtigt, einem Spiel einfach beizutreten und gegen den Host zu spielen.

**Preconditions:** 
Beide Spieler sind mit einem eindeutigen Identifier mit demselben Netzwerk verbunden und bereit, ein Spiel zu spielen.

**Success Guarantee (Postconditions):**
 Ein Multiplayer-Spiel wird erfolgreich gestartet, und beide Spieler können gegeneinander spielen. Nach dem Spiel wird die Verbindung getrennt und die Statistiken beider Spieler erfolgreich aktualisiert.

**Main Success Scenario:**
1. Beide Spieler finden sich in einer Lobby als Gast und Host zusammen.
2. Bei beiden Spielern wird innerhalb des Spiels eine temporäre Niederlage eingetragen. 
3. Eine Münze wird durch den Host geworfen, womit entschieden wird, wer beginnen darf.
4. Das Spiel beginnt.
5. Je nach Spielverlauf endet das Spiel entweder in einem Unentschieden, Sieg oder Niederlage, wobei dies dem jeweiligen Spieler angezeigt wird.
6. Der Spielausgang wird in die Statistik der jeweiligen Parteien eingetragen.
7. Nach dem Spiel wird die Verbindung zwischen den beiden Parteien geschlossen.

**Extensions (or Alternative Flows):**
- *a: Internet/-Synchronisationsprobleme:

      1. Fehlermeldung bei Host & Client, falls Toleranzen bei Synchronisationsinformationen nicht eingehalten werden.
      2. Erneute Verbindungsprüfung innerhalb eines bestimmten Zeitrahmens.
      3. Sollte Verbindungsprüfung fehlschlagen, Eintragen eines Unentschiedens bei Host & Client.
      4. Host & Client werden zu Hauptmenü geleitet.
- 4a: Ein Spieler verlässt Spiel frühzeitig:

      1. Bei dem entsprechenden Spieler wird die finale Niederlage und dem anderen ein Sieg eingetragen (temporäre Niederlage annuliert).

**Special Requirements:**
- Eine benutzerfreundliche Oberfläche für die Erstellung und das Beitreten zu Multiplayer-Spielen.


Dieser Use Case beschreibt den Prozess um das Starten, Spielen und Beenden eines Multiplayer-Spiels herum, bei dem zwei Spieler gegeneinander antreten können.

---
**Use Case: Host Game**

**Use Case ID:** UC3.1
**Primary Actor:** Spieler 1 (Host), Spieler 2 (Gast)  

**Stakeholders and Interests:**
- **Spieler 1 (Host):** Möchte problemlos ein Spiel erstellen und starten können sowie das Leaderboard bzw die Statistiken innerhalb des Spiels anzeigen.
- **Spieler 2 (Gast):** Sollte die Connection-Details des Hosts per Broadcast angezeigt bekommen.

**Preconditions:** 
Der Host ist mit einem Netzwerk verbunden, in welchen sich auch ein anderer Spieler befindet. Des Weiteren ist der Host bereit, ein Spiel zu starten.

**Success Guarantee (Postconditions):** 
Ein Multiplayer-Spiel wird durch den Host erfolgreich gestartet, die Statistiken bzw. das Leaderboard werden korrekt angezeigt, die Verbindungsdetails werden erfolgreich ins Netzwerk gesendet.

**Main Success Scenario:**
1. Spieler 1 wählt Multiplayer-Spiel aus und wird zum Host, wobei damit ein neues Spielfeld erstellt wird.
2. Innerhalb des eben erstellten Spielfelds werden die aktuellen Statistiken bzw das Leaderboard geladen.
3. Die Verbindungsinformationen werden per Broadcast im Netzwerk verbreitet.

**Extensions (or Alternative Flows):**
- 1a. Der Host wählt innerhalb des Muliplayer-Menüs einen bereits bestehenden Host aus:

      1. Der Host wird automatisch zum Client.
- 2a. Die Statistiken sind nicht verfügbar oder können nicht geladen werden:

      1. Es wird eine leere Liste angezeigt mit der Information, dass die Statistiken bzw. das Leaderboard aktuell nicht zur Verfügung steht.
- 3a. Verbindungsprobleme innerhalb des Netzwerks:

      1. Es findet eine Sendungswiederholung statt, wobei gleichzeitig eine Fehlermeldung ausgegeben wird.
      2. Wenn die Sendungswiederholung nicht erfolgreich ist, wird mehrere Male ein neuer Sendungsversuch unternommen, bis nach einer gewissen Zeit eine finale Fehlermeldung ausgegeben wird und der Host zum Hauptmenü weitergeleitet wird.

**Special Requirements:**
- Eine benutzerfreundliche Oberfläche für die Erstellung von Multiplayer-Spielen.


Dieser Use Case beschreibt den Prozess des Hostens eines Multiplayer-Spiels inkl. dem Senden von Verbindungsinformationen im lokalen Netzwerk.

---

**Use Case: Join Game**

**Use Case ID:** UC3.2
**Primary Actor:** Spieler 1 (Host), Spieler 2 (Gast)  

**Stakeholders and Interests:**
- **Spieler 1 (Host):** 
Stellt Verbindungsinformationen via Broadcast im Netzwerk zur Verfügung.
- **Spieler 2 (Gast):** 
Beabsichtigt, durch Eingabe der Verbindungsinformationen eines Hosts oder Auswählen eines Hosts aus der Liste der verfügbaren Spiele einem Spiel einfach beizutreten und gegen den Host zu spielen. Dabei sollen nach dem Beitreten mögliche Statistiken bzw. das Leaderboard durch den Host zur Verfügung gestellt und angezeigt werden.

**Preconditions:** 
Der Client ist mit einem Netzwerk verbunden, in dem sich auch der Host befindet, wobei beide Spieler einen eindeutigen Identifier besitzen. Der Host hat zudem bereits ein Spiel gestartet, wobei der Client bereit ist, dem Spiel beizutreten.

**Success Guarantee (Postconditions):** 
Einem Multiplayer-Spiel wird erfolgreich beigetreten, alle Statistiken bzw. das Leaderboard wird vollständig angezeigt und beide Spieler können gegeneinander spielen.

**Main Success Scenario:**

1. Spieler 2 wählt Spiel innerhalb des Multiplayer-Menüs aus oder gibt alternativ die IP des Hosts ein.
2. Spieler 2 verbindet sich erfolgreich zum Host.
3. Dem Spieler 2 werden die Statistiken bzw das Leaderboard korrekt angezeigt.

**Extensions (or Alternative Flows):**

1a. Der Client wählt Multiplayer-Spiel innerhalb des Multiplayer-Menüs aus:

      1. Der Client wird automatisch zum Host.
2a. Verbindung schlägt fehl:

	1. Verbindungswiederholung und Anzeigen einer Fehlermeldung
      2. Nach einer gewissen Anzahl an Versuchen wird eine finale Fehlermeldung ausgegeben, wobei der Client zum Hauptmenü weitergeleitet wird.
3a. Die Statistiken bzw. das Leaderboard werden nicht richtig angezeigt:

      1. Der Client lädt die Informationen nach einer gewissen Zeit automatisch neu.
      2. Sollte nach einer gewissen Anzahl an Versuchen immer noch keine Informationen zur Verfügung gestellt werden, wird eine Fehlermeldung ausgegeben.

**Special Requirements:**
- Eine benutzerfreundliche Oberfläche für das Beitreten zu Multiplayer-Spielen.


Dieser Use Case beschreibt den Prozess des Beitretens eines Multiplayer-Spiels durch den Client an einen Host im selben Netzwerk.

---

**Use Case: Leave Game**

**Use Case ID:** UC3.3
**Primary Actor:** Spieler 1 (Host), Spieler 2 (Gast)  

**Stakeholders and Interests:**
- **Spieler 1 (Host):** Stellt Spiel zur Verfügung.
- **Spieler 2 (Gast):** Möchte nach dem Spiel die Lobby verlassen

**Preconditions:** 
Beide Spieler haben einen erfolgreichen Spieldurchlauf und sind am Ende angelangt.

**Success Guarantee (Postconditions):** 
Die Verbindung von Gast zu Host wird erfolgreich getrennt. Beide Spieler befinden sich wieder im Hauptmenü

**Main Success Scenario:**
1. Spieler 2 verlässt die Lobby.
2. Die Verbindung zum Host wird geschlossen
3. Beide Spieler werden zum Hauptmenü geleitet.

**Extensions (or Alternative Flows):**

1a: Spieler 1 verlässt die Lobby:

      1. Dem Client wird eine Fehlermeldung angezeigt und er wird in das Hauptmenü geleitet.
1b: Spieler 2 verlässt die Lobby nicht:

      1. Der Host kann die Lobby verlassen. Damit wird auch der Client in das Hauptmenü geleitet.

**Special Requirements:**
- Eine benutzerfreundliche Oberfläche für das Verlassen des Spiels.


### UC4
**Use Case ID:** UC4  
**Use Case Name:** Echtzeit-Chat während des Spiels  
**Primary Actor:** Spieler 1, Spieler 2  
**Scope:** Online Multiplayer-Spiel  
**Level:** User Interaction  

**Stakeholders and Interests:**
- **Spieler 1 und Spieler 2:** Wollen während des Spiels effektiv kommunizieren, um Strategien zu teilen, Spielzüge zu diskutieren oder einfach soziale Interaktionen zu pflegen.

**Preconditions:** Ein Multiplayer-Spiel zwischen Spieler 1 und Spieler 2 ist aktiv und beide Spieler sind am Spiel beteiligt.

**Success Guarantee (Postconditions):** Spieler können während des aktiven Spiels in Echtzeit Nachrichten austauschen.

**Main Success Scenario:**
1. Ein Spieler (entweder Spieler 1 oder Spieler 2) wählt den Chat-Bereich innerhalb des Spiels.
2. Der Spieler tippt eine Nachricht in das Chat-Fenster ein und sendet sie ab.
3. Die gesendete Nachricht wird sofort an den anderen Spieler übertragen und in dessen Chat-Bereich angezeigt.
Die Schritt 1-3 können während des Spiels beliebig oft wiederholt werden.

**Extensions (or Alternative Flows):**
2a. Der Sender ist mit der Nachricht nicht zufrieden.
    1a. Der Sender kann die Nachricht editieren.
    1b. Der Sender kann die Nachricht löschen.
3a. Nachricht kann nicht übermittelt werden:
    Wenn die Nachricht nicht übermittelt werden kann, wird die sendende Partei darüber informiert.
    1a. Der Spieler kann versuchen, die Nachricht erneut zu senden.
    1b. Sendende Partei kann sich detaillierten Fehlerbericht anzeigen lassen.

**Special Requirements:**
- Wenn ein Spieler den Chat-Bereich nicht geöffnet hat und eine Nachricht empfängt, wird eine visuelle oder akustische Benachrichtigung angezeigt.
- Spieler können spezielle Chat-Kommandos verwenden, um Aktionen auszuführen, wie das Senden von Emoticons oder das Ausführen von Spielaktionen direkt aus dem Chat.
- Der Chat muss eine geringe Verzögerung aufweisen, um eine Echtzeit-Kommunikation zu gewährleisten.
- Die Chat-Oberfläche sollte auch während des aktiven Spiels leicht zugänglich und bedienbar sein, ohne das Spielgeschehen negativ zu beeinflussen.

**Technology and Data Variations List:**

Dieser Use Case beschreibt die Möglichkeit für Spieler, während eines aktiven Multiplayer-Spiels in Echtzeit zu kommunizieren. Er legt fest, wie Spieler den Chat öffnen, Nachrichten eingeben und senden können, und berücksichtigt dabei die Anforderung an sofortige Nachrichtenübermittlung für eine flüssige und engagierte Spielerfahrung.

---

### UC5

**Use Case: Spielstatistiken anzeigen**

**Use Case ID:** UC5

**Primary Actor:** Spieler

**Stakeholders and Interests:**
- **Spieler:** Interessiert an einer detaillierten Ansicht der eigenen und gegnerischen Leistungen, einschließlich Spielhistorie, Sieg/Niederlage-Verhältnis und anderer relevanter Statistiken, um Fortschritte zu verfolgen und Bereiche für Verbesserungen zu identifizieren.

**Preconditions:** 
Der Spieler hat mindestens ein Spiel in einem beliebigen Spiel abgeschlossen, und ist entweder in einem Spielmodus oder auf dem Statistik-Menü.

**Success Guarantee (Postconditions):** Die Spieler können eine vollständige Übersicht über ihre Spielstatistiken abrufen, einschließlich der gespielten Spiele, des Sieg/Niederlage-Verhältnisses und der Unterscheidung zwischen eigenen und gegnerischen Leistungen.

**Main Success Scenario:**
1. Der Spieler wählt im Menü die Option, seine Spielstatistiken anzusehen.
2. Das System sammelt und bereitet die Statistiken des Spielers auf, einschließlich:
   - Gesamtanzahl der gespielten Spiele
   - Sieg-Niederlagen-Verhältnis
   - Anzahl der Spiele gegen KI vs. andere Spieler
3. Das System zeigt die Statistiken auf einer dedizierten Seite an, einschließlich Sieg und Niederlageverlauf

---

1. Der Spieler startet einen beliebigen Spielmodus
2. Das System sammelt und bereitet die Statistiken des Spielers auf, einschließlich:
   - Gesamtanzahl der gespielten Spiele
   - Sieg-Niederlagen-Verhältnis
   - Anzahl der Spiele gegen KI vs. andere Spieler
3. Das System zeigt die Statistiken an der linken Seite des Spieles an

**Special Requirements:**
- Die Benutzeroberfläche für die Anzeige der Statistiken muss intuitiv und leicht navigierbar sein, um eine positive Benutzererfahrung zu gewährleisten.
- Die Datenaktualisierung muss nach einem gespielten Spiel erfolgen.
- Die eigene Statistik und die Gegnerstatistik müssen im Spiel vergleichbar sein
