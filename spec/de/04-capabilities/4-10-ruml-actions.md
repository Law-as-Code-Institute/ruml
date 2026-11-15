<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

# 4.10 ruml:actions

## 4.10 Capability `ruml:actions`

### Überblick

| Eigenschaft             | Wert                                       |
| ----------------------- | ------------------------------------------ |
| **Capability-ID**       | `ruml:actions`                             |
| **Scope**               | Node-Level (`capabilities`-Feld am Knoten) |
| **Standard `required`** | `false`                                    |
| **Rolle**               | `reaction`                                 |

Diese Capability stellt Actions-Objekte an Knoten bereit. Actions lösen Aktionen basierend auf dem
Status eines Nodes aus. Sie treffen keine Entscheidungen, sondern reagieren auf den Wahrheitswert,
der durch Data Queries, AI Queries oder die Operator-Logik ermittelt wurde.

### Anwendungsfälle

Actions können grundsätzlich alles auslösen, was ein Computerbefehl auslösen kann. Die folgende
Liste zeigt Beispiele und ist nicht vollständig:

- Andere Rulemaps triggern (z.B. Detailprüfung nach positivem Ergebnis)
- Benachrichtigungen versenden (E-Mail, SMS, Push, Messenger)
- Fristen setzen und überwachen (z.B. Widerspruchsfrist nach Bescheid)
- Abfragen und Datenanforderungen auslösen (z.B. fehlende Unterlagen anfordern)
- Externe Systeme aufrufen (APIs, Webhooks, Drittsysteme)
- Dokumente erstellen (Bescheide, Berichte, Protokolle)
- Akten erstellen oder aktualisieren (CRM, ERP, Fachverfahren)
- Menschliche Entscheidungen anfordern (Workflows, Genehmigungsprozesse)
- Zahlungen oder Buchungen auslösen
- Berechtigungen freischalten oder sperren
- Fälle eskalieren, archivieren oder weiterleiten
- Logging- und Audit-Trail-Einträge schreiben

### Grundprinzip: Reaktion auf Node-Status

Actions werden über den `capabilities`-Eintrag mit `id: "ruml:actions"` an einem Node definiert und
reagieren auf dessen Status:

| **Node-Status** | **Bedeutung**                                              | **Beispiel-Aktion**                |
| --------------- | ---------------------------------------------------------- | ---------------------------------- |
| `true`          | Bedingung erfüllt                                          | Genehmigungsdokument erstellen     |
| `false`         | Bedingung nicht erfüllt                                    | Ablehnungsdokument erstellen       |
| `undefined`     | Ausgewertet, aber nicht entscheidbar (z.B. fehlende Daten) | E-Mail mit Datenanforderung senden |

### Einbettung über Capability

Actions werden über die Capability `ruml:actions` im `capabilities`-Array eines Nodes
bereitgestellt:

```jsonc
"1": {
  "id": "fcf02185-ffee-48a4-bf93-d2fb1b17944d",
  "label": "Einkommensprüfung",
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_annual_income > 50000"
      }
    },
    {
      "id": "ruml:actions",
      "payload": {
        "onTrue": {
          "operation": "createDocument",
          "ref": "approval_document_service"
        },
        "onFalse": {
          "operation": "sendNotification",
          "ref": "rejection_notification_service"
        }
      }
    }
  ]
}
```

**Regeln:**

- Actions DÜRFEN an jedem Node definiert werden (Leaf-Nodes und Parent-Nodes) ([`CAP-34`](../08-validation/index.md#rule-cap-34))
- Bei Leaf-Nodes ohne `decision`-Capability (`ruml:query` oder `ruml:ai-query`) ist der Node-Status
  immer `undefined`. In diesem Fall kann nur ein `onUndefined`-Handler ausgelöst werden; `onTrue`-
  und `onFalse`-Handler werden nie ausgeführt.
- Bei Parent-Nodes DARF `ruml:actions` alleine stehen; der Status ergibt sich aus der Operator-Logik
  der Kinder ([`CAP-34`](../08-validation/index.md#rule-cap-34))

### Auslösebedingung für Actions

Actions werden nur ausgelöst, wenn der betreffende Node im aktuellen Durchlauf tatsächlich
ausgewertet wurde. Nodes, die aufgrund eines vorherigen Abbruchs der Auswertung nicht erreicht
wurden, lösen keine Actions aus – unabhängig von ihrem Status.

**Beispiel:**

```
Node 1 (AND)
├── Node 2: Ausgewertet → true
├── Node 3: Ausgewertet → undefined (Daten fehlen) → Action wird ausgelöst
├── Node 4: Nicht erreicht (Auswertung bei Node 3 gestoppt) → Keine Action
└── Node 5: Nicht erreicht → Keine Action
```

In diesem Beispiel wird nur die `onUndefined`-Action von Node 3 ausgelöst, nicht die von Node 4 oder
Node 5, obwohl deren Status ebenfalls `undefined` ist.

**Hinweis:** Die Details zur Auswertungsreihenfolge und zum Abbruchverhalten werden in Kapitel 5
(Entscheidungsstatus) spezifiziert.

### Struktur

```jsonc
"1": {
  "id": "7baae662-0b5c-44bb-9a2b-802074fe5d0f",
  "label": "Bescheiderstellung",
  "capabilities": [
    {
      "id": "ruml:query",
      "payload": {
        "expression": "dp_application_complete = true"
      }
    },
    {
      "id": "ruml:actions",
      "payload": {
        "description": "Erstellt den entsprechenden Bescheid basierend auf der Entscheidung",
        "onTrue": {
          "operation": "createDocument",
          "ref": "approval_document_service",
          "config": {
            "template": "approval-letter",
            "format": "pdf"
          }
        },
        "onFalse": {
          "operation": "createDocument",
          "ref": "rejection_document_service",
          "config": {
            "template": "rejection-letter",
            "format": "pdf"
          }
        },
        "onUndefined": {
          "operation": "sendNotification",
          "ref": "email_service",
          "config": {
            "template": "missing-data-request",
            "channel": "email"
          }
        }
      }
    }
  ]
}
```

### Felder des actions-Objekts

| **Feld**      | **Typ** | **Beschreibung**                                                    |
| ------------- | ------- | ------------------------------------------------------------------- |
| `description` | String  | DARF beschreiben, welche Aktionen ausgeführt werden ([`CAP-35`](../08-validation/index.md#rule-cap-35)) |
| `onTrue`      | Object  | DARF die Aktion bei Status `true` definieren                        |
| `onFalse`     | Object  | DARF die Aktion bei Status `false` definieren                       |
| `onUndefined` | Object  | DARF die Aktion bei Status `undefined` definieren                   |

**Hinweis:** Mindestens eines der Felder `onTrue`, `onFalse` oder `onUndefined` MUSS vorhanden sein
([`CAP-35`](../08-validation/index.md#rule-cap-35)).

### Action-Objekt

Jedes Action-Objekt (`onTrue`, `onFalse`, `onUndefined`) hat folgende Struktur:

```jsonc
"onTrue": {
  "operation": "createDocument",
  "ref": "document_service",
  "config": {
    "template": "approval-letter",
    "format": "pdf"
  }
}
```

| **Feld**    | **Typ** | **Beschreibung**                                                             |
| ----------- | ------- | ---------------------------------------------------------------------------- |
| `operation` | String  | MUSS die Art der Aktion angeben ([`CAP-35`](../08-validation/index.md#rule-cap-35))                              |
| `ref`       | String  | MUSS eine symbolische Referenz zur Implementierung enthalten ([`CAP-35`](../08-validation/index.md#rule-cap-35)) |
| `config`    | Object  | DARF Konfigurationshinweise für die Aktion enthalten ([`CAP-35`](../08-validation/index.md#rule-cap-35))         |

### Operationen

Das Feld `operation` gibt die Art der Aktion an. Die folgende Liste ist nicht vollständig und DARF
von Implementierungen erweitert werden:

| **Operation**      | **Beschreibung**                                          |
| ------------------ | --------------------------------------------------------- |
| `triggerRulemap`   | Andere Rulemap prozessieren                               |
| `sendNotification` | Benachrichtigung versenden (E-Mail, SMS, Push, Messenger) |
| `requestData`      | Abfrage oder Datenanforderung auslösen                    |
| `callWebhook`      | Webhook oder externe API aufrufen                         |
| `triggerProcess`   | Externen Prozess starten                                  |
| `createDocument`   | Dokument generieren (Bescheid, Bericht, Protokoll)        |
| `createCase`       | Akte erstellen oder aktualisieren                         |
| `requestDecision`  | Menschliche Entscheidung anfordern                        |
| `initiatePayment`  | Zahlung oder Buchung auslösen                             |
| `managePermission` | Berechtigung freischalten oder sperren                    |
| `archive`          | Fall archivieren                                          |
| `writeAuditLog`    | Logging- oder Audit-Trail-Eintrag schreiben               |

**Hinweis:** Implementierungen DÜRFEN zusätzliche Operationen definieren ([`CAP-35`](../08-validation/index.md#rule-cap-35)). Die
RUML-Spezifikation schreibt keine geschlossene Liste vor.

### Symbolische Referenz

Das Feld `ref` enthält eine symbolische Referenz, die vom Tool zur Laufzeit aufgelöst wird.

**Tool-Workflow:**

1. Beim Laden der RUML-Datei sammelt das Tool alle Actions mit `ref`
2. Das Tool zeigt eine Übersicht: "Folgende Aktionen müssen konfiguriert werden:"
3. Für jede `ref` ermöglicht das Tool die Zuordnung zu einer konkreten Implementierung
4. Die Implementierungsdetails (E-Mail-Server, API-Endpoints, etc.) werden in der Tool-Konfiguration
   gespeichert, NICHT in der RUML-Datei

### Vollständiges Beispiel

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:datapoints",
      "payload": {
        "data": {
          "dp_annual_income": {
            "name": "Jahreseinkommen",
            "type": "currency",
            "unit": "EUR",
            "binding": {
              "type": "input"
            }
          },
          "dp_applicant_email": {
            "name": "E-Mail des Antragstellers",
            "type": "email",
            "binding": {
              "type": "input"
            }
          },
          "dp_documents_complete": {
            "name": "Unterlagen vollständig",
            "type": "boolean",
            "binding": {
              "type": "input"
            }
          }
        }
      }
    },
    {
      "id": "ruml:query"
    },
    {
      "id": "ruml:actions"
    }
  ],
  "metadata": {
    "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
    "title": "Förderantrag",
    "version": "1.0.0",
    "created": "2024-01-01T00:00:00Z",
    "modified": "2024-01-01T00:00:00Z",
    "status": "inForce",
    "validFrom": "2024-01-01T00:00:00Z"
  },
  "rulemap": {
    "nodes": {
      "1": {
        "id": "ec36948d-fbb2-4815-985a-bd5e9375d934",
        "operator": "AND",
        "label": "Förderantrag",
        "children": ["2", "3"],
        "capabilities": [
          {
            "id": "ruml:actions",
            "payload": {
              "description": "Erstellt und versendet den Bescheid basierend auf dem Gesamtergebnis",
              "onTrue": {
                "operation": "createDocument",
                "ref": "document_service",
                "config": {
                  "template": "approval-letter",
                  "format": "pdf"
                }
              },
              "onFalse": {
                "operation": "sendNotification",
                "ref": "notification_service",
                "config": {
                  "recipient": "dp_applicant_email",
                  "template": "application-rejected",
                  "channel": "email"
                }
              },
              "onUndefined": {
                "operation": "requestDecision",
                "ref": "manual_review_workflow",
                "config": {
                  "recipient": "role:case-worker",
                  "deadline": "P3D",
                  "responseOptions": ["approve", "reject"]
                }
              }
            }
          }
        ]
      },
      "2": {
        "id": "0eb360a6-626a-406d-89a1-9f434ced141b",
        "label": "Einkommensgrenze",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_annual_income < 50000"
            }
          }
        ]
      },
      "3": {
        "id": "6840b48d-117f-474e-ae4e-337b8e60537c",
        "label": "Dokumentenprüfung",
        "capabilities": [
          {
            "id": "ruml:query",
            "payload": {
              "expression": "dp_documents_complete = true"
            }
          }
        ]
      }
    }
  }
}
```

### Sicherheitshinweise

- Empfänger und Endpunkte werden als symbolische Referenzen angegeben
- Konkrete E-Mail-Adressen, API-Keys oder Server-URLs werden in der Tool-Konfiguration hinterlegt,
  NICHT in der RUML-Datei
- **Ausnahme:** Wenn ein DataPoint als Empfänger referenziert wird (z.B.
  `"recipient": "dp_applicant_email"`), wird der Wert zur Laufzeit aus dem DataPoint bezogen

### Lieferung via Sidecar (RUML-EXT)

```jsonc
{
  // ...
  "nodes": {
    "0eb360a6-626a-406d-89a1-9f434ced141b": {
      "ruml:actions": {
        "onTrue": {
          "operation": "createDocument",
          "ref": "document_service",
          "config": {
            "template": "credit-approval",
            "format": "pdf"
          }
        }
      }
    }
  }
}
```

### Anwendbarkeit

- `ruml:actions` DARF auf jedem Knotentyp verwendet werden — Leaf-Nodes und Parent-Nodes
  ([`CAP-34`](../08-validation/index.md#rule-cap-34)).
- Actions feuern nur, wenn der Knoten während der Traversierung tatsächlich ausgewertet wurde.

### Abgrenzung Spezifikation / Laufzeit

Die RUML-Spezifikation definiert ausschließlich die Deklaration von Actions — welche Aktion unter
welcher Bedingung ausgelöst werden soll. Die Ausführung, Zuordnung von Ergebnisartefakten zum
Prüfvorgang, Fehlerbehandlung und Nachverfolgung sind Verantwortung der Laufzeitumgebung.
