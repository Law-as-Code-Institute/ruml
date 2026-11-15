<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.5 Verschlüsselungs-Schicht

### Zweck

Verschlüsselung bietet **Vertraulichkeit** — sie beantwortet die Frage: _„Wer darf diese Datei
lesen?"_

Die Verschlüsselung im RUML-Container arbeitet auf **Dateiebene**: Eine vollständige Datei wird
verschlüsselt und als `.enc`-Datei im `encrypted/`-Verzeichnis abgelegt. Die Klartextdatei wird aus
dem Container entfernt.

Für feldbasierte Verschlüsselung innerhalb einer Datei (z.B. einzelne Capability-Payloads) ist die
jeweilige Capability selbst verantwortlich — nicht der Container.

### Verschlüsselte Dateien

Wenn eine Datei verschlüsselt ist, existiert sie nicht mehr als Klartext im Container. Stattdessen
liegt die verschlüsselte Version im `encrypted/`-Verzeichnis:

```
Container OHNE Verschlüsselung:
├── results/2026-03-15.json           ← Klartext

Container MIT Verschlüsselung:
├── encrypted/results/2026-03-15.json.enc   ← verschlüsselt
```

Die Klartextdatei (`results/2026-03-15.json`) DARF NICHT gleichzeitig mit ihrer verschlüsselten
Version im Container existieren.

### Verschlüsselungs-Formate

Diese Spezifikation schreibt kein Verschlüsselungs-Format vor. Das Manifest nennt das Format im Feld
`format`; welche Formate ein Parser unterstützt, entscheidet die Implementierung.

| Kennung         | Format              | Standard |
| --------------- | ------------------- | -------- |
| `jwe`           | JSON Web Encryption | RFC 7516 |
| `cms-enveloped` | CMS-`EnvelopedData` | RFC 5652 |

Diese beiden Kennungen sind für die genannten Formate reserviert. Jedes andere Format MUSS eine
Kennung in Reverse-Domain-Form verwenden.

Wie Schlüssel beschafft und verteilt werden, liegt außerhalb dieser Spezifikation.

### Manifest-Referenz

Die Verschlüsselung wird im Manifest wie folgt deklariert:

```jsonc
"encryption": {
  "path": "encrypted/results/2026-03-15.json.enc",
  "format": "jwe",
  "algorithm": "RSA-OAEP-256"
}
```

| Feld        | Typ    | Beschreibung                                                          |
| ----------- | ------ | --------------------------------------------------------------------- |
| `path`      | String | MUSS den Pfad zur verschlüsselten Datei im Container angeben          |
| `format`    | String | MUSS das Verschlüsselungs-Format angeben                              |
| `algorithm` | String | DARF den verwendeten Algorithmus nennen, wie das Format ihn definiert |

### Reihenfolge: Signatur vor Verschlüsselung

Wenn eine Datei sowohl signiert als auch verschlüsselt ist, MUSS die Signatur über den **Klartext**
erstellt werden — nicht über die verschlüsselte Version. Die Verarbeitungsreihenfolge ist:

**Erstellen:** Hash → Signatur → Verschlüsselung (auf Klartext) **Verifizieren:** Entschlüsselung →
Signaturprüfung → Hash-Prüfung (auf Klartext)

Dies bedeutet: Hash und Signatur beziehen sich immer auf den Klartext. Die Signatur-Datei liegt im
`signatures/`-Verzeichnis und bezieht sich auf die logische Datei (z.B. `results/2026-03-15.json`),
nicht auf die verschlüsselte Datei.

### Validierung

Beim Zugriff auf eine verschlüsselte Datei MUSS ein Parser:

1. Prüfen, ob ein passender Entschlüsselungsschlüssel verfügbar ist
2. Die `.enc`-Datei entschlüsseln
3. Die entschlüsselte Datei zur weiteren Verarbeitung bereitstellen (Signaturprüfung, Hash-Prüfung,
   Parsing)

Ein Parser, der das Format nicht unterstützt oder keinen passenden Schlüssel hat, MUSS die Datei als
nicht lesbar melden. Die übrigen Dateien im Container MÜSSEN weiterhin verarbeitbar sein — eine
einzelne nicht-entschlüsselbare Datei DARF NICHT den gesamten Container unbrauchbar machen.
