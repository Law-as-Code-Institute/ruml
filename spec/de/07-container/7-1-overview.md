<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.1 Überblick

### Dual-Mode-Konzept

RUML-Dateien existieren in zwei Modi:

| Modus         | Format | Dateiendung                          | Zweck                                                    |
| ------------- | ------ | ------------------------------------ | -------------------------------------------------------- |
| **Bare**      | JSON   | `.ruml`, `.ruml-ext`, `.ruml-result` | Entwicklung, Entwurf, Einbettung in andere Systeme       |
| **Container** | ZIP    | `.rumlc`                             | Distribution, Archivierung, rechtlich bindende Dokumente |

Container-Dateien verwenden die Endung `.rumlc`. Bare-Dateien behalten ihre ursprünglichen Endungen
(`.ruml`, `.ruml-ext`, `.ruml-result`).

**Bare-Modus:** Die Datei ist reines JSON ohne Integritätsschichten. Für Entwicklung und Entwurf —
kein Hash, keine Signatur, keine Verschlüsselung.

**Container-Modus:** Die Datei ist ein ZIP-Archiv, das das JSON-Dokument zusammen mit Hash-,
Signatur- und Verschlüsselungsdaten enthält. Jede Integritätsschicht ist optional — ein Container
DARF jede Kombination davon enthalten, etwa allein Hashes, allein Signaturen oder alle drei
Schichten.

### Dateitypen im Container

Ein Container DARF beliebige Kombinationen folgender Dateitypen enthalten:

| Typ         | Beschreibung                           | Manifest-Typ  |
| ----------- | -------------------------------------- | ------------- |
| RUML        | Rulemap (Kernstruktur)                 | `ruml`        |
| RUML-EXT    | Sidecar-Datei mit Capability-Daten     | `ruml-ext`    |
| RUML-Result | Auswertungsergebnis                    | `ruml-result` |
| Asset       | Beliebige Datei (PDF, Text, Bild etc.) | `asset`       |

Es gibt keine Einschränkung, welche Kombinationen erlaubt sind:

- Ein Container mit nur einer Rulemap ist gültig
- Ein Container mit nur einer EXT-Datei ist gültig (die Basis-Rulemap wird über `$base`
  referenziert)
- Ein Container mit Rulemap + mehreren Result-Dateien ist gültig
- Ein Container mit mehreren Versionen derselben Rulemap ist gültig

### Designprinzipien

1. **Schichten sind unabhängig:** Jede Datei im Container DARF unabhängig gehasht, signiert und
   verschlüsselt werden — einschließlich des Manifests selbst.
2. **Formate sind deklarativ:** Das Manifest deklariert, welche Algorithmen und Formate verwendet
   werden. Der Container schreibt keine spezifische Kryptographie-Implementierung vor.
3. **Bare ist immer gültig:** Eine Bare-JSON-Datei ist eine vollwertige RUML-Datei. Der Container
   fügt Schichten hinzu, ändert aber nichts am Inhalt.
