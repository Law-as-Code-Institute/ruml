<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.6 Verarbeitungsreihenfolge

### Die drei Schichten

Das RUML-Container-Format definiert drei unabhängige Schichten, die in einer festen Reihenfolge
angewendet werden:

| Schicht                | Frage                               | Zweck                 |
| ---------------------- | ----------------------------------- | --------------------- |
| **1. Hash**            | „Ist die Datei unverändert?"        | Technische Integrität |
| **2. Signatur**        | „Wer hat die Datei veröffentlicht?" | Authentizität         |
| **3. Verschlüsselung** | „Wer darf die Datei lesen?"         | Vertraulichkeit       |

**Reihenfolge:** Klartext → Hash → Signatur → Verschlüsselung → Container (ZIP)

### Erstellungsreihenfolge (Authoring)

Beim Erstellen eines Containers MUSS folgende Reihenfolge eingehalten werden:

1. **Hash berechnen** — über die kanonisierte Klartextdatei (RFC 8785 bei JSON, rohe Bytes bei
   Assets). Der Wert kommt in Schritt 4 ins Manifest.
2. **Signatur erstellen** — über die kanonisierte Klartextdatei. In die Signatur-Datei schreiben.
3. **Verschlüsseln** — die Klartextdatei verschlüsseln. Die verschlüsselte Version in `encrypted/`
   ablegen. Die Klartextdatei aus dem Container entfernen.
4. **Manifest erstellen** — alle Dateien, ihre Hashes und ihre Schichten im Manifest dokumentieren.
5. **Manifest hashen/signieren** — optional, als letzter Schritt.

### Verarbeitungsreihenfolge (Consuming)

Beim Öffnen eines Containers MUSS folgende Reihenfolge eingehalten werden:

1. **Manifest lesen** — das Manifest laden und parsen.
2. **Manifest verifizieren** — wenn das Manifest einen Signatur-Eintrag für sich selbst hat, diesen
   zuerst prüfen. Algorithmus-Deklarationen im Manifest (`"algorithm"`-Felder) sind erst nach dieser
   Verifikation vertrauenswürdig: Ohne eine verifizierte Manifest-Signatur kann jede
   Algorithmus-Deklaration von einer Partei mit Schreibzugriff auf den Container substituiert
   werden.
3. **Pro Datei**, in dieser Reihenfolge:
   - **Entschlüsseln** — wenn die Datei verschlüsselt ist, die `.enc`-Datei entschlüsseln.
   - **Signatur prüfen** — wenn eine Signatur vorhanden ist, die Signatur gegen die (entschlüsselte)
     Klartextdatei prüfen.
   - **Hash prüfen** — wenn ein Hash vorhanden ist, den Hash der (entschlüsselten) Klartextdatei
     berechnen und vergleichen.

### Schichten sind optional und unabhängig

Jede Schicht ist optional. Folgende Kombinationen sind gültig:

| Hash | Signatur | Verschlüsselung | Anwendungsfall                                                 |
| ---- | -------- | --------------- | -------------------------------------------------------------- |
| ✗    | ✗        | ✗               | Einfacher Container (nur Bündelung)                            |
| ✓    | ✗        | ✗               | Integritätsprüfung ohne Authentizität                          |
| ✓    | ✓        | ✗               | Signierte Distribution                                         |
| ✓    | ✓        | ✓               | Integrität geprüft, signiert und verschlüsselt                 |
| ✗    | ✓        | ✗               | Signiert ohne expliziten Hash (Signatur impliziert Integrität) |
| ✗    | ✗        | ✓               | Nur verschlüsselt (z.B. vertrauliche Ergebnisse)               |

### Fehlverhalten

| Situation                                                                       | Verhalten                                                                                               |
| ------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------- |
| Hash-Abweichung                                                                 | MUSS Fehler auslösen. Datei gilt als kompromittiert.                                                    |
| Ungültige Signatur                                                              | MUSS Fehler auslösen. Datei gilt als nicht authentisch.                                                 |
| Nicht unterstützter Hash-Algorithmus                                            | MUSS Warnung ausgeben. Hash-Prüfung überspringen.                                                       |
| Nicht unterstütztes Signatur-Format                                             | MUSS melden, dass die Signatur nicht geprüft wurde. Die Datei DARF NICHT als signiert behandelt werden. |
| Nicht unterstütztes Verschlüsselungs-Format oder kein Entschlüsselungsschlüssel | MUSS die Datei als nicht lesbar melden. Andere Dateien im Container MÜSSEN weiterhin verarbeitbar sein. |
