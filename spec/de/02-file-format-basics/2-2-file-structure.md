<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 2.2 Dateistruktur Übersicht

### Root-Objekt Struktur

Jede RUML-Datei MUSS ein JSON-Objekt als Root-Element haben ([`FMT-02`](../08-validation/index.md#rule-fmt-02)):

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [/* ... */],
  "metadata": {/* ... */},
  "rulemap": {/* ... */}
}
```

### Format-Identifikation

- Das Feld `$format` MUSS einen der folgenden Werte haben:
  - `"RUML"` — reguläre Inhaltsdatei (diese Spezifikation)
  - `"RUML-Result"` — separate Auswertungsergebnisdatei (siehe
    [Kapitel 5.1](../05-result-format/5-1-result-model.md))
  - `"RUML-EXT"` — Capability-Erweiterungsoverlay (Sidecar-Datei); hat eine abweichende
    Root-Struktur ohne `metadata` und `rulemap` (siehe
    [Kapitel 4.5](../04-capabilities/4-5-ruml-ext.md))
- Das Feld `$specVersion` MUSS die Formatversion angeben
  ([2.3](./2-3-versioning.md#das-feld-specversion))
- Diese Felder MÜSSEN die ersten beiden Felder im Root-Objekt sein ([`FMT-05`](../08-validation/index.md#rule-fmt-05))
- Bei `"RUML-Result"` MUSS zusätzlich ein `rumlReference`-Objekt vorhanden sein (siehe
  [Kapitel 5.1](../05-result-format/5-1-result-model.md))

### Pflichtfelder im Root-Objekt

| **Feld**       | **Typ** | **Beschreibung**                                                                                 |
| -------------- | ------- | ------------------------------------------------------------------------------------------------ |
| `$format`      | String  | MUSS `"RUML"` sein ([`FMT-03`](../08-validation/index.md#rule-fmt-03))                                                               |
| `$specVersion` | String  | MUSS die Formatversion angeben ([2.3](./2-3-versioning.md#das-feld-specversion)) ([`FMT-04`](../08-validation/index.md#rule-fmt-04)) |
| `metadata`     | Object  | MUSS die in Kapitel 3.3 definierten Metadaten enthalten ([`FMT-06`](../08-validation/index.md#rule-fmt-06))                          |
| `rulemap`      | Object  | MUSS die in Kapitel 3.4 definierte Rulemap-Struktur enthalten ([`FMT-06`](../08-validation/index.md#rule-fmt-06))                    |

### Optionale Felder im Root-Objekt

| **Feld**       | **Typ** | **Beschreibung**                                                                                                                                                                                                                                    |
| -------------- | ------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `capabilities` | Array   | DARF die Capabilities deklarieren, die diese Datei verwendet, als Liste von Einträgen; ihre Reihenfolge ist nicht signifikant. Jeder Eintrag führt seine Daten in seinem `payload` (siehe [Kapitel 4](../04-capabilities/index.md)) ([`FMT-06`](../08-validation/index.md#rule-fmt-06)) |

Das Root-Objekt DARF KEINE anderen Felder als diese haben ([`FMT-07`](../08-validation/index.md#rule-fmt-07)).

### Minimale gültige Datei

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.0.0",
    "created": "2024-01-01T00:00:00Z",
    "modified": "2024-01-01T00:00:00Z",
    "status": "draft"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "label": "Root"
      }
    }
  }
}
```

**Hinweise:**

- Das `nodes`-Objekt ist das einzige Pflichtfeld in der `rulemap`
- Der Root-Node **MUSS** den Key `"1"` im `nodes`-Objekt haben (LexID 1) ([`FMT-08`](../08-validation/index.md#rule-fmt-08))
- Jeder Node **MUSS** eine `id` haben (UUID v4) ([`NODE-01`](../08-validation/index.md#rule-node-01))
- Integritätssicherung (Hash, Signatur) erfolgt auf Container-Ebene (siehe
  [Kapitel 7](../07-container/index.md))

### RUML-Result-Format

Für die separate Speicherung von Auswertungsergebnissen wird das RUML-Result-Format verwendet:

- **Dateiendung**: `.ruml-result`
- **Format-Identifikation**: `$format` MUSS den Wert `"RUML-Result"` haben
- **Struktur**: Siehe [Kapitel 5.1](../05-result-format/5-1-result-model.md)

Das RUML-Result-Format ermöglicht die Trennung von Regelstruktur und Auswertungsergebnissen. Dies
ist besonders geeignet für Massenverfahren, Aktensysteme und Langzeitarchivierung.

```jsonc
{
  "$format": "RUML-Result",
  "$specVersion": "1.0",
  "rumlReference": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
  },
  "evaluation": {/* ... */}
}
```

## Konformitätstests

- [2.2 File Structure Overview](../../../tests/02-file-format-basics/2-2-file-structure.test.yaml)
