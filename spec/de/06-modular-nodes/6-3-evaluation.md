<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 6.3 Auswertung und Kopierverhalten

---

**Auswertung bei Mehrfach-Referenzierung:**

Da ein modularer Knoten nur einmal im `nodes`-Objekt existiert, sind alle strukturellen
Eigenschaften (`label`, `operator`, `children`, `capabilities`, etc.) automatisch identisch an jeder
Referenzstelle.

Das Evaluationsergebnis **DARF** jedoch pro Referenzstelle unterschiedlich sein. Bei der Auswertung
**MUSS** das Tool den Kontext berücksichtigen – also über welchen Pfad der modulare Knoten erreicht
wurde. Die Pfade werden zur Laufzeit aus der Baumstruktur (`children`-Arrays) berechnet.

---

**Beispiel:** Ein modularer Knoten "Bonitätsprüfung" (`lexId: 8`) wird an zwei Stellen referenziert:

| Pfad    | Kontext                                                     | Ergebnis |
| ------- | ----------------------------------------------------------- | -------- |
| `1.2`   | Direkter Aufruf von Root – vorgelagerte Bedingungen erfüllt | `true`   |
| `1.3.1` | Aufruf über "Alternative Prüfungen" – andere Datenlage      | `false`  |

---

**Speicherung der Ergebnisse:**

Da ein modularer Knoten unterschiedliche Ergebnisse pro Pfad haben kann, werden die
Auswertungsergebnisse im `results`-Objekt der RUML-Result-Datei nach **Pfad** indiziert (siehe
[Kapitel 5.1.2](../05-result-format/5-1-result-model.md)):

```jsonc
"results": {
  "1.2": {
    "lexId": "8",
    "status": "true",
    "reason": "AND: alle Kinder true"
  },
  "1.3.1": {
    "lexId": "8",
    "status": "false",
    "reason": "AND: Schufa-Score nicht erreicht"
  }
}
```

Die `lexId` wird als Pflichtfeld in jedem Ergebnis-Eintrag gespeichert, um die Zuordnung zum
Node-Objekt zu ermöglichen.

---
