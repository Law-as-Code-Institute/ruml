<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 2.5 Identifikator-System

### LexID (Lexical Identifier)

Primärer numerischer Identifikator innerhalb einer RUML-Datei:

- **Format**: Positive Ganzzahl, als JSON-String kodiert (z. B. `"12"`)
- **Pattern**: `^[1-9][0-9]*$` ([`FMT-11`](../08-validation/index.md#rule-fmt-11))
- **Start**: MUSS bei 1 beginnen (Root-Node) ([`FMT-08`](../08-validation/index.md#rule-fmt-08))
- **Eindeutigkeit**: MUSS innerhalb der Datei eindeutig sein ([`FMT-12`](../08-validation/index.md#rule-fmt-12))
- **Wiederverwendung**: Ein modularer Knoten (siehe
  [6.2](../06-modular-nodes/6-2-implementation.md#definition-modularer-knoten)) existiert einmal in
  `nodes`; seine LexID bleibt eindeutig

LexIDs sind überall Strings — als Schlüssel in `rulemap.nodes` und in `children`. Die Knoten-Map ist
ein JSON-Objekt, ihre Schlüssel sind damit systembedingt Strings; dieselbe Form für Referenzen hält
Referenz und Schlüssel direkt vergleichbar.

### UUID (Universally Unique Identifier)

Globaler eindeutiger Identifikator für externe Referenzierung:

- **Format**: UUID v4 (zufällig generiert)
- **Pattern**: `^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$`
  ([`FMT-10`](../08-validation/index.md#rule-fmt-10))
- **Standard**: RFC 4122 Version 4
- **Entropie**: 122 Bit kryptografisch sicher
- **Generierung**: SOLLTE mit Standard-UUID-Bibliothek erfolgen (z.B. `uuid` npm-Paket, v4-Funktion)

**Beispiele gültiger UUIDs:**

```
e7c9a3f1-4b82-4d15-9a6c-3d8f2b01e794
a3f5c9e7-2d48-4b71-8f6a-1c3d0b92e475
b8d2e4f6-0a73-4c85-9b1e-5f7c2a34d098
c1e3a5f7-6b90-4d42-8c4a-7f2e3b01d563
```

## Konformitätstests

- [2.5 Identifier System](../../../tests/02-file-format-basics/2-5-identifier-system.test.yaml)
