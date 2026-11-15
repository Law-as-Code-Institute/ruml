<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 6.5 Verschachtelung

Modulare Knoten **DÜRFEN** andere modulare Knoten als Kinder haben. Dies ermöglicht die Komposition
komplexer, wiederverwendbarer Regelstrukturen. ([`MOD-06`](../08-validation/index.md#rule-mod-06))

---

### Grundregeln

- Keine Beschränkung der Verschachtelungstiefe
- Jeder modulare Knoten **DARF** unabhängig vom übergeordneten modularen Knoten an anderen Stellen
  referenziert werden ([`MOD-06`](../08-validation/index.md#rule-mod-06))

---

### Beispiel

**Struktur:**

```
Root (AND, lexId: 1)
├── Hauptprüfung (AND, lexId: 10, modular) ──────────────┐
│   ├── Identitätsprüfung (Leaf, lexId: 11)              │
│   └── Bonitätsprüfung (AND, lexId: 20, modular) ───┐   │
│       ├── Einkommensprüfung (Leaf, lexId: 21)      │   │
│       └── Schufa-Prüfung (Leaf, lexId: 22)         │   │
├── Alternative (OR, lexId: 2)                       │   │
│   └── [Referenz auf lexId: 10] ────────────────────│───┘
└── Schnellprüfung (OR, lexId: 3)                    │
    └── [Referenz auf lexId: 20] ────────────────────┘
```

**Erläuterung:**

- `lexId: 10` (Hauptprüfung) wird 2× referenziert: von Root und von "Alternative"
- `lexId: 20` (Bonitätsprüfung) wird 3× erreicht: 2× als Kind von lexId: 10, plus 1× direkt von
  "Schnellprüfung"

---

**RUML-Datei:**

```jsonc
"rulemap": {
  "nodes": {
    "1": {
      "id": "b6620b3c-4279-4a45-9115-c8bb2032d868",
      "operator": "AND",
      "label": "Root",
      "children": ["10", "2", "3"]
    },
    "2": {
      "id": "551ff73a-66ce-48ca-b889-84bc63ce864c",
      "operator": "OR",
      "label": "Alternative",
      "children": ["10"]
    },
    "3": {
      "id": "42d9431d-b7db-404f-bdf9-7ecdde505cce",
      "operator": "OR",
      "label": "Schnellprüfung",
      "children": ["20"]
    },
    "10": {
      "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
      "modular": true,
      "operator": "AND",
      "label": "Hauptprüfung",
      "children": ["11", "20"]
    },
    "11": {
      "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
      "label": "Identitätsprüfung",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_identity_verified = true"
          }
        }
      ]
    },
    "20": {
      "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
      "modular": true,
      "operator": "AND",
      "label": "Bonitätsprüfung",
      "children": ["21", "22"]
    },
    "21": {
      "id": "52820488-2849-4487-842b-952dc3ba301d",
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
    "22": {
      "id": "48b34df4-06bb-4dc2-aeb7-807a146760f4",
      "label": "Schufa-Prüfung",
      "capabilities": [
        {
          "id": "ruml:query",
          "payload": {
            "expression": "dp_schufa >= 600"
          }
        }
      ]
    }
  }
}
```

---

### Auswertungsergebnisse

Bei der Auswertung kann jede Instanz eines verschachtelten modularen Knotens ein unterschiedliches
Ergebnis haben. Die Ergebnisse werden nach Pfad indiziert (siehe
[Kapitel 5.1.2](../05-result-format/5-1-result-model.md)):

```jsonc
"results": {
  "1.1.2": {
    "lexId": "20",
    "status": "true",
    "reason": "AND: alle Kinder true"
  },
  "1.2.1.2": {
    "lexId": "20",
    "status": "true",
    "reason": "AND: alle Kinder true"
  },
  "1.3.1": {
    "lexId": "20",
    "status": "false",
    "reason": "AND: Einkommensprüfung false"
  }
}
```

Im Beispiel hat die Bonitätsprüfung über die "Schnellprüfung" (Pfad `1.3.1`) ein anderes Ergebnis
als über die "Hauptprüfung" – möglicherweise weil unterschiedliche Datenpunkte im Kontext verfügbar
waren.
