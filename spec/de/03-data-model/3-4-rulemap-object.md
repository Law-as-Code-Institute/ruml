<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 3.4 Rulemap-Objekt

Die Rulemap ist das Kernstück einer RUML-Datei und enthält die hierarchische Regellogik in einer
flachen Map-Struktur mit `LexID`-Referenzen.

### 3.4.1 Pflichtfelder

| Feld    | Typ      | Beschreibung                                                                                                                                                                                                                                                                        |
| ------- | -------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `nodes` | `Object` | **MUSS** alle Knoten der Rulemap als flache Map enthalten. Keys sind die LexIDs als Strings (z.B. `"1"`, `"42"`). Values **MÜSSEN** Node-Objekte gemäß [3.5](3-5-node-object.md) sein ([`NODE-02`](../08-validation/index.md#rule-node-02)). **MUSS** einen Eintrag mit Key `"1"` enthalten (Root-Node) ([`FMT-08`](../08-validation/index.md#rule-fmt-08)). |

**Strukturbeispiel:**

```jsonc
"rulemap": {
  "nodes": {
    "1": {
      "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
      "operator": "AND",
      "label": "Credit worthiness check",
      "children": ["2", "3"]
    },
    "2": {
      "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
      "label": "Income verification"
    },
    "3": {
      "id": "95f566ad-b37c-4a18-b004-e83274d0fe83",
      "label": "Credit score check"
    }
  }
}
```

**Hinweise zur Struktur:**

- Der Key IST die LexID — ein separates `lexId`-Feld im Node-Objekt ist NICHT erforderlich
- Direkter Lookup via `children`-Referenzen: `nodes[String(childLexId)]`

### 3.4.2 Umfang des Rulemap-Objekts

Das `rulemap`-Objekt ist die **Strukturebene** — es trägt den Entscheidungsbaum und sonst nichts.
Beschreibende Informationen über das Dokument (`title`, `description`, Autoren, Status,
Identifikatoren …) liegen im `metadata`-Objekt (siehe [Kapitel 3.3](3-3-metadata-object.md));
Erweiterungen liegen in `capabilities` (siehe [Kapitel 4](../04-capabilities/index.md)). `rulemap`
hat daher derzeit genau ein Feld, `nodes`; das Objekt bleibt erhalten (statt `nodes` auf die
Root-Ebene zu heben), um diese Trennung von Struktur, Metadaten und Capabilities explizit zu halten
und einen Ort für künftige baum-weite Einstellungen zu bieten.
