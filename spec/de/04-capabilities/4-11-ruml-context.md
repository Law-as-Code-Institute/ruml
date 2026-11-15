<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.11 ruml:context

## 4.11 Capability `ruml:context`

### Überblick

| Eigenschaft             | Wert                                                 |
| ----------------------- | ---------------------------------------------------- |
| **Capability-ID**       | `ruml:context`                                       |
| **Scope**               | Root-Level (`data`) + Node-Level                     |
| **Standard `required`** | `false`                                              |
| **Node-Level**          | `payload.refs` des `ruml:context`-Eintrags am Knoten |
| **Rolle**               | `data`                                               |

Diese Capability stellt Context-Materialien bereit, die für die Prüfung und Anwendung der Rulemap
relevant sind. Dabei werden zwei grundlegend verschiedene Rollen unterschieden:

**Referenzmaterial** (`subject: false`, Standard) — Hintergrundwissen, das mit der Rulemap verbunden
ist: Gerichtsurteile, Kommentare, Verwaltungsvorschriften, Richtlinien, Beispielfälle.
Referenzmaterial ist Teil der Rulemap oder ihrer Sidecar-Dateien und bleibt über alle Prüfvorgänge
hinweg gleich.

**Prüfgegenstand** (`subject: true`) — Ein Dokument, das selbst Gegenstand der Bewertung in
mindestens einem Prüfvorgang ist: ein zu bewertendes Gutachten, ein zu prüfender Antrag oder
Bescheid, Beweismittel wie Fotos oder Dokumente. Anders als Referenzmaterial werden Prüfgegenstände
typischerweise pro Prüfvorgang bereitgestellt und sind nicht fest in der Rulemap hinterlegt.

Die Zuordnung der Rolle erfolgt an zwei Stellen:

- Am **Context-Objekt** selbst: `subject: true` signalisiert, dass dieses Dokument mindestens an
  einer Stelle als Prüfgegenstand dient
- In der **`inputs.context`-Referenz** einer `ruml:ai-query`: `role: "subject"` bzw.
  `role: "reference"` bestimmt, in welcher Rolle das Dokument für diese konkrete Query verwendet
  wird (siehe [Kapitel 4.9](4-9-ruml-ai-query.md))

### Anwendungsfälle

**Als Referenzmaterial:**

- Gerichtsurteile und Präzedenzfälle zur Auslegung von Regelungen
- Gesetzeskommentare und Fachliteratur
- Verwaltungsvorschriften und Richtlinien
- Beispiel- und Musterfälle für AI Queries
- Historische Entwicklung einer Regelung
- Verknüpfte Rulemaps für Detailprüfungen

**Als Prüfgegenstand:**

- Gutachten, die inhaltlich bewertet werden sollen
- Anträge und Bescheide zur Prüfung
- Fotos, Screenshots oder Dokumente als Beweismittel
- Berichte und Stellungnahmen als Entscheidungsgrundlage

### Bereitstellung über Capability

Context-Objekte werden über die Capability `ruml:context` bereitgestellt — entweder inline im
`capabilities`-Array oder über eine RUML-EXT-Sidecar-Datei:

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:context",
      "payload": {
        "data": {
          "ctx_bgh_2024": {
            "title": "BGH zur Auslegung des Wohnsitzbegriffs",
            "category": "courtDecision"
            // ...
          },
          "ctx_example_approved": {
            "title": "Beispiel: Genehmigter Härtefall",
            "category": "example"
            // ...
          }
        }
      }
    }
  ],
  "metadata": {/* ... */},
  "rulemap": {/* ... */}
}
```

### Grundstruktur

```jsonc
"ctx_bgh_2024": {
  "title": "BGH zur Auslegung des Wohnsitzbegriffs",
  "category": "courtDecision",
  "type": "url",
  "timestamp": "2024-01-15T10:00:00Z",
  // ...
  "metadata": {/* ... */},
  "content": {/* ... */},
  "source": {/* ... */}
}
```

### Pflichtfelder

| **Feld**                                                                                                                                                                                                                           | **Typ**  | **Beschreibung**                                                                                          |
| ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- | -------- | --------------------------------------------------------------------------------------------------------- |
| `title`                                                                                                                                                                                                                            | String   | MUSS einen Titel haben ([`CTX-01`](../08-validation/index.md#rule-ctx-01)).                                                                   |
| `category`                                                                                                                                                                                                                         | Enum     | MUSS eine der definierten Kategorien sein (siehe unten) ([`CTX-01`](../08-validation/index.md#rule-ctx-01), [`CTX-02`](../08-validation/index.md#rule-ctx-02)).                   |
| `timestamp`                                                                                                                                                                                                                        | DateTime | MUSS den Änderungszeitpunkt des Contexts als RFC 3339 `date-time` angeben ([`CTX-01`](../08-validation/index.md#rule-ctx-01), [`CTX-03`](../08-validation/index.md#rule-ctx-03)). |
| **Hinweis:** Der Object-Key (z.B. `"ctx_bgh_2024"`) dient als Identifikator (siehe [Kapitel 3.2.6](../03-data-model/3-2-data-types-and-formats.md)). Context-IDs MÜSSEN dem Muster `[a-z_][a-z0-9_]*` entsprechen ([`CTX-04`](../08-validation/index.md#rule-ctx-04)). |

Context-Objekte werden auf Root-Ebene im `data`-Feld der Capability definiert — dies ist der Pool
des verfügbaren Contexts. Sie werden zum Zeitpunkt der Definition nicht an Knoten gebunden.

#### Bindung von Context an Knoten

Ein Knoten referenziert die von ihm verwendeten Context-Objekte über das `refs`-Array im `payload`
seines Node-Level-`ruml:context`-Eintrags, analog zu `payload.refs` des
`ruml:text-reference`-Eintrags (siehe [Kapitel 4.3](4-3-capabilities-node-field.md)). Dieselbe
Context-ID DARF im `refs`-Array eines Knotens NICHT mehrfach vorkommen ([`CTX-05`](../08-validation/index.md#rule-ctx-05)).

```jsonc
"2": {
  "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
  "label": "Einkommensgrenze unterschritten",
  "capabilities": [
    {
      "id": "ruml:context",
      "payload": {
        "refs": ["ctx_bgh_2024", "ctx_guidelines"]
      }
    }
  ]
}
```

### Optionale Felder

| **Feld**        | **Typ** | **Beschreibung**                                                                                                                                                                                                                                                                                                                     |
| --------------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `type`          | Enum    | DARF die Art der Einbindung angeben: `embedded`, `container`, `url`, `external`. Standard: `embedded`. Für `container`-, `url`- oder `external`-Einträge explizit setzen ([`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                                                            |
| `subject`       | Boolean | DARF angeben, dass dieses Dokument mindestens an einer Stelle als Prüfgegenstand dient (siehe Rollenunterscheidung oben). Standard: `false` ([`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                                                                                         |
| `metadata`      | Object  | DARF zusätzliche kategoriespezifische Metadaten enthalten ([`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                                                                                                                                                                           |
| `content`       | Object  | DARF den Payload und/oder eine Zusammenfassung enthalten. Offenes Objekt — die interne Struktur ist flexibel (siehe [Content-Objekt](#content-object)) ([`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                                                                              |
| `source`        | Object  | DARF Quellenangaben enthalten ([`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                                                                                                                                                                                                       |
| `url`           | String  | MUSS bei `type: "url"` die URL des Dokuments enthalten ([`CTX-07`](../08-validation/index.md#rule-ctx-07)).                                                                                                                                                                                                                                                              |
| `containerPath` | String  | MUSS bei `type: "container"` den Pfad im Container angeben ([`CTX-07`](../08-validation/index.md#rule-ctx-07)).                                                                                                                                                                                                                                                          |
| `ref`           | String  | MUSS bei `type: "external"` eine symbolische Referenz enthalten ([`CTX-07`](../08-validation/index.md#rule-ctx-07)).                                                                                                                                                                                                                                                     |
| `hash`          | String  | DARF einen Integritäts-Hash der referenzierten Datei bzw. des Dokuments enthalten, bei Einträgen jeden `type` (typischerweise `container` oder `url`) ([`CTX-06`](../08-validation/index.md#rule-ctx-06)). MUSS die Form `<Algorithmus>:<Hex>` haben: der Algorithmus `sha3-256`, `sha256` oder `blake3`, dann 64 Hexadezimalzeichen in Kleinbuchstaben ([`CTX-08`](../08-validation/index.md#rule-ctx-08)). |
| `accessDate`    | Date    | DARF das Datum des letzten Zugriffs auf die Quelle als ISO-8601-Datum (`YYYY-MM-DD`) angeben. Bei Einträgen jeden `type` zulässig, typischerweise `url` ([`CTX-03`](../08-validation/index.md#rule-ctx-03), [`CTX-06`](../08-validation/index.md#rule-ctx-06)).                                                                                                                                              |

### 4.11.1 Context-Kategorien

Context-Objekte werden über das `category`-Feld nach ihrer inhaltlichen Art kategorisiert.

Das `metadata`-Objekt ist offen — RUML schreibt keine bestimmten Schlüssel je Kategorie vor.
Vorhandene Werte SOLLTEN den RUML-Datentypen entsprechen (siehe
[Kapitel 3.2](../03-data-model/3-2-data-types-and-formats.md)); darüber hinaus ist
implementierungsabhängig, wie Metadaten validiert werden. Die folgenden Beispiele zeigen gängige
Schlüssel, von denen jedoch keiner verpflichtend ist.

### Vordefinierte Kategorien

| **Kategorie**            | **Beschreibung**                                                                     |
| ------------------------ | ------------------------------------------------------------------------------------ |
| `courtDecision`          | Gerichtsurteil / Präzedenzfall                                                       |
| `commentary`             | Gesetzeskommentar                                                                    |
| `administrativeGuidance` | Verwaltungsvorschrift / Richtlinie                                                   |
| `explanatoryMemorandum`  | Gesetzesbegründung — Auslegungsmaterial ersten Ranges aus dem Gesetzgebungsverfahren |
| `example`                | Beispiel- / Musterfall                                                               |
| `literature`             | Fachliteratur / Aufsatz                                                              |
| `faq`                    | Häufige Fragen                                                                       |
| `history`                | Historische Entwicklung                                                              |
| `rulemap`                | Verknüpfte RUML-Datei                                                                |
| `custom`                 | Benutzerdefiniert                                                                    |

### Beispiele nach Kategorie

**courtDecision:**

```jsonc
"ctx_bgh_2024": {
  "title": "BGH zur Auslegung des Wohnsitzbegriffs",
  "category": "courtDecision",
  "type": "url",
  "timestamp": "2024-01-15T10:00:00Z",
  "url": "https://www.bundesgerichtshof.de/2024/123",
  "metadata": {
    "court": "BGH",
    "reference": "I ZR 123/23",
    "date": "2024-01-01"
  },
  "content": {
    "summary": "Präzisierung des Wohnsitzbegriffs bei Auslandsbezug"
  },
  "source": {
    "citation": "BGH, Urt. v. 1.1.2024 - I ZR 123/23",
    "url": "https://www.bundesgerichtshof.de/2024/123",
    "publication": "NJW 2024, 456"
  }
}
```

**commentary:**

```jsonc
"ctx_palandt_823": {
  "title": "Palandt zu § 823 BGB",
  "category": "commentary",
  "type": "external",
  "timestamp": "2024-01-01T00:00:00Z",
  "metadata": {
    "author": "Sprau",
    "publication": "Palandt BGB Kommentar",
    "edition": "83. Auflage 2024"
  },
  "ref": "legal_database_palandt",
  "source": {
    "citation": "Palandt/Sprau, § 823 Rn. 15-20",
    "license": "Copyright"
  }
}
```

**administrativeGuidance:**

```jsonc
"ctx_bmf_income_tax": {
  "title": "BMF-Schreiben zur Einkommensteuer",
  "category": "administrativeGuidance",
  "type": "url",
  "timestamp": "2024-01-01T00:00:00Z",
  "metadata": {
    "authority": "Bundesministerium der Finanzen",
    "reference": "IV C 2 - S 2400/19/10001",
    "validFrom": "2024-01-01"
  },
  "url": "https://www.bundesfinanzministerium.de/bmf-schreiben/2024-01-01-einkommensteuer",
  "source": {
    "citation": "BMF-Schreiben v. 1.1.2024, IV C 2 - S 2400/19/10001",
    "license": "Public Domain"
  }
}
```

**example:**

```jsonc
"ctx_example_approved": {
  "title": "Beispiel: Genehmigter Härtefall",
  "category": "example",
  "type": "embedded",
  "timestamp": "2024-01-01T00:00:00Z",
  "content": {
    "text": "Fall: Alleinerziehende Mutter, zwei Kinder, Jahreseinkommen 18.000 EUR. Begründung: Unvorhergesehene Krankheitskosten. Entscheidung: Genehmigt.",
    "summary": "Genehmigung aufgrund unvorhergesehener Krankheitskosten"
  }
}
```

**rulemap:**

```jsonc
"ctx_rulemap_residence": {
  "title": "Detailprüfung Wohnsitzbegriff",
  "category": "rulemap",
  "type": "external",
  "timestamp": "2024-01-01T00:00:00Z",
  "metadata": {
    "rulemapId": "043fdfce-d617-4a76-af40-e02de43c07b8",
    "rulemapHash": "sha3-256:ed73f1144536b4be0eaa8d8dcc82bbfacbca02ca3bea57b4dc8b5c67484b5c0f",
    "relationship": "extends",
    "description": "Vertiefende Prüfung für Sonderfälle"
  },
  "ref": "rulemap_repository"
}
```

### Relationship-Typen für verknüpfte Rulemaps

| **Relationship** | **Beschreibung**                |
| ---------------- | ------------------------------- |
| `extends`        | Erweitert diese Rulemap         |
| `replaces`       | Ersetzt ältere Version          |
| `references`     | Verweist auf verwandte Regelung |
| `depends`        | Benötigt diese Rulemap          |
| `conflicts`      | Steht im Widerspruch            |

### 4.11.2 Content-Typen

Das Feld `type` definiert, wie der Context-Inhalt eingebunden wird. RUML unterstützt vier
Einbindungsarten. `type` ist optional und hat den Standardwert `embedded` (siehe
[Optionale Felder](#optionale-felder)).

| **Type**    | **Beschreibung**                     | **Verwendung**                            |
| ----------- | ------------------------------------ | ----------------------------------------- |
| `embedded`  | Direkt in der RUML-Datei eingebettet | Kurze Texte, Beispiele, Zusammenfassungen |
| `container` | Im RUML-Container (ZIP) eingebettet  | PDF-Dokumente, umfangreiche Texte         |
| `url`       | Externe URL                          | Öffentliche Dokumente, Gesetzestexte      |
| `external`  | Symbolische Referenz                 | Datenbanken, APIs, lokale Dateien         |

### Type: embedded

Der Inhalt wird direkt im `content`-Objekt der RUML-Datei gespeichert.

```jsonc
"ctx_example_rejected": {
  "title": "Beispiel: Abgelehnter Härtefall",
  "category": "example",
  "type": "embedded",
  "timestamp": "2024-01-01T00:00:00Z",
  "content": {
    "text": "Fall: Einzelperson, Jahreseinkommen 45.000 EUR. Begründung: Urlaubsreise geplant. Entscheidung: Abgelehnt, da keine Härte erkennbar.",
    "summary": "Ablehnung mangels Härtefall-Kriterien"
  }
}
```

**Content-Objekt** {#content-object}

`content` ist ein **offenes Objekt** — seine interne Struktur ist flexibel und wird von RUML nicht
eingeschränkt. Die Beispiele in diesem Kapitel verwenden `text` (der Payload bei `type: "embedded"`)
und `summary`; `media` (Base64-kodiert) ist ebenfalls gängig. Jede andere Struktur ist zulässig.

**Empfehlung:** `type: "embedded"` für Texte unter 10.000 Zeichen und kleine Medien unter 1 MB
verwenden.

### Type: container

Der Inhalt wird als separate Datei im RUML-Container gespeichert (siehe
[Kapitel 7](../07-container/index.md) für die vollständige Container-Spezifikation).

```jsonc
"ctx_bgh_judgment_pdf": {
  "title": "BGH-Urteil I ZR 123/23",
  "category": "courtDecision",
  "type": "container",
  "timestamp": "2024-01-15T10:00:00Z",
  "containerPath": ".context/BGH-I-ZR-123-23.pdf",
  "hash": "sha3-256:49ebbe3e80b9c4ad2cb32540c4b052017d346b2306e75bf669d1dfc281cdaf6d",
  "content": {
    "summary": "Präzisierung des Wohnsitzbegriffs bei Auslandsbezug"
  },
  "metadata": {
    "court": "BGH",
    "reference": "I ZR 123/23",
    "date": "2024-01-01"
  }
}
```

**Felder bei container:**

| **Feld**        | **Typ** | **Beschreibung**                                                                                  |
| --------------- | ------- | ------------------------------------------------------------------------------------------------- |
| `containerPath` | String  | MUSS den Pfad im Container angeben. MUSS mit `.context/` beginnen ([`CTX-07`](../08-validation/index.md#rule-ctx-07), [`CTX-09`](../08-validation/index.md#rule-ctx-09)). |
| `hash`          | String  | DARF den Hash der Datei zur Integritätsprüfung enthalten.                                         |

### Type: url

Der Inhalt wird über eine externe URL referenziert.

```jsonc
"ctx_estg_32a": {
  "title": "§ 32a EStG - Einkommensteuertarif",
  "category": "administrativeGuidance",
  "type": "url",
  "timestamp": "2024-01-01T00:00:00Z",
  "url": "https://www.gesetze-im-internet.de/estg/__32a.html",
  "hash": "sha3-256:877998158956cc7b189ce0906e3b6c30cf2cc27e6d8d3dc3170460389d610b5b",
  "content": {
    "summary": "Grundtarif der Einkommensteuer"
  },
  "source": {
    "citation": "§ 32a EStG",
    "license": "Public Domain"
  }
}
```

**Pflichtfelder bei url:**

| **Feld** | **Typ** | **Beschreibung**                                                |
| -------- | ------- | --------------------------------------------------------------- |
| `url`    | String  | MUSS eine gültige URL enthalten ([`CTX-03`](../08-validation/index.md#rule-ctx-03), [`CTX-07`](../08-validation/index.md#rule-ctx-07)). |

**Optionale Felder bei url:**

| **Feld**     | **Typ** | **Beschreibung**                                              |
| ------------ | ------- | ------------------------------------------------------------- |
| `hash`       | String  | DARF den Hash des Dokuments zur Integritätsprüfung enthalten. |
| `accessDate` | Date    | DARF das Datum des letzten Zugriffs angeben.                  |

**Hinweis:** Bei `type: "url"` SOLLTE das Tool den Inhalt zur Laufzeit laden und cachen. Der
optionale `hash` ermöglicht die Prüfung, ob sich der Inhalt geändert hat.

### Type: external

Der Inhalt wird über eine symbolische Referenz bezogen, die vom Tool zur Laufzeit aufgelöst wird.

```jsonc
"ctx_internal_guidelines": {
  "title": "Interne Bearbeitungsrichtlinien",
  "category": "administrativeGuidance",
  "type": "external",
  "timestamp": "2024-01-01T00:00:00Z",
  "ref": "internal_knowledge_base",
  "content": {
    "summary": "Richtlinien für die Sachbearbeitung"
  }
}
```

**Pflichtfelder bei external:**

| **Feld** | **Typ** | **Beschreibung**                                          |
| -------- | ------- | --------------------------------------------------------- |
| `ref`    | String  | MUSS eine symbolische Referenz enthalten ([`CTX-07`](../08-validation/index.md#rule-ctx-07)). |

**Tool-Workflow:**

1. Beim Laden der RUML-Datei sammelt das Tool alle Context-Objekte mit `type: "external"`
2. Das Tool zeigt eine Übersicht: "Folgende Context-Quellen müssen konfiguriert werden:"
3. Für jede `ref` ermöglicht das Tool die Zuordnung zu einer konkreten Datenquelle
4. Die Verbindungsdetails werden in der Tool-Konfiguration gespeichert, NICHT in der RUML-Datei

**Anwendungsfälle für external:**

- Interne Wissensdatenbanken
- Proprietäre Dokumentenserver
- Dynamische Inhalte aus APIs
- Lokale Dateisysteme

### 4.11.3 Quellenangaben und Lizenzen

Das optionale `source`-Objekt dokumentiert die Herkunft des Context-Inhalts und dessen
Nutzungsrechte.

### Source-Objekt Struktur

```jsonc
"ctx_commentary_823": {
  "title": "Kommentar zu § 823 BGB",
  "category": "commentary",
  "type": "external",
  "timestamp": "2024-01-01T00:00:00Z",
  "ref": "legal_database",
  "source": {
    "citation": "Palandt/Sprau, § 823 Rn. 15-20",
    "author": "Sprau, Hartwig",
    "publication": "Palandt BGB Kommentar, 83. Auflage",
    "url": "https://beck-online.de/palandt-bgb/823",
    "isbn": "978-3-406-12345-6",
    "doi": "10.1234/example.doi",
    "accessDate": "2024-06-01",
    "license": "Copyright",
    "note": "Nur Zitate nach § 51 UrhG erlaubt"
  }
}
```

### Source-Felder

`source` ist ein **offenes Objekt** mit flexibler Struktur. Das Beispiel oben zeigt die gängigen
Schlüssel (`citation`, `author`, `publication`, `url`, `isbn`, `doi`, `accessDate`, `license`,
`note`); jeder weitere Schlüssel ist zulässig. Von diesen hat nur `license` eine definierte Semantik
— siehe [Lizenzen](#lizenzen) unten.

### Lizenzen

Das `license`-Feld dokumentiert die Nutzungsrechte des eingebundenen Materials. Dies ist kritisch
für die rechtskonforme Verwendung von urheberrechtlich geschütztem Material.

`license` ist ein **freier String**, keine geschlossene Aufzählung — proprietäre oder
benutzerdefinierte Lizenzkennungen sind zulässig. Die folgenden Werte sind ein empfohlenes
Vokabular, das Tools erkennen SOLLTEN. Der Wert `null` ist ausdrücklich zulässig und signalisiert
einen unbekannten oder unklaren Rechtsstatus, den Tools konservativ behandeln MÜSSEN (siehe
[Handlungsempfehlungen für Tools](#handlungsempfehlungen-für-tools)).

**Gängige Lizenzen und ihre Bedeutung:**

| **Lizenz**        | **Bedeutung**              | **Erlaubte Nutzung in RUML**               |
| ----------------- | -------------------------- | ------------------------------------------ |
| `"Public Domain"` | Gemeinfrei                 | Vollständige Einbindung erlaubt            |
| `"CC0"`           | Verzicht auf alle Rechte   | Vollständige Einbindung erlaubt            |
| `"CC-BY-4.0"`     | Namensnennung erforderlich | Einbindung mit Quellenangabe               |
| `"CC-BY-SA-4.0"`  | Namensnennung + Weitergabe | Einbindung, RUML muss gleiche Lizenz haben |
| `"CC-BY-NC-4.0"`  | Nicht-kommerziell          | Nur für nicht-kommerzielle RUML            |
| `"Copyright"`     | Alle Rechte vorbehalten    | Nur Zitate im Rahmen des Zitatrechts       |
| `"Proprietary"`   | Proprietär/Geschützt       | Nur mit expliziter Erlaubnis               |

### Beispiele für Quellenangaben

**Gerichtsurteil (meist gemeinfrei):**

```jsonc
"source": {
  "citation": "BGH, Urt. v. 1.1.2024 - I ZR 123/23",
  "url": "https://www.bundesgerichtshof.de/2024/123",
  "publication": "NJW 2024, 456",
  "license": "Public Domain",
  "note": "Amtliche Werke nach § 5 UrhG gemeinfrei"
}
```

**Kommentarliteratur (geschützt):**

```jsonc
"source": {
  "citation": "Palandt/Sprau, § 823 Rn. 15",
  "author": "Sprau, Hartwig",
  "publication": "Beck Verlag 2024",
  "isbn": "978-3-406-12345-6",
  "license": "Copyright",
  "note": "Nur Zitate nach § 51 UrhG erlaubt"
}
```

**Open Access Fachartikel:**

```jsonc
"source": {
  "citation": "Müller, Digitale Verwaltung, JurPC 2024",
  "author": "Müller, Klaus",
  "doi": "10.1234/jurpc.2024.123",
  "url": "https://www.jurpc.de/2024/123",
  "license": "CC-BY-4.0",
  "note": "Volltext-Einbindung mit Namensnennung erlaubt"
}
```

**Verwaltungsvorschrift:**

```jsonc
"source": {
  "citation": "BMF-Schreiben v. 1.1.2024, IV C 2 - S 2400/19/10001",
  "url": "https://www.bundesfinanzministerium.de/bmf-schreiben/2024-01-01-einkommensteuer",
  "license": "Public Domain",
  "note": "Amtliches Werk"
}
```

**Unklare Rechtslage:**

```jsonc
"source": {
  "citation": "Historisches Dokument von 1950",
  "license": null,
  "note": "Urheberrechtsstatus unklar - Vorsicht bei Verwendung"
}
```

### Quellenangaben

Das `source`-Objekt ist optional. Es SOLLTE überall dort angegeben werden, wo Urheber- oder
Lizenzangaben relevant sind — insbesondere bei Fremdmaterial wie Kommentaren oder Literatur, wo eine
`license` die Nutzungsrechte explizit macht.

### Handlungsempfehlungen für Tools

Basierend auf der Lizenz SOLLTEN Tools:

| **Lizenz**                       | **Tool-Verhalten**                           |
| -------------------------------- | -------------------------------------------- |
| Open License (CC, Public Domain) | Volltext anzeigen, Bearbeitung erlauben      |
| Copyright/Proprietary            | Nur Zusammenfassung/Zitate, Warnung anzeigen |
| Lizenz fehlt/unklar              | Warnung anzeigen, konservativ behandeln      |

**Wichtiger Hinweis:** Die Angabe einer offenen Lizenz in der RUML-Datei ersetzt NICHT die Prüfung
der tatsächlichen Rechtslage. Ersteller von RUML-Dateien sind selbst verantwortlich für die
rechtskonforme Nutzung von Fremdmaterial.

### 4.11.4 Vollständiges Beispiel

Das folgende Beispiel zeigt eine RUML-Datei mit verschiedenen Context-Typen, die in einer AI Query
referenziert werden:

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:context",
      "payload": {
        "data": {
          "ctx_guidelines": {
            "title": "Richtlinien zur Härtefallprüfung",
            "category": "administrativeGuidance",
            "type": "url",
            "timestamp": "2024-01-01T00:00:00Z",
            "url": "https://www.example.gov/haertefall-richtlinien.pdf",
            "hash": "sha3-256:bd7a69bf084c64d738739cff1a68a9949802e82c83314fd1b93c3ce58a028afb",
            "metadata": {
              "authority": "Bundesministerium für Soziales",
              "reference": "BMSoz-2024-001",
              "validFrom": "2024-01-01"
            },
            "content": {
              "summary": "Offizielle Richtlinien für die Beurteilung von Härtefällen"
            },
            "source": {
              "citation": "BMSoz-Richtlinie v. 1.1.2024",
              "license": "Public Domain"
            }
          },
          "ctx_bsg_ruling": {
            "title": "BSG zur Auslegung des Härtefallbegriffs",
            "category": "courtDecision",
            "type": "container",
            "timestamp": "2023-06-15T10:00:00Z",
            "containerPath": ".context/BSG-B-14-AS-123-22.pdf",
            "hash": "sha3-256:d70cff10ab78f18281549cf0c0daf5a13370b8142797be951e75c5f74c5f0eef",
            "metadata": {
              "court": "BSG",
              "reference": "B 14 AS 123/22",
              "date": "2023-06-15"
            },
            "content": {
              "summary": "Grundsatzurteil zur Auslegung des Härtefallbegriffs im Sozialrecht"
            },
            "source": {
              "citation": "BSG, Urt. v. 15.6.2023 - B 14 AS 123/22",
              "publication": "BSGE 135, 123",
              "license": "Public Domain"
            }
          },
          "ctx_example_approved_medical": {
            "title": "Beispiel: Genehmigt - Medizinische Notlage",
            "category": "example",
            "type": "embedded",
            "timestamp": "2024-01-01T00:00:00Z",
            "content": {
              "text": "Fall: Alleinerziehende Mutter, zwei Kinder (4 und 7 Jahre), Jahreseinkommen 18.000 EUR. Begründung: Unvorhergesehene Krankheitskosten nach Unfall des älteren Kindes, Zuzahlungen für Rehabilitation. Entscheidung: Genehmigt. Begründung: Unvorhersehbarkeit der Kosten, nachgewiesene finanzielle Belastung, soziale Verantwortung für Kinder.",
              "summary": "Genehmigung aufgrund unvorhergesehener medizinischer Kosten"
            }
          },
          "ctx_example_approved_job_loss": {
            "title": "Beispiel: Genehmigt - Arbeitsplatzverlust",
            "category": "example",
            "type": "embedded",
            "timestamp": "2024-01-01T00:00:00Z",
            "content": {
              "text": "Fall: Einzelperson, 52 Jahre, vorheriges Jahreseinkommen 42.000 EUR, aktuell arbeitslos. Begründung: Betriebsbedingte Kündigung nach 20 Jahren, schwierige Arbeitsmarktlage in der Region. Entscheidung: Genehmigt. Begründung: Unverschuldeter Arbeitsplatzverlust, fortgeschrittenes Alter erschwert Neuanstellung.",
              "summary": "Genehmigung aufgrund unverschuldeten Arbeitsplatzverlusts"
            }
          },
          "ctx_example_rejected_luxury": {
            "title": "Beispiel: Abgelehnt - Freiwillige Ausgaben",
            "category": "example",
            "type": "embedded",
            "timestamp": "2024-01-01T00:00:00Z",
            "content": {
              "text": "Fall: Einzelperson, Jahreseinkommen 45.000 EUR. Begründung: Finanzielle Engpässe nach Kauf eines Neuwagens und geplanter Urlaubsreise. Entscheidung: Abgelehnt. Begründung: Selbstverschuldete Situation durch freiwillige Luxusausgaben, keine unvorhersehbare Notlage.",
              "summary": "Ablehnung aufgrund selbstverschuldeter Situation"
            }
          },
          "ctx_example_rejected_income": {
            "title": "Beispiel: Abgelehnt - Einkommen zu hoch",
            "category": "example",
            "type": "embedded",
            "timestamp": "2024-01-01T00:00:00Z",
            "content": {
              "text": "Fall: Ehepaar, gemeinsames Jahreseinkommen 85.000 EUR. Begründung: Hohe Kreditraten für Eigenheim. Entscheidung: Abgelehnt. Begründung: Einkommen deutlich über Härtefallgrenze, Kreditverpflichtungen waren vorhersehbar und freiwillig eingegangen.",
              "summary": "Ablehnung aufgrund zu hohen Einkommens"
            }
          }
        }
      }
    },
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_hardship_reason": {
            "name": "Härtefallbegründung",
            "type": "string",
            "binding": {
              "type": "input",
              "hint": "Bitte beschreiben Sie Ihre besondere Situation"
            },
            "validation": {
              "required": true,
              "minLength": 50,
              "maxLength": 2000
            }
          },
          "dp_annual_income": {
            "name": "Jahreseinkommen",
            "type": "currency",
            "unit": "EUR",
            "binding": {
              "type": "input"
            },
            "validation": {
              "required": true,
              "min": 0
            }
          }
        }
      }
    },
    {
      "id": "ruml:query"
    },
    {
      "id": "ruml:ai-query"
    },
    {
      "id": "ruml:actions"
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "version": "1.0.0",
    "created": "2024-01-01T12:00:00+01:00",
    "modified": "2024-01-15T14:30:00+01:00",
    "status": "draft"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
        "operator": "AND",
        "label": "Härtefall anerkennen?",
        "children": ["2", "3"],
        "capabilities": [
          {
            "id": "ruml:actions",
            "payload": {
              "description": "Erstellt den Bescheid basierend auf dem Gesamtergebnis",
              "onTrue": {
                "operation": "createDocument",
                "ref": "document_service",
                "config": {
                  "template": "hardship-approval",
                  "format": "pdf"
                }
              },
              "onFalse": {
                "operation": "createDocument",
                "ref": "document_service",
                "config": {
                  "template": "hardship-rejection",
                  "format": "pdf"
                }
              }
            }
          }
        ]
      },
      "2": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "label": "Einkommensgrenze unterschritten",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_annual_income < 25000"
            }
          }
        ]
      },
      "3": {
        "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
        "label": "Begründung plausibel",
        "capabilities": [
          {
            "id": "ruml:ai-query",
            "payload": {
              "model": "strong",
              "description": "Prüft die Plausibilität der Härtefallbegründung anhand der Richtlinien und Beispielfälle",
              "inputs": {
                "context": [
                  "ctx_guidelines",
                  "ctx_bsg_ruling",
                  "ctx_example_approved_medical",
                  "ctx_example_approved_job_loss",
                  "ctx_example_rejected_luxury",
                  "ctx_example_rejected_income"
                ],
                "dataPoints": ["dp_hardship_reason", "dp_annual_income"]
              },
              "config": {
                "deterministic": true,
                "effort": "high"
              }
            }
          },
          {
            "id": "ruml:actions",
            "payload": {
              "onUndefined": {
                "operation": "requestDecision",
                "ref": "manual_review_workflow",
                "config": {
                  "recipient": "role:social-worker",
                  "deadline": "P5D",
                  "responseOptions": ["approve", "reject", "requestMoreInfo"],
                  "context": ["ctx_guidelines", "ctx_bsg_ruling"]
                }
              }
            }
          }
        ]
      }
    }
  }
}
```

**Hinweise zum Beispiel:**

- **Capability-Deklaration:** `ruml:context`, `ruml:ai-query` und `ruml:actions` werden im
  Root-`capabilities`-Array deklariert; Context-Daten stehen im `data`-Feld von `ruml:context`
- **Verschiedene Context-Typen:** Das Beispiel zeigt `url` (Richtlinien), `container`
  (Gerichtsurteil als PDF) und `embedded` (Beispielfälle)
- **Verschiedene Kategorien:** `administrativeGuidance`, `courtDecision` und `example`
- **Knotenbindung:** Die Beispielfälle und Richtlinien werden über `inputs.context` am AI-Query-Node
  referenziert
- **AI Query mit Context:** Die AI Query wird über `capabilities.ruml:ai-query` am Node definiert
  und referenziert Context-Objekte im `inputs.context`-Array
- **Actions als Node-Capability:** Sowohl der Root-Node als auch der AI-Query-Node verwenden
  `capabilities.ruml:actions`
- **Quellenangaben:** Alle Context-Objekte mit externen Quellen haben ein `source`-Objekt mit
  Lizenzangaben
- **Object-Key als ID:** Die Context-Objekte haben kein separates `id`-Feld – der Object-Key (z.B.
  `"ctx_guidelines"`) dient als Identifikator

### Lieferung via Sidecar (RUML-EXT)

```jsonc
{
  "$format": "RUML-EXT",
  "$specVersion": "1.0",
  "$base": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "hash": "sha3-256:4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
  },
  "capabilities": [
    {
      "id": "ruml:context",
      "payload": {
        "data": {
          "ctx_guidance": {
            "title": "Kreditvergaberichtlinien",
            "category": "administrativeGuidance",
            "type": "url",
            "url": "https://intern.bank.de/richtlinien.pdf",
            "timestamp": "2024-01-01T00:00:00Z"
          }
        }
      }
    }
  ],
  "nodes": {
    "0eb360a6-626a-406d-89a1-9f434ced141b": {
      "ruml:context": {
        "refs": ["ctx_guidance"]
      }
    }
  }
}
```

### Validierung

Alle Validierungsregeln gelten — die Pflichtfelder (`title`, `category`, `timestamp`) plus die
`type`-abhängigen (`url`, `containerPath`, `ref`), jeder `refs`-Eintrag eines Knotens MUSS auf einen
Eintrag im `data`-Pool auflösbar sein ([`CTX-10`](../08-validation/index.md#rule-ctx-10)), Lizenz-Tracking.

## Konformitätstests

- [4.11 ruml:context](../../../tests/04-capabilities/4-11-ruml-context.test.yaml)
