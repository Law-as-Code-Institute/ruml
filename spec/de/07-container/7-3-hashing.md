<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.3 Hash-Schicht

### Zweck

Hashing dient ausschließlich der **technischen Integritätsprüfung** — es beantwortet die Frage:
_„Ist diese Datei unverändert?"_

Hashing bietet **keine Authentizität** und **keine Unveränderlichkeitsgarantie**. Jede Person mit
Schreibzugriff kann den Inhalt ändern und einen neuen Hash berechnen. Für Authentizität und
Nicht-Abstreitbarkeit ist eine digitale Signatur erforderlich (siehe [7.4](7-4-signatures.md)).

### Hash im Manifest

Jede Datei im Container DARF einen Hash haben. Der Hash steht im Manifest-Eintrag der Datei;
separate Hash-Dateien gibt es nicht:

```jsonc
"hash": {
  "algorithm": "sha3-256",
  "value": "4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
}
```

| Feld        | Typ    | Beschreibung                                                     |
| ----------- | ------ | ---------------------------------------------------------------- |
| `algorithm` | String | MUSS den verwendeten Algorithmus angeben                         |
| `value`     | String | MUSS den Hash als kleingeschriebene Hexadezimalziffern enthalten |

Weil das Manifest die Hash-Werte enthält, deckt eine Signatur über das Manifest (siehe
[7.4](7-4-signatures.md#manifest-signatur-als-vertrauensanker)) den Inhalt jeder Datei ab, die einen
Hash hat.

### Algorithmen

| Verbindlichkeit | Algorithmus  | Kennung      | Ausgabelänge   |
| --------------- | ------------ | ------------ | -------------- |
| **MUSS**        | SHA3-256     | `sha3-256`   | 64 Hex-Zeichen |
| **DARF**        | Jeder andere | Frei wählbar | Variabel       |

Ein Parser MUSS SHA3-256 unterstützen. Ein Container SOLLTE SHA3-256 verwenden, damit jeder Parser
ihn prüfen kann.

Ein Parser, der einen Algorithmus antrifft, den er nicht unterstützt, MUSS eine Warnung ausgeben und
die Integritätsprüfung für diese Datei überspringen.

### Kanonische Repräsentation für JSON-Dateien

Für konsistente Hash-Berechnung MÜSSEN JSON-Dateien im Container nach **RFC 8785 (JCS — JSON
Canonicalization Scheme)** kanonisiert werden:

1. Objektschlüssel MÜSSEN lexikographisch sortiert sein (nach UTF-16 Code Units)
2. Whitespace außerhalb von String-Werten MUSS entfernt werden
3. Zahlen MÜSSEN in ihrer kürzesten IEEE 754 Darstellung angegeben werden

Der Hash wird über die **kanonisierte Form** berechnet, nicht über die Datei wie sie im Container
gespeichert ist. Die gespeicherte Datei DARF formatiert (Pretty-Print) sein — dies hat keinen
Einfluss auf den Hash.

Für Nicht-JSON-Dateien (Assets) wird der Hash über die **rohen Bytes** berechnet.

### Validierung

Bei der Integritätsprüfung MUSS ein Parser:

1. Die Quelldatei laden und kanonisieren (bei JSON) bzw. die rohen Bytes lesen (bei Assets)
2. Den Hash mit dem Algorithmus berechnen, den der Manifest-Eintrag nennt
3. Ihn mit dem `value` im Manifest-Eintrag vergleichen
4. Bei Abweichung MUSS ein Fehler ausgelöst werden — die Datei gilt als kompromittiert

Ein Parser MUSS die Hash-Prüfung durchführen, wenn der Manifest-Eintrag einer Datei einen `hash`
hat. Die Hash-Prüfung ist unabhängig vom Status der RUML-Datei (`draft`, `inForce` etc.) — sie wird
immer durchgeführt.
