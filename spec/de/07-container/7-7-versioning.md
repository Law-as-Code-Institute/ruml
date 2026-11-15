<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.7 Versionierung

### Einzelversion (Standard)

Im Standardfall enthält ein Container eine einzelne Version einer Datei. Versionierung erfolgt über
die Metadaten der RUML-Datei selbst:

- `metadata.version` — die Versionsnummer
- `metadata.replaces` — UUID der ersetzten Version
- `metadata.replacedBy` — UUID der Nachfolgeversion

Jede Version ist ein eigener Container — unabhängig signierbar und distributierbar.

### Mehrere Versionen (Archiv)

Ein Container DARF mehrere Versionen derselben Datei enthalten. Dies ist nützlich für:

- **Audit-Archivierung:** Vollständige Versionshistorie in einer Datei
- **Vergleich:** Alte und neue Version nebeneinander
- **Übergangszeiträume:** Aktuelle und vorherige Version während einer Migration

Mehrere Versionen werden über Unterverzeichnisse organisiert:

```
archiv.rumlc (ZIP)
├── versions/
│   ├── 1.0/
│   │   └── rulemap.json
│   ├── 2.0/
│   │   └── rulemap.json
│   └── 2.1-draft/
│       └── rulemap.json
├── signatures/
│   └── versions/2.0/rulemap.json.sig
└── manifest.json
```

Das Manifest deklariert jede Version als separate Datei:

```jsonc
{
  "$format": "RUML-Container",
  "$specVersion": "1.0",
  "created": "2026-03-15T10:30:00+01:00",
  "files": {
    "versions/1.0/rulemap.json": {
      "type": "ruml",
      "hash": {
        "algorithm": "sha3-256",
        "value": "1b3d5f7a9c1e3b5d7f9a1c3e5b7d9f1a3c5e7b9d1f3a5c7e9b1d3f5a7c9e1b3d"
      }
    },
    "versions/2.0/rulemap.json": {
      "type": "ruml",
      "hash": {
        "algorithm": "sha3-256",
        "value": "4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
      },
      "signature": {
        "path": "signatures/versions/2.0/rulemap.json.sig",
        "format": "jws-detached"
      }
    },
    "versions/2.1-draft/rulemap.json": {
      "type": "ruml"
    }
  }
}
```

Jede Version DARF unabhängig gehasht, signiert und verschlüsselt werden. Eine archivierte Version
ohne Signatur ist gültig — nur die aktuelle, rechtskräftige Version benötigt typischerweise eine
Signatur.

### Versionskennzeichnung

Die Versionskennung im Verzeichnisnamen (z.B. `1.0`, `2.0`, `2.1-draft`) ist ausschließlich ein
menschenlesbarer Bezeichner. Parser DÜRFEN Verzeichnisnamen NICHT als Quelle für
Versionsinformationen verwenden. Die normative Version wird ausschließlich durch `metadata.version`
innerhalb der jeweiligen RUML-Datei festgelegt. Der Verzeichnisname SOLLTE aus Lesbarkeitsgründen
mit `metadata.version` übereinstimmen, dies wird jedoch nicht erzwungen.
