# Use Cases
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

