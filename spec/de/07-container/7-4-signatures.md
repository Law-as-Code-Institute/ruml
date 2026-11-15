<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.4 Signatur-Schicht

### Zweck

Digitale Signaturen bieten **Authentizität** und **Nicht-Abstreitbarkeit** — sie beantworten die
Fragen: _„Wer hat diese Datei veröffentlicht?"_ und _„Wurde sie seit der Signierung verändert?"_

Im Gegensatz zum Hash (reine Integritätsprüfung) erfordert eine Signatur den privaten Schlüssel des
Signierenden. Eine Signatur kann nicht ohne Weiteres neu erstellt werden — sie bindet eine bestimmte
Identität an einen bestimmten Inhalt.

### Detached Signatures

Signaturen im RUML-Container sind **immer detached** — die Signatur-Datei enthält nur die Signatur,
nicht den signierten Inhalt. Der signierte Inhalt liegt als separate Datei im Container.

```
rulemap.json                          ← signierter Inhalt
signatures/rulemap.json.sig           ← Signatur (ohne Inhalt)
```

Zur Verifizierung werden beide Dateien benötigt: der Parser lädt den Inhalt und die Signatur, und
prüft die Signatur gegen den Inhalt.

**Bei JSON-Dateien** wird die **kanonisierte Form** (RFC 8785) signiert — nicht die gespeicherte
Datei. Dies stellt sicher, dass Formatierungsunterschiede (Whitespace, Schlüsselreihenfolge) die
Signatur nicht invalidieren.

**Bei Nicht-JSON-Dateien** (Assets) werden die **rohen Bytes** signiert.

### Signatur-Formate

Diese Spezifikation schreibt kein Signatur-Format vor. Das Manifest nennt das Format jeder Signatur
im Feld `format`; welche Formate ein Parser unterstützt, entscheidet die Implementierung.

| Kennung        | Format                       | Standard           |
| -------------- | ---------------------------- | ------------------ |
| `jws-detached` | JWS mit abgetrenntem Inhalt  | RFC 7515, Anhang F |
| `cms-detached` | CMS-`SignedData` ohne Inhalt | RFC 5652           |

Diese beiden Kennungen sind für die genannten Formate reserviert. Jedes andere Format MUSS eine
Kennung in Reverse-Domain-Form verwenden, zum Beispiel `com.example/ed25519-raw`.

Ein Parser, der das Format einer Signatur nicht unterstützt, MUSS melden, dass die Signatur nicht
geprüft wurde, und DARF die Datei NICHT als signiert behandeln.

Wie Schlüssel und Zertifikate beschafft werden und wem vertraut wird, liegt außerhalb dieser
Spezifikation.

### Manifest-Referenz

Die Signatur wird im Manifest wie folgt deklariert:

```jsonc
"signature": {
  "path": "signatures/rulemap.json.sig",
  "format": "jws-detached"
}
```

| Feld     | Typ    | Beschreibung                                          |
| -------- | ------ | ----------------------------------------------------- |
| `path`   | String | MUSS den Pfad zur Signatur-Datei im Container angeben |
| `format` | String | MUSS das Signatur-Format angeben                      |

### Mehrfachsignaturen

Eine Datei DARF von mehreren Parteien signiert werden. In diesem Fall MUSS `signature` ein Array
sein:

```jsonc
"signature": [
  {
    "path": "signatures/rulemap.json.ministry.sig",
    "format": "cms-detached",
    "signer": "Bundesministerium der Justiz"
  },
  {
    "path": "signatures/rulemap.json.auditor.sig",
    "format": "jws-detached",
    "signer": "Auditor"
  }
]
```

Das optionale `signer`-Feld DARF einen menschenlesbaren Bezeichner des Signierenden enthalten. Die
kryptographische Identität wird durch das Zertifikat in der Signatur-Datei selbst bestimmt —
`signer` dient nur der Lesbarkeit.

### Manifest-Signatur als Vertrauensanker

Das Manifest DARF wie jede andere Datei im Container signiert werden. Die Signatur wird im
`files`-Eintrag des Manifests selbst deklariert:

```jsonc
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
```

Wird das Manifest signiert, entsteht eine **Vertrauenskette über den gesamten Container**:

1. Die Manifest-Signatur schützt den Manifest-Inhalt
2. Das Manifest enthält die Hashes aller Inhaltsdateien
3. Die Hashes schützen die Dateiinhalte

Ein signiertes Manifest bedeutet: _„Der Signierende bestätigt die Integrität aller im Manifest
referenzierten Dateien zum Zeitpunkt der Signierung."_

**Berechnung:** Bei der Hash-Berechnung und Signierung des Manifests MUSS der eigene Eintrag
(`"manifest.json"`) aus dem `files`-Objekt ausgenommen werden. Hash und Signatur werden über die
kanonisierte (RFC 8785) Version des Manifests berechnet, in der dieser Schlüssel nicht vorhanden
ist. Der Eintrag wird erst nach der Signierung in das Manifest eingefügt.

**Empfehlung:** Für rechtlich bindende Container SOLLTE das Manifest signiert werden. Für maximale
Sicherheit SOLLTE ein Container sowohl einzelne Dateien signieren (pro-Datei-Verantwortung) als auch
das Manifest (Container-Integrität als Ganzes).

### Integration mit qualifizierten Signaturen

Für rechtlich bindende Signaturen (z.B. unter eIDAS, ZertES, ESIGN Act) wird typischerweise
folgender Ablauf verwendet:

1. Die Datei im Container kanonisieren (RFC 8785 bei JSON)
2. Den Hash der kanonisierten Datei berechnen
3. Den Hash an einen qualifizierten Vertrauensdiensteanbieter (QTSP) senden
4. Der QTSP signiert den Hash mit dem privaten Schlüssel des Signierenden (auf einem HSM)
5. Die Signatur wird zurückgegeben und als `.sig`-Datei im Container abgelegt
6. Das Manifest wird mit `"format": "cms-detached"` aktualisiert

Dieser Ablauf erfordert keine Änderung am RUML-Format — die qualifizierte Signatur ist einfach eine
CMS-Datei im `signatures/`-Verzeichnis.

### Validierung

Bei der Signaturprüfung MUSS ein Parser:

1. Die Signatur-Datei und die Quelldatei aus dem Container laden
2. Die Quelldatei kanonisieren (bei JSON) bzw. die rohen Bytes verwenden (bei Assets)
3. Die Signatur gegen den kanonisierten Inhalt prüfen
4. Bei ungültiger Signatur MUSS ein Fehler ausgelöst werden

Ein Parser SOLLTE zusätzlich:

- Die Zertifikatskette validieren (bei CMS-Signaturen)
- Den Zeitstempel prüfen (falls vorhanden)
- Den Sperrstatus des Zertifikats prüfen (OCSP/CRL)

Die Tiefe der Signaturvalidierung hängt vom Anwendungskontext ab. Ein Entwicklungstool DARF sich auf
die kryptographische Gültigkeit beschränken. Ein System für rechtlich bindende Dokumente MUSS die
vollständige Zertifikatskette und den Sperrstatus prüfen.
