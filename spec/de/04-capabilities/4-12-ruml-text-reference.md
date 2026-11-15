<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.12 ruml:text-reference

## 4.12 Capability `ruml:text-reference`

### Überblick

| Eigenschaft             | Wert                                                        |
| ----------------------- | ----------------------------------------------------------- |
| **Capability-ID**       | `ruml:text-reference`                                       |
| **Scope**               | Root-Level (`data`) + Node-Level                            |
| **Standard `required`** | `false`                                                     |
| **Node-Level**          | `payload.refs` des `ruml:text-reference`-Eintrags am Knoten |
| **Rolle**               | `data`                                                      |

Diese Capability verknüpft Knoten mit normativen Texten — Gesetzen, Verordnungen, technischen
Normen, Verwaltungsvorschriften und anderen Regelwerken.

Eine RUML-Datei trägt ihre Texte im Root-`data`-Objekt — als Klartext oder als strukturierter
[RUML Text](#ruml-text). Node-seitige [Anker](#node-level-anker) sind **lokal**: Sie zeigen nur in
die Texte derselben RUML-Datei. Eine Rulemap, die sich auf ein Gesetz in einer anderen RUML-Datei
stützt, verankert sich nicht im Text dieser Datei; sie referenziert die Knoten des Gesetzes
([`ruml:tree-reference`](4-15-ruml-tree-reference.md)), die eigene Anker haben.

**Die Norm des Knotens (`represents`):** Unter seinen Ankern DARF ein Knoten den einen Text
markieren, den er _repräsentiert_ — die Norm, die die Regel umsetzt (siehe
[Node-Level](#node-level-anker)).

**Abgrenzung zu `ruml:context`:** `ruml:context` ([Kapitel 4.11](4-11-ruml-context.md)) enthält
unterstützende, informative Materialien (Urteile, Kommentare, Beispiele) sowie den zu prüfenden
Sachverhalt. `ruml:text-reference` enthält normative Grundlagentexte, auf die Entscheidungsregeln
sich stützen.

### Anwendungsfälle

- Verknüpfung von Knoten mit zugrundeliegenden Normen und Regelwerken
- Dokumentation der Rechtsgrundlagen für Audit-Trails
- Ein vollständiges Gesetz als strukturierter Text in der RUML-Datei, die es repräsentiert
- Verknüpfung jedes Knotens der Rulemap dieses Gesetzes mit dem Element des Textes, das er
  repräsentiert
- Mehrsprachige Texte für internationale Anwendungen

---

### Root-Level: Text-Einträge

Texte werden über die Capability `ruml:text-reference` bereitgestellt — entweder inline im
`capabilities`-Array der RUML-Datei oder über eine RUML-EXT-Sidecar-Datei
([Kapitel 4.5](4-5-ruml-ext.md)):

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:text-reference",
      "payload": {
        "data": {
          "text_main": {
            "title": "Sozialgesetzbuch (SGB) Zwölftes Buch (XII) – Sozialhilfe",
            "uri": "eli/bund/bgbl-1/2003/s3023/2026-07-30/1/deu",
            "timestamp": "2026-10-09T00:00:00Z",
            "digest": "sha3-256:87464fc40b2e11c817467dffbc6c57c16d1611e132d4ae8d431f3f755357198f",
            "source": {
              "uri": "https://testphase.rechtsinformationen.bund.de/v1/legislation/eli/bund/bgbl-1/2003/s3023/2026-07-30/1/deu/regelungstext-verkuendung-1.xml"
            },
            "content": {
              "type": "akomaNtoso",
              "attrs": {
                "xmlns": "http://Inhaltsdaten.LegalDocML.de/1.8.2/"
              },
              "content": [/* ... */]
            }
          },
          "text_bgb_823": {
            "title": "§ 823 BGB – Schadensersatzpflicht",
            "uri": "/akn/de/act/1896-08-18/bgb#sec_823__subsec_1",
            "timestamp": "2024-01-01T00:00:00Z",
            "status": "inForce",
            "text": "Wer vorsätzlich oder fahrlässig das Leben, den Körper, die Gesundheit, die Freiheit, das Eigentum oder ein sonstiges Recht eines anderen widerrechtlich verletzt, ist dem anderen zum Ersatz des daraus entstehenden Schadens verpflichtet.",
            "validFrom": "2002-01-01T00:00:00Z",
            "language": "de"
          },
          "text_3f2c9a1e4b7d4e0f9a6c1b2d3e4f5a6b": {
            "title": "Benutzungssatzung der Stadtbibliothek",
            "timestamp": "2026-10-10T09:00:00Z",
            "digest": "sha3-256:b146f781bafdee78f9e68475fca93da37cf68d3559cd1c5f6e82ab3cef9c2638",
            "content": {
              "type": "akomaNtoso",
              "attrs": {
                "xmlns": "http://Inhaltsdaten.LegalDocML.de/1.8.2/"
              },
              "content": [/* ... */]
            }
          }
        }
      }
    }
  ],
  "metadata": {/* ... */},
  "rulemap": {/* ... */}
}
```

**Key-Konvention:** Die Keys im `data`-Objekt (z.B. `text_main`) dienen als eindeutige
Identifikatoren. Keys **MÜSSEN** dem Muster `[a-z_][a-z0-9_]*` entsprechen ([`TXT-02`](../08-validation/index.md#rule-txt-02)). Ein
separates `id`-Feld ist nicht erforderlich. Anker enthalten den Key, daher **DARF** sich ein Key
**NICHT** mehr ändern, sobald Anker auf ihn zeigen können ([`TXT-03`](../08-validation/index.md#rule-txt-03)); Tools, die Keys erzeugen,
**SOLLTEN** `text_` gefolgt von den 32 Hexadezimalziffern einer UUID ohne Bindestriche verwenden
(`text_3f2c9a1e4b7d4e0f9a6c1b2d3e4f5a6b`) und Keys **NICHT** aus Titeln ableiten. Jede amtliche
Sprachfassung eines Textes ist ein eigener Eintrag (z.B. `text_de`, `text_fr`).

#### Pflichtfelder

| **Feld**    | **Typ**  | **Beschreibung**                                                                                                                                                                                    |
| ----------- | -------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `title`     | String   | **MUSS** den lesbaren Titel des Textes angeben, z.B. für Listen und Kataloge ([`TXT-04`](../08-validation/index.md#rule-txt-04)).                                                                                                       |
| `timestamp` | DateTime | **MUSS** den Zeitpunkt der Erfassung als RFC 3339 `date-time` angeben ([`TXT-04`](../08-validation/index.md#rule-txt-04), [`TXT-05`](../08-validation/index.md#rule-txt-05)).                                                                                               |
| `status`    | Enum     | **MUSS** den Status angeben (siehe [Status-Werte](#status-werte)), sofern der Eintrag kein `content` hat; mit `content` ergibt sich der Status aus den Metadaten des Textes selbst ([`TXT-04`](../08-validation/index.md#rule-txt-04)). |

#### Optionale Felder

| **Feld**        | **Typ**  | **Beschreibung**                                                                                                                                                                                                                                                          |
| --------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `uri`           | String   | **MUSS** den Text identifizieren, wenn er von einer Behörde oder einer anderen externen Quelle veröffentlicht ist (siehe [URI-Konvention](#uri-konvention)); entfällt bei Texten, die in dieser RUML-Datei selbst geschrieben sind.                                       |
| `type`          | Enum     | **DARF** die Art der Einbindung angeben: `embedded`, `container`, `url`, `external`. Standard: `embedded`. `external` ist veraltet ([`TXT-06`](../08-validation/index.md#rule-txt-06)).                                                                                                                       |
| `text`          | String   | **DARF** den Text als Klartext enthalten. Ein Eintrag **DARF NICHT** zugleich `text` und `content` haben ([`TXT-06`](../08-validation/index.md#rule-txt-06), [`TXT-07`](../08-validation/index.md#rule-txt-07)).                                                                                                                                  |
| `content`       | Object   | **DARF** den Text als [RUML Text](#ruml-text) enthalten. Erfordert `digest` ([`TXT-06`](../08-validation/index.md#rule-txt-06), [`TXT-08`](../08-validation/index.md#rule-txt-08)).                                                                                                                                                               |
| `digest`        | String   | **MUSS** bei vorhandenem `content` angegeben sein: `sha3-256:` gefolgt vom Hex-SHA3-256 der [kanonischen Form](#digest) von `content` ([`TXT-08`](../08-validation/index.md#rule-txt-08), [`TXT-09`](../08-validation/index.md#rule-txt-09)).                                                                                                     |
| `source`        | Object   | **SOLLTE** bei vorhandenem `content` angegeben sein: Herkunft des Textes — `uri` des Quelldokuments, aus dem er importiert wurde, optional `digest` der archivierten Quelle, optional `terms` (URI der Nutzungsbedingungen der Quelle, sofern die Quelle welche vorgibt). |
| `url`           | String   | **MUSS** bei `type: "url"` die URL enthalten. **MUSS** ein gültiges URI-Format haben ([`TXT-05`](../08-validation/index.md#rule-txt-05), [`TXT-10`](../08-validation/index.md#rule-txt-10)).                                                                                                                                                      |
| `containerPath` | String   | **MUSS** bei `type: "container"` den Pfad im Container angeben. **MUSS** mit `.texts/` beginnen ([`TXT-10`](../08-validation/index.md#rule-txt-10), [`TXT-11`](../08-validation/index.md#rule-txt-11)).                                                                                                                                           |
| `ref`           | String   | **MUSS** bei `type: "external"` eine symbolische Referenz enthalten ([`TXT-10`](../08-validation/index.md#rule-txt-10)).                                                                                                                                                                                      |
| `version`       | String   | **DARF** die Fassung angeben (z.B. `"Fassung vom 1.1.2024"`) ([`TXT-06`](../08-validation/index.md#rule-txt-06)).                                                                                                                                                                                             |
| `validFrom`     | DateTime | **DARF** den Gültigkeitsbeginn angeben. **MUSS** ein RFC 3339 `date-time` sein ([`TXT-05`](../08-validation/index.md#rule-txt-05), [`TXT-06`](../08-validation/index.md#rule-txt-06)).                                                                                                                                                            |
| `validUntil`    | DateTime | **DARF** das Gültigkeitsende angeben. **MUSS** wenn vorhanden > `validFrom` sein ([`TXT-06`](../08-validation/index.md#rule-txt-06), [`TXT-12`](../08-validation/index.md#rule-txt-12)).                                                                                                                                                          |
| `language`      | String   | **DARF** die Sprache angeben. **MUSS** dem ISO 639-1 Format entsprechen (z.B. `"de"`, `"en"`) ([`TXT-05`](../08-validation/index.md#rule-txt-05), [`TXT-06`](../08-validation/index.md#rule-txt-06)).                                                                                                                                             |
| `isReferenced`  | Boolean  | **DARF** angeben, ob dieser Eintrag von Nodes referenziert wird. Standard: `true` ([`TXT-06`](../08-validation/index.md#rule-txt-06)).                                                                                                                                                                        |

Hat ein Eintrag `content`, **SOLLTEN** die Felder `status`, `validFrom`, `validUntil`, `language`
und `version` weggelassen werden; sind sie vorhanden, **MÜSSEN** sie mit den Metadaten des Textes
selbst übereinstimmen ([`TXT-13`](../08-validation/index.md#rule-txt-13)).

#### URI-Konvention

Die `uri` eines Text-Eintrags identifiziert einen Text, der außerhalb der RUML-Datei existiert —
vorzugsweise über seinen amtlichen Identifikator. Ein in der RUML-Datei selbst geschriebener Text
hat keine `uri`; er ist über die Datei und seinen Eintrags-Key identifiziert. Die `uri` dient nicht
dazu, Elemente innerhalb des Textes zu adressieren; das leisten [Anker](#node-level-anker).

| Format                                | Beispiel                                                                                   | Hinweise                                                    |
| ------------------------------------- | ------------------------------------------------------------------------------------------ | ----------------------------------------------------------- |
| European Legislation Identifier (ELI) | `eli/bund/bgbl-1/2003/s3023/2026-07-30/1/deu`, `http://data.europa.eu/eli/reg/2016/679/oj` | Bevorzugt, wo die Behörde ELIs vergibt                      |
| Akoma Ntoso (AKN)                     | `/akn/de/act/1900-08-18/bgb`                                                               | Internationaler Standard für Rechtsdokumente                |
| STOP (NL)                             | `/akn/nl/act/2024/gst-2024-123`                                                            | Niederländische Rechtsdokumente                             |
| Gesetze-im-Internet                   | `https://www.gesetze-im-internet.de/bgb/__823.html`                                        | Akzeptabel für deutsches Recht ohne amtlichen Identifikator |

Die RUML-Spezifikation schreibt **kein** bestimmtes URI-Schema vor. Autoren **SOLLTEN** den
amtlichen Identifikator verwenden, wo einer existiert.

#### Einbindungsarten (`type`)

| **Type**    | **Beschreibung**                                    | **Verwendung**                                                                               |
| ----------- | --------------------------------------------------- | -------------------------------------------------------------------------------------------- |
| `embedded`  | Direkt in der RUML-Datei, als `text` oder `content` | Text beliebiger Länge — von einzelnen Absätzen bis zum vollständigen Wortlaut eines Gesetzes |
| `container` | Im RUML-Container (ZIP)                             | Original-/Binärformate (z.B. PDF)                                                            |
| `url`       | Externe URL                                         | Öffentliche Portale (z.B. [gesetze-im-internet.de](https://www.gesetze-im-internet.de))      |
| `external`  | Symbolische Referenz (veraltet)                     | Abgelöst durch RUML-Dateien, die den Text selbst tragen                                      |

**Hinweis zu vollständigen Gesetzen:** Eine Rulemap, die ein Gesetz repräsentiert
(`documentType: "law"`), trägt den vollständigen Wortlaut als `embedded`-Eintrag, vorzugsweise als
`content` in RUML Text — es gibt KEINE Längenbegrenzung. Andere Rulemaps referenzieren die Knoten
dieses Gesetzes, statt den Text zu kopieren.

**Hinweis zu `url`:** Das Tool **SOLLTE** den Inhalt bei Bedarf abrufen und cachen. Die URL
**SOLLTE** auf eine stabile, versionierte Quelle verweisen.

**Hinweis zu `external`:** Das Tool **MUSS** die symbolische Referenz (`ref`) in eine konkrete
Datenquelle auflösen. Die Konfiguration erfolgt in den Tool-Einstellungen, **NICHT** in der
RUML-Datei. Neue Dateien **SOLLTEN** stattdessen die RUML-Datei referenzieren, die den Text trägt.

Die vollständige Container-Spezifikation (ZIP-Struktur, Manifest, Verzeichniskonventionen) ist in
[Kapitel 7](../07-container/index.md) definiert.

#### Status-Werte

| **Status** | **Beschreibung** | **Verwendung**                                              |
| ---------- | ---------------- | ----------------------------------------------------------- |
| `draft`    | Entwurf          | Noch nicht verabschiedet                                    |
| `proposed` | Vorgeschlagen    | Eingebrachte Entwürfe, in Beratung                          |
| `enacted`  | Verabschiedet    | Beschlossen, aber noch nicht in Kraft                       |
| `inForce`  | In Kraft         | Aktuell gültige Norm                                        |
| `amended`  | Geändert         | Durch neuere Version ersetzt, aber noch gültig für Altfälle |
| `repealed` | Aufgehoben       | Außer Kraft getreten                                        |

**Validierungsregel:** Bei `status: "inForce"` und `type: "embedded"` (dem Standard) **MUSS** der
Eintrag ein nicht-leeres `text` oder ein `content` haben ([`TXT-07`](../08-validation/index.md#rule-txt-07)). Einträge mit jedem anderen
Status **DÜRFEN** beides weglassen.

---

### RUML Text

RUML Text ist die strukturierte Form eines Rechtstextes: ein
[Akoma-Ntoso](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/)-XML-Dokument, verlustfrei
als JSON geschrieben. Er ist Teil des RUML-Formats, kein eigenes Dateiformat: Er existiert nur im
`content` eines Text-Eintrags, und für ihn gelten die Regeln der `$specVersion` der Datei. XML
bleibt das Format für Austausch und Validierung: Akoma-Ntoso-Dokumente, auch die nationaler Dialekte
wie LegalDocML.de, werden mechanisch in RUML Text und zurück umgewandelt
([Umwandlung](#umwandlung)).

#### Struktur

```jsonc
"content": {
  "type": "akomaNtoso",
  "attrs": {
    "xmlns": "http://Inhaltsdaten.LegalDocML.de/1.8.2/"
  },
  "content": [
    {
      "type": "act",
      "attrs": {
        "name": "regelungstext"
      },
      "content": [
        {
          "type": "body",
          "content": [
            {
              "type": "article",
              "attrs": {
                "eId": "art-z1",
                "GUID": "0b1e9e8a-2c55-4f5f-9a3e-6d1c7b2a4e01"
              },
              "content": [
                {
                  "type": "num",
                  "content": ["§ 1"]
                },
                {
                  "type": "heading",
                  "content": ["Aufgabe der Sozialhilfe"]
                },
                {
                  "type": "paragraph",
                  "attrs": {
                    "eId": "art-z1_abs-z",
                    "GUID": "5d8f3c21-7a64-4c0b-8e2f-1a9b6c3d7e02"
                  },
                  "content": [
                    {
                      "type": "num"
                    },
                    {
                      "type": "content",
                      "content": [
                        {
                          "type": "p",
                          "content": [
                            "Aufgabe der Sozialhilfe ist es, den Leistungsberechtigten die Führung eines Lebens zu ermöglichen, das der Würde des Menschen entspricht.",
                            {
                              "type": "marker",
                              "attrs": {
                                "eId": "art-z1_abs-z_inhalt-n1_text-n1_marker-n1",
                                "GUID": "9a7c2e14-3b58-4d6f-a1e0-4c2b8d5f6a03",
                                "refersTo": "satzende"
                              }
                            },
                            " Die Leistung soll sie so weit wie möglich befähigen, unabhängig von ihr zu leben; darauf haben auch die Leistungsberechtigten nach ihren Kräften hinzuarbeiten.",
                            {
                              "type": "marker",
                              "attrs": {
                                "eId": "art-z1_abs-z_inhalt-n1_text-n1_marker-n2",
                                "GUID": "e27b9d03-1c4a-4f86-b5d2-7a0c9e3f1b24",
                                "refersTo": "satzende"
                              }
                            },
                            " Zur Erreichung dieser Ziele haben die Leistungsberechtigten und die Träger der Sozialhilfe im Rahmen ihrer Rechte und Pflichten zusammenzuwirken.",
                            {
                              "type": "marker",
                              "attrs": {
                                "eId": "art-z1_abs-z_inhalt-n1_text-n1_marker-n3",
                                "GUID": "55a21fb5-d00e-41c1-91a2-38eda90f21e0",
                                "refersTo": "satzende"
                              }
                            }
                          ]
                        }
                      ]
                    }
                  ]
                }
              ]
            }
          ]
        }
      ]
    }
  ]
}
```

- **Elemente:** Jedes Element des XML-Dokuments ist ein Knoten `{type, attrs?, content?}`. `type`
  ist der Elementname, `attrs` enthält seine Attribute als Zeichenketten, beide so benannt wie im
  XML. `content` enthält seine Kinder in Dokumentreihenfolge; Zeichendaten sind einfache
  JSON-Zeichenketten.
- **Exakter Baum:** Hüllelemente wie `content`, `intro` oder `num` sind Knoten wie alle anderen.
  Alle Zeichendaten bleiben erhalten, auch Leerraum zwischen Elementen. Benachbarte Zeichenketten
  **MÜSSEN** zu einer zusammengefasst werden ([`TXT-14`](../08-validation/index.md#rule-txt-14)).
- **Wurzel:** Das Wurzelobjekt ist das Akoma-Ntoso-Wurzelelement. Es **MUSS** `type`, `attrs` und
  `content` haben ([`TXT-15`](../08-validation/index.md#rule-txt-15)).
- **Namensräume:** Namensraum-Deklarationen sind Attribute und bleiben dort, wo das XML sie hat. Die
  Wurzel **MUSS** den Namensraum ihres [Dialekts](#dialekte) als Standard-Namensraum deklarieren
  (`xmlns`), sodass die Elemente des Dialekts kein Präfix tragen; kein anderes Element deklariert
  `xmlns` neu ([`TXT-15`](../08-validation/index.md#rule-txt-15), [`TXT-16`](../08-validation/index.md#rule-txt-16)). Namen aus anderen Namensräumen, etwa die
  `ris:`-Metadaten von LegalDocML.de, behalten ihr Präfix; das Präfix **MUSS** durch ein Attribut
  `xmlns:<präfix>` am Element oder einem Vorfahren deklariert sein ([`TXT-16`](../08-validation/index.md#rule-txt-16)). Elemente und
  Attribute jedes Namensraums **MÜSSEN** erhalten bleiben, auch wenn ein Tool sie nicht versteht
  ([`TXT-17`](../08-validation/index.md#rule-txt-17)).
- **Dokumenttypen:** Die Wurzel kann jeden Akoma-Ntoso-Dokumenttyp enthalten — `act`, `bill`,
  `amendment`, `judgment`, `documentCollection` und weitere.

#### Umwandlung

**Aus XML.** Jedes Element wird zu einem Knoten mit seinem Namen als `type`, seinen Attributen
(einschließlich Namensraum-Deklarationen) als `attrs` und seinen Kindern als `content`.
Zeichendaten, CDATA-Abschnitte und aufgelöste Entitäts- und Zeichenreferenzen werden zu
Zeichenketten. Nicht abgebildet werden die XML-Deklaration, die Dokumenttyp-Deklaration, Kommentare,
Verarbeitungsanweisungen und das Attribut `xsi:schemaLocation`: Sie tragen keinen Teil des
Rechtstextes. Ein Element **DARF** das Attribut `xsi:schemaLocation` **NICHT** haben
([`TXT-16`](../08-validation/index.md#rule-txt-16)). Bindet die Quelle den Namensraum des Dialekts an ein Präfix
(LegalDocML.de-Dokumente verwenden `akn:`), entfernt der Importer das Präfix aus den Namen der
Elemente dieses Namensraums und deklariert den Namensraum mit `xmlns` an der Wurzel; die Deklaration
`xmlns:<präfix>` behält er nur, solange Attribute das Präfix noch verwenden.

**Nach XML.** Jeder Knoten wird zu einem Element namens `type` mit den Attributen aus `attrs` und
seinem `content` in Reihenfolge. Zeichenketten werden zu Zeichendaten, wobei `&`, `<` und `>`
maskiert werden, in Attributwerten zusätzlich `"`, Tabulator, Zeilenvorschub und Wagenrücklauf. Ein
Exporter **DARF** eine XML-Deklaration und die Schema-Verweise schreiben, die sein Dialekt verwendet
(bei LegalDocML.de `xsi:schemaLocation` an der Wurzel und eine `xml-model`-Verarbeitungsanweisung
für das Schematron).

**Hin und zurück.** Ein XML-Dokument, das in RUML Text und zurück umgewandelt wird, gleicht dem
Original nach [Canonical XML 2.0](https://www.w3.org/TR/xml-c14n2/), bis auf die nicht abgebildeten
Teile und ein vom Importer entferntes Präfix.

#### Dialekte

Der Standard-Namensraum der Wurzel benennt den Akoma-Ntoso-Dialekt des Textes und seine Version. In
XML umgewandelt **MUSS** ein Text gegen die Schemas seines Dialekts gültig sein ([`TXT-18`](../08-validation/index.md#rule-txt-18)). Ein
Text **DARF** ein Fragment sein, dem Teile fehlen, die sein Dialekt verlangt, etwa der `meta`-Block
eines von einem Tool erzeugten Textes; jedes Element, das er enthält, **MUSS** dann dort gültig
sein, wo es in einem vollständigen Dokument des Dialekts steht ([`TXT-18`](../08-validation/index.md#rule-txt-18)). RUML wiederholt
keine Regeln des Dialekts: Nummerierung, `eId`-Bildung und Zitierung legt der Dialekt fest, und
seine Schemas prüfen sie.

| Dialekt                           | Namensraum (`xmlns`)                               | Schemas                                                                                                                                                                                                                                                                                                                                   |
| --------------------------------- | -------------------------------------------------- | ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| Akoma Ntoso 3.0 (OASIS)           | `http://docs.oasis-open.org/legaldocml/ns/akn/3.0` | [XSD](https://docs.oasis-open.org/legaldocml/akn-core/v1.0/os/part2-specs/schemas/akomantoso30.xsd)                                                                                                                                                                                                                                       |
| LegalDocML.de 1.8.2 (Bundesrecht) | `http://Inhaltsdaten.LegalDocML.de/1.8.2/`         | [XSD](https://raw.githubusercontent.com/digitalservicebund/ris-norms/18c7c79ddc0e17f6cab36ba16171927b80a43272/LegalDocML.de/1.8.2/schema/legalDocML.de-baukasten.xsd), [Schematron](https://raw.githubusercontent.com/digitalservicebund/ris-norms/18c7c79ddc0e17f6cab36ba16171927b80a43272/LegalDocML.de/1.8.2/schema/legalDocML.de.sch) |

#### Element-Identität: `GUID`

Jedes Element mit einer `eId` **MUSS** auch eine `GUID` haben ([`TXT-16`](../08-validation/index.md#rule-txt-16)). Die `GUID` ist die
dauerhafte Identität des Elements, und [Anker](#node-level-anker) zeigen auf sie; die `eId` ist
seine lesbare Bezeichnung in der aktuellen Fassung, nach den Regeln des [Dialekts](#dialekte) des
Textes aus der Nummerierung gebildet (bei LegalDocML.de: Schematron-Regeln SCH-00430 bis SCH-00450),
und ändert sich bei einer Neunummerierung.

- **Wert:** **MUSS** eine kleingeschriebene UUID (RFC 9562, [`TXT-16`](../08-validation/index.md#rule-txt-16)) sein, vergeben, wenn das
  Element angelegt wird. Ein Text, der aus einer Quelle mit `GUID`-Werten importiert wird
  (LegalDocML.de verlangt eine an jedem Element), behält diese.
- **Eindeutigkeit:** Innerhalb eines Text-Eintrags **MUSS** eine `GUID` eindeutig sein
  ([`TXT-16`](../08-validation/index.md#rule-txt-16)). Ein kopiertes Element ist ein neues Element und erhält eine neue `GUID`.
- **Stabilität:** Eine `GUID` **DARF** sich **NICHT** ändern — weder in veröffentlichten Versionen
  noch in Entwürfen, denn Anker in dieser Datei und Referenzen anderer RUML-Dateien auf die hier
  verankerten Knoten können sich bereits auf sie stützen ([`TXT-03`](../08-validation/index.md#rule-txt-03)). Eine Neunummerierung
  ändert nur `eId`-Werte.
- **Über Fassungen hinweg:** Eine neue Fassung eines Textes behält die `GUID` jedes fortbestehenden
  Elements und gibt neuen Elementen neue. Vergibt eine Quelle für jede Fassung neue `GUID`-Werte,
  **MUSS** der Import die `GUID` jedes Elements übernehmen, das er der vorigen Fassung zuordnet
  ([`TXT-03`](../08-validation/index.md#rule-txt-03)).
- **Sprachen:** Jede Sprachfassung ist ein eigener Text-Eintrag mit eigenen `GUID`-Werten; RUML
  definiert keine Identität über Sprachfassungen hinweg.

**Beispiel:** „§ 3“ wird mit der `eId` `art-z3` und der `GUID` `7c1e9a52-…` angelegt. Davor wird ein
neuer § 2 eingefügt; das Element wird zu „§ 4“ mit der `eId` `art-z4` — seine `GUID` bleibt
`7c1e9a52-…`, jeder Anker darauf findet es weiterhin, und Zitate zeigen das aktuelle „§ 4“.

#### Sätze

Markiert die Quelle das Ende eines Satzes mit einem `marker`-Element, dessen `refersTo` `satzende`
ist (wie LegalDocML.de), identifiziert die `GUID` des Markers den an diesem Marker endenden Satz;
ein Anker darauf adressiert diesen Satz. Tools **DÜRFEN NICHT** Satzmarker hinzufügen, die die
Quelle nicht enthält ([`TXT-17`](../08-validation/index.md#rule-txt-17)). Texte ohne Satzmarker sind bis zu ihrem kleinsten markierten
Element (z.B. Absatz oder Nummer) adressierbar.

#### Digest

Der `digest` eines Text-Eintrags ist `sha3-256:` gefolgt vom kleingeschriebenen Hex-SHA3-256-Hash
der UTF-8-Bytes der RFC-8785-Form (JSON Canonicalization Scheme) von `content`. Ein Parser
**SOLLTE** ihn prüfen, bevor er sich auf den Text stützt.

#### Herkunft

`source` hält fest, woher der Text importiert wurde; `source.terms` verweist auf die
Nutzungsbedingungen der Quelle, sofern die Quelle welche vorgibt (zum Beispiel eine
Namensnennungspflicht).

RUML definiert keine Klartextform von RUML Text. Tools, die Klartext benötigen, leiten ihn selbst
aus dem Baum ab.

---

### Node-Level: Anker

Knoten verweisen mit **Ankern** in der Liste `refs` ihres node-seitigen
`ruml:text-reference`-Eintrags auf die Texte ihrer eigenen RUML-Datei. Ein Anker benennt einen
Text-Eintrag über seinen Key und optional ein Element seines RUML Text über die
[`GUID`](#element-identität-guid) des Elements.

```jsonc
{
  "id": "ruml:text-reference",
  "payload": {
    "refs": [
      {
        "id": "text_main",
        "element": "9a7c2e14-3b58-4d6f-a1e0-4c2b8d5f6a03",
        "type": "represents"
      },
      {
        "id": "text_main",
        "element": "e27b9d03-1c4a-4f86-b5d2-7a0c9e3f1b24",
        "type": "refers-to"
      },
      {
        "id": "text_bgb_823",
        "type": "refers-to"
      }
    ]
  }
}
```

| **Feld**  | **Typ**       | **Pflicht** | **Beschreibung**                                                                                                                                                                                                                                        |
| --------- | ------------- | ----------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `refs`    | Array[Object] | **MUSS**    | Die Anker des Knotens; mindestens einer ([`TXT-01`](../08-validation/index.md#rule-txt-01)).                                                                                                                                                                                                |
| `id`      | String        | **MUSS**    | Key eines Text-Eintrags im eigenen `data`-Objekt dieser Datei ([`TXT-01`](../08-validation/index.md#rule-txt-01)).                                                                                                                                                                          |
| `element` | String        | **DARF**    | `GUID` eines Elements im RUML Text des Eintrags — ein Paragraf, ein Absatz, ein Listenelement, ein Satzende-Marker. Ohne `element` adressiert der Anker den ganzen Text ([`TXT-01`](../08-validation/index.md#rule-txt-01)).                                                                |
| `type`    | Enum          | **MUSS**    | `represents`: die Norm, die der Knoten umsetzt — der Text, den die Regel in eine Entscheidung überführt. `refers-to`: ein Text, auf den sich der Knoten stützt, ohne ihn umzusetzen, etwa eine Begriffsbestimmung oder eine Verweisung ([`TXT-01`](../08-validation/index.md#rule-txt-01)). |

**Validierungsregeln:**

- `refs` **MUSS** mindestens einen Anker enthalten ([`TXT-01`](../08-validation/index.md#rule-txt-01)).
- Ein Knoten **DARF NICHT** mehr als einen Anker vom Typ `represents` haben ([`TXT-01`](../08-validation/index.md#rule-txt-01)).
- Jede `id` **MUSS** als Key im `data`-Objekt der `ruml:text-reference`-Capability dieser Datei
  existieren ([`TXT-19`](../08-validation/index.md#rule-txt-19)).
- Ein `element` **MUSS** die `GUID` eines Elements im `content` dieses Eintrags sein; ein Eintrag
  ohne `content` kann nur als Ganzes verankert werden ([`TXT-20`](../08-validation/index.md#rule-txt-20)).
- Anker **MÜSSEN** eindeutig sein — dieselbe Kombination aus `id`, `element` und `type` **DARF
  NICHT** zweimal vorkommen ([`TXT-01`](../08-validation/index.md#rule-txt-01)).

Anker verlassen ihre RUML-Datei nie, deshalb tragen sie weder Datei noch Version: Wechselt die Datei
auf eine neue Fassung ihres Textes, bleiben die Anker unverändert, weil `GUID`-Werte stabil sind.
Zeichenbereiche und Textzitat-Selektoren werden nicht unterstützt; die kleinste adressierbare
Einheit ist ein Element mit `GUID`.

**Verhalten bei modularen Knoten:** Ein modularer Knoten (`modular: true`) repräsentiert stets
dieselbe Norm — seine Anker gelten für **alle Instanziierungen**, unabhängig davon, wo der Knoten im
Regelbaum erscheint.

## Konformitätstests

- [4.12 ruml:text-reference](../../../tests/04-capabilities/4-12-ruml-text-reference.test.yaml)
