<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 6.2 Implementierung

---

### Definition modularer Knoten

Ein Knoten ist **modular**, wenn er mehrfach referenziert wird: Seine `lexId` kommt mehr als einmal
in den `children`-Arrays der Rulemap vor, unter verschiedenen Parent-Nodes oder zweimal unter
demselben. Die Selbstreferenz eines rekursiven Knotens zählt als eine dieser Referenzen (siehe
[6.4](6-4-recursion.md)).

- Ein modularer Knoten existiert genau einmal im `nodes`-Objekt
- Ein modularer Knoten **MUSS** `modular: true` haben ([`MOD-01`](../08-validation/index.md#rule-mod-01))
- Ein Knoten, der nicht modular ist, **SOLLTE** `modular: true` **NICHT** haben

---

**Identifikation der Kinder:**

- Ob ein Knoten Teil eines modularen Teilbaums ist, ergibt sich aus der Baumstruktur und wird zur
  Laufzeit ermittelt

---

**Beispiel Mehrfach-Referenzierung:**

```jsonc
"rulemap": {
  "nodes": {
    "1": {
      "id": "b6620b3c-4279-4a45-9115-c8bb2032d868",
      "operator": "AND",
      "label": "Hauptprüfung",
      "children": ["2", "8", "10"]
    },
    "2": {
      "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
      "label": "Antragsteller volljährig",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_age >= 18"
          }
        }
      ]
    },
    "8": {
      "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
      "modular": true,
      "operator": "AND",
      "label": "Standardprüfung Bonität",
      "children": ["9", "11"]
    },
    "9": {
      "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
      "label": "Einkommensprüfung",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_income > 30000"
          }
        }
      ]
    },
    "10": {
      "id": "42d9431d-b7db-404f-bdf9-7ecdde505cce",
      "operator": "OR",
      "label": "Alternative Prüfungen",
      "children": ["8", "12"]
    },
    "11": {
      "id": "52820488-2849-4487-842b-952dc3ba301d",
      "label": "Schufa-Score",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_schufa >= 600"
          }
        }
      ]
    },
    "12": {
      "id": "48b34df4-06bb-4dc2-aeb7-807a146760f4",
      "label": "Bürgschaft vorhanden",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_guarantor = true"
          }
        }
      ]
    }
  }
}
```

---

**Hinweis zum Beispiel:** Die `lexId: 8` (Standardprüfung Bonität) wird zweimal referenziert –
einmal von Knoten 1 (`children: [2, 8, 10]`) und einmal von Knoten 10 (`children: [8, 12]`). Der
Knoten selbst existiert nur einmal im `nodes`-Objekt.

---

**Fehlendes** `modular`-Flag bei Mehrfach-Referenzierung:

_Ungültig_

```jsonc
"nodes": {
  "1": {
    "id": "b6620b3c-4279-4a45-9115-c8bb2032d868",
    "operator": "AND",
    "label": "Antrag",
    "children": ["2", "3"]
  },
  "2": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "operator": "AND",
    "label": "Antrag A",
    "children": ["5"]
  },
  "3": {
    "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
    "operator": "AND",
    "label": "Antrag B",
    "children": ["5"]
  },
  "5": {
    // 'modular' ist nicht gesetzt
    "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
    "label": "Mehrfach referenziert"
  }
}
```

---

**Hinweis zu Textankern bei modularen Knoten:**

Die Anker der Capability `ruml:text-reference` auf Knotenebene (siehe
[Kapitel 4.12](../04-capabilities/4-12-ruml-text-reference.md#node-level-anker)) verhalten sich bei
modularen Knoten anders als die pfadabhängige Auswertung: Sie sind eine Eigenschaft der
**Knotendefinition**, nicht der Instanziierung.

Das bedeutet: Ein modularer Knoten markiert mit seinem `represents`-Anker für alle seine
Verwendungsstellen dieselbe Norm. Wenn derselbe Prüfungsknoten an zwei Positionen im Regelbaum
eingesetzt wird, gelten seine Anker an beiden Stellen gleich – sie benennen immer denselben
Paragraphen, Absatz oder Satz des Ausgangstextes.

**Begründung:** Da ein modularer Knoten konzeptionell eine Regelprüfung darstellt, die an mehreren
Stellen wiederverwendet wird, basiert er stets auf einer Rechtsgrundlage. Unterschiedliche Anker je
Instanz würden dem Konzept der modularen Wiederverwendung widersprechen.

## Konformitätstests

- [6.2 Implementation](../../../tests/06-modular-nodes/6-2-implementation.test.yaml)
