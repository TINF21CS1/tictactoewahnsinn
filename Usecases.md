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


Dieser Use Case beschreibt den Prozess des Beenden/Verlassens eines Multiplayer-Spiels.