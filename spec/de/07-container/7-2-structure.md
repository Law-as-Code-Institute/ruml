<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.2 Container-Struktur

### ZIP-Layout

Ein RUML-Container ist ein ZIP-Archiv mit folgender Struktur:

```
dokument.rumlc (ZIP)
├── rulemap.json                          # RUML-Datei (Bare-JSON)
├── ext/                                  # Sidecar-Dateien (optional)
│   └── bank.json
├── results/                              # Ergebnisdateien (optional)
│   └── 2026-03-15.json
├── assets/                               # Referenzierte Dateien (optional)
│   ├── estg-2024.pdf
│   └── bgh-urteil.pdf
├── signatures/                           # Signatur-Dateien (optional)
│   ├── rulemap.json.sig
│   └── ext/bank.json.sig
├── encrypted/                            # Verschlüsselte Dateien (optional)
│   └── results/2026-03-15.json.enc
└── manifest.json                         # Container-Index (MUSS vorhanden sein)
```

### Pflichtdateien

Ein RUML-Container MUSS genau eine `manifest.json` im Root-Verzeichnis enthalten.

Ein RUML-Container MUSS mindestens eine Inhaltsdatei (Typ `ruml`, `ruml-ext` oder `ruml-result`)
enthalten.

### Verzeichniskonventionen

| Verzeichnis   | Inhalt                                                                      |
| ------------- | --------------------------------------------------------------------------- |
| Root (`/`)    | RUML-Dateien und Manifest                                                   |
| `ext/`        | RUML-EXT Sidecar-Dateien                                                    |
| `results/`    | RUML-Result-Dateien                                                         |
| `assets/`     | Referenzierte Dateien (PDFs, Texte, Bilder etc.)                            |
| `signatures/` | Signatur-Dateien — Pfadstruktur spiegelt die Quelldatei                     |
| `encrypted/`  | Verschlüsselte Versionen von Dateien — Pfadstruktur spiegelt die Quelldatei |

Die Pfadstruktur in `signatures/` und `encrypted/` MUSS die Pfadstruktur der Quelldatei spiegeln.
Beispiel: Die Signatur für `ext/bank.json` liegt unter `signatures/ext/bank.json.sig`.

### Dateinamen-Konventionen

| Schicht         | Suffix | Beispiel                                |
| --------------- | ------ | --------------------------------------- |
| Signatur        | `.sig` | `signatures/rulemap.json.sig`           |
| Verschlüsselung | `.enc` | `encrypted/results/2026-03-15.json.enc` |

### manifest.json

Das Manifest ist der zentrale Index des Containers. Es beschreibt alle Inhaltsdateien und ihre
Integritätsschichten.

```jsonc
{
  "$format": "RUML-Container",
  "$specVersion": "1.0",
  "created": "2026-03-15T10:30:00+01:00",
  "files": {
    "rulemap.json": {
      "type": "ruml",
      "hash": {
        "algorithm": "sha3-256",
        "value": "4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
      },
      "signature": {
        "path": "signatures/rulemap.json.sig",
        "format": "jws-detached"
      }
    },
    "ext/bank.json": {
      "type": "ruml-ext",
      "hash": {
        "algorithm": "sha3-256",
        "value": "9a1c0d5e7b3f48261e0a9c7d5b3f1e2a4c6d8f0b2a4c6e8f1a3b5c7d9e0f1a2b"
      },
      "signature": {
        "path": "signatures/ext/bank.json.sig",
        "format": "cms-detached"
      }
    },
    "results/2026-03-15.json": {
      "type": "ruml-result",
      "hash": {
        "algorithm": "sha3-256",
        "value": "c2f4a6b8d0e1f3a5c7b9d1e3f5a7c9b1d3e5f7a9c1b3d5e7f9a1c3b5d7e9f1a3"
      },
      "encryption": {
        "path": "encrypted/results/2026-03-15.json.enc",
        "format": "jwe",
        "algorithm": "RSA-OAEP-256"
      }
    },
    "assets/estg-2024.pdf": {
      "type": "asset",
      "hash": {
        "algorithm": "sha3-256",
        "value": "07b5d3f1e9c7a5b3d1f9e7c5a3b1d9f7e5c3a1b9d7f5e3c1a9b7d5f3e1c9a7b5"
      }
    },
    "manifest.json": {
      "hash": {
        "algorithm": "sha3-256",
        "value": "5d8e2b1f4a7c0e3b6d9f2a5c8e1b4d7f0a3c6e9b2d5f8a1c4e7b0d3f6a9c2e5b"
      },
      "signature": {
        "path": "signatures/manifest.json.sig",
        "format": "jws-detached"
      }
    }
  }
}
```

#### Manifest-Pflichtfelder

| Feld           | Typ      | Beschreibung                                                                                                                                                                                                                                                              |
| -------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$format`      | String   | MUSS den Wert `"RUML-Container"` haben                                                                                                                                                                                                                                    |
| `$specVersion` | String   | MUSS die Spec-Version angeben ([2.3](../02-file-format-basics/2-3-versioning.md#das-feld-specversion))                                                                                                                                                                    |
| `created`      | DateTime | MUSS den Erstellungszeitpunkt des Containers angeben                                                                                                                                                                                                                      |
| `files`        | Object   | MUSS einen Eintrag pro Inhaltsdatei enthalten. Schlüssel ist der relative Pfad der Datei; bei einer verschlüsselten Datei der Pfad ihres Klartexts. Signatur-Dateien und verschlüsselte Dateien werden aus diesen Einträgen referenziert und haben keinen eigenen Eintrag |

#### Felder pro Datei-Eintrag

| Feld         | Typ    | Pflicht                          | Beschreibung                                                                                                                                                                                   |
| ------------ | ------ | -------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`       | String | MUSS (außer für `manifest.json`) | Dateityp: `ruml`, `ruml-ext`, `ruml-result` oder `asset`                                                                                                                                       |
| `uri`        | String | DARF                             | Die URI der unveränderlichen RUML-Version, die diese Datei repräsentiert (siehe [Gebündelte RUML-Dateien](#gebündelte-ruml-dateien)). DARF NICHT angegeben sein, wenn `type` nicht `ruml` ist. |
| `hash`       | Object | DARF                             | Hash-Information (siehe [7.3](7-3-hashing.md))                                                                                                                                                 |
| `signature`  | Object | DARF                             | Signatur-Information (siehe [7.4](7-4-signatures.md))                                                                                                                                          |
| `encryption` | Object | DARF                             | Verschlüsselungs-Information (siehe [7.5](7-5-encryption.md))                                                                                                                                  |

#### Manifest-Selbstreferenz

Das Manifest DARF sich selbst im `files`-Objekt referenzieren. Dies ermöglicht es, das Manifest
selbst zu hashen und zu signieren. Wird das Manifest signiert, entsteht eine Vertrauenskette über
den gesamten Container-Inhalt: Die Manifest-Signatur schützt die Manifest-Inhalte, die wiederum die
Hashes aller anderen Dateien enthalten.

Wenn eine Inhaltsdatei im Container eine `signature` trägt, SOLLTE das Manifest selbst signiert
sein. Ein unsigniertes Manifest kann seine Hashes nicht vor Substitution schützen: Eine Partei mit
Schreibzugriff auf den Container kann eine Datei und den zugehörigen Hash im Manifest ersetzen, ohne
dass dies erkannt wird. Nur eine Manifest-Signatur — die den privaten Schlüssel erfordert —
verhindert diesen Angriff.

Bei der Berechnung des Manifest-Hashes MUSS der `manifest.json`-Eintrag im `files`-Objekt
ausgenommen werden — er existiert zu diesem Zeitpunkt noch nicht. Der Hash wird über die
kanonisierte (RFC 8785) Version des Manifests berechnet, in der der Schlüssel `"manifest.json"` aus
dem `files`-Objekt entfernt ist.

### Gebündelte RUML-Dateien

Ein Container DARF mehrere RUML-Dateien enthalten: eine Rulemap zusammen mit den RUML-Dateien, in
die ihre Knotenanker zeigen (zum Beispiel das Gesetz, das sie umsetzt, siehe
[Kapitel 4.15](../04-capabilities/4-15-ruml-tree-reference.md#bündelung-für-den-export)). Jede
gebündelte Datei, die Ziel von Knotenankern ist, MUSS die Versions-URI, die sie repräsentiert, im
Feld `uri` ihres Manifest-Eintrags haben:

```json
"files": {
  "rulemap.json": { "type": "ruml" },
  "gmbhg.json": {
    "type": "ruml",
    "uri": "https://rulemapping.org/rulemapping/gmbhg:2025-01-01"
  }
}
```

Innerhalb eines Containers MUSS jede `uri` eindeutig sein. Ein Parser löst einen Knotenanker gegen
die gebündelte Datei auf, deren `uri` der RUML-URI des Ankers entspricht, bevor er sie anderweitig
abruft.

### Validierung

Beim Öffnen eines RUML-Containers MUSS ein Parser:

1. Prüfen, ob `manifest.json` vorhanden ist und gültiges JSON enthält
2. Prüfen, ob mindestens eine Inhaltsdatei (Typ `ruml`, `ruml-ext` oder `ruml-result`) vorhanden ist
3. Prüfen, ob jede Datei, die das Manifest aufführt oder referenziert, im Container existiert: jede
   Inhaltsdatei, oder ihre verschlüsselte Version, wenn der Eintrag `encryption` hat, und jede
   Signatur-Datei

Ein Parser DARF eine Datei, die das Manifest weder aufführt noch referenziert, NICHT verarbeiten und
SOLLTE für sie eine Warnung ausgeben.

### Größenbeschränkungen für Container

Ein Container SOLLTE 1 GB unkomprimierte Gesamtgröße NICHT überschreiten. Parser DÜRFEN niedrigere
Grenzwerte erzwingen; jeder erzwungene Grenzwert MUSS dokumentiert sein.
