<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 5.0 Knotenstatus

Jeder Knoten, der ein Ergebnis hat, MUSS einen der folgenden vier Status haben. Der Status ist ein
**Laufzeit-Konzept** — er wird nicht in der RUML-Datei gespeichert, sondern in der zugehörigen
RUML-Result-Datei (`.ruml-result`, siehe [Abschnitt 5.1](5-1-result-model.md)).

| Status      | Beschreibung         | Semantik                                                                                      |
| ----------- | -------------------- | --------------------------------------------------------------------------------------------- |
| `true`      | Erfüllt              | Die Bedingung des Knotens ist erfüllt.                                                        |
| `false`     | Nicht erfüllt        | Die Bedingung des Knotens ist nicht erfüllt.                                                  |
| `undefined` | Nicht determinierbar | Die Prüfung wurde durchgeführt, aber das Ergebnis ist nicht eindeutig bestimmbar.             |
| `ignored`   | Übersprungen         | Die Prüfung wurde bewusst übersprungen (z.B. durch Short-Circuit oder manuelle Entscheidung). |

Jedes Knotenergebnis MUSS außerdem eine Begründung für seinen Status angeben; die Felder der
Begründung hängen vom Status ab.

Knoten DÜRFEN NICHT in das Ergebnis aufgenommen werden, bevor sie ausgewertet oder übersprungen
wurden.

### true

`true` signalisiert, dass die Bedingung des Knotens erfüllt ist:

- **Bei Leaf-Nodes:** Die entscheidungsrelevanten Capabilities ergeben `true`
- **Bei Parent-Nodes:** Die Operator-Logik über die Kind-Ergebnisse ergibt `true`

#### Begründung

Pflicht. Ein String mit einer menschenlesbaren Begründung:

_Knoten 1.1 – true_

```jsonc
"1.1": {
  "lexId": "2",
  "status": "true",
  "reason": "Age 34 >= 18",
  "capabilities": [/* ... */]
}
```

### false

`false` signalisiert, dass die Bedingung des Knotens nicht erfüllt ist:

- **Bei Leaf-Nodes:** Die entscheidungsrelevanten Capabilities ergeben `false`
- **Bei Parent-Nodes:** Die Operator-Logik über die Kind-Ergebnisse ergibt `false`

#### Begründung

Pflicht. Ein String mit einer menschenlesbaren Begründung:

_Knoten 1.4 – false_

```jsonc
"1.4": {
  "lexId": "3",
  "status": "false",
  "reason": "Credit score 540 < 600",
  "capabilities": [/* ... */]
}
```

### undefined

`undefined` signalisiert, dass eine Prüfung zwar durchgeführt wurde, aber kein eindeutiges Ergebnis
ermittelt werden konnte. Typische Ursachen:

- **Fehlende Daten:** Erforderliche Eingabedaten für die Auswertung sind nicht verfügbar
- **Technische Fehler:** API-Fehler, Timeouts oder Systemausfälle während der Auswertung
- **Logische Unentscheidbarkeit:** Widersprüchliche Regeln oder Daten
- **Capability ohne Ergebnis:** Eine entscheidungsrelevante Capability konnte kein eindeutiges
  Ergebnis ermitteln

**Wichtig:** `undefined` bedeutet "Prüfung durchgeführt, aber kein Ergebnis möglich" — nicht
"Prüfung nicht durchgeführt".

#### Begründung

Pflicht. Ein Objekt mit den folgenden Feldern, alle Pflicht:

| Feld      | Typ    | Beschreibung                                        |
| --------- | ------ | --------------------------------------------------- |
| `type`    | Enum   | Ursache des Status `undefined`, siehe Tabelle unten |
| `message` | String | Menschenlesbare Erläuterung (nicht leer)            |

Zusätzliche Felder sind NICHT erlaubt.

Das Feld `type` MUSS einen der folgenden Werte haben.

| Wert      | Ursache                                                                                                                                                                                                          |
| --------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `error`   | Ein technischer Fehler hat ein Ergebnis verhindert, z.B. ein fehlgeschlagener API-Aufruf, ein Timeout oder ein Knoten jenseits der maximalen Rekursionstiefe (siehe [6.4](../06-modular-nodes/6-4-recursion.md)) |
| `default` | Jede andere Ursache, z.B. fehlende Daten                                                                                                                                                                         |

_Knoten 1.3.2.2 – error: jenseits der maximalen Rekursionstiefe_

```jsonc
"1.3.2.2": {
  "lexId": "8",
  "status": "undefined",
  "reason": {
    "type": "error",
    "message": "Recursion depth 2 exceeds the maximum recursion depth of 1"
  }
}
```

_Knoten 1.2 – default: fehlende Daten_

```jsonc
"1.2": {
  "lexId": "4",
  "status": "undefined",
  "reason": {
    "type": "default",
    "message": "dp_income is missing"
  },
  "capabilities": [/* ... */]
}
```

### ignored

`ignored` unterscheidet sich von `undefined` dadurch, dass die Prüfung **bewusst nicht
durchgeführt** wurde. Typische Ursachen:

- **Short-Circuit-Evaluation im Modus `optimized`** (siehe Kapitel
  [3.6 Operatoren](../03-data-model/3-6-operators.md))
- **Manuelle Überspringung:** Ein Benutzer hat die Prüfung bewusst übersprungen
- **Konditionale Deaktivierung:** Der Knoten wurde aufgrund von Vorbedingungen deaktiviert

#### Begründung

Pflicht. Ein Objekt mit den folgenden Feldern, alle Pflicht:

| Feld       | Typ    | Beschreibung                                                                                                                                                                                                                                                                                                                                                                                           |
| ---------- | ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `type`     | Enum   | Ursache des Überspringens, siehe Tabelle unten                                                                                                                                                                                                                                                                                                                                                         |
| `trigger`  | String | Bezeichner des Geschwister- oder Knotens, der das Überspringen ausgelöst hat (nicht leer)                                                                                                                                                                                                                                                                                                              |
| `operator` | Enum   | Operator des Parent-Knotens; Tools nutzen ihn zur Darstellung des Ergebnisses. Bei `type: "shortCircuit"` MUSS er `AND`, `XOR`, `NOT_AND`, `NOT_XOR` oder `undefined` sein: `OR`, `NOT_OR` und `DELEGATED` DÜRFEN NICHT short-circuiten (siehe [Kapitel 3.6.2](../03-data-model/3-6-operators.md#362-or-und-not_or) und [Kapitel 3.6.4](../03-data-model/3-6-operators.md#364-der-operator-delegated)) |
| `mode`     | Enum   | Auswertungsmodus, unter dem der Knoten übersprungen wurde: `optimized`, `complete`                                                                                                                                                                                                                                                                                                                     |

Zusätzliche Felder sind NICHT erlaubt.

Das Feld `type` MUSS einen der folgenden Werte haben.

| Wert                      | Ursache                                                  |
| ------------------------- | -------------------------------------------------------- |
| `shortCircuit`            | Short-Circuit-Evaluation durch den Parent-Operator       |
| `manualSkip`              | Ein Benutzer hat den Knoten bewusst übersprungen         |
| `conditionalDeactivation` | Der Knoten wurde aufgrund von Vorbedingungen deaktiviert |

_Knoten 1.5 – shortCircuit: das AND des Parent-Nodes ist durch Knoten 1.4 bereits false_

```jsonc
"1.5": {
  "lexId": "5",
  "status": "ignored",
  "reason": {
    "type": "shortCircuit",
    "trigger": "1.4",
    "operator": "AND",
    "mode": "optimized"
  }
}
```

**Wichtig:** `ignored` bedeutet "bewusst nicht geprüft" — nicht "Fehler bei der Prüfung". Ein
`ignored`-Knoten fließt NICHT in die Operator-Berechnung des Parent-Nodes ein.
