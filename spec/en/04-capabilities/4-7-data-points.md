<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 4.7 DataPoints

### Overview

| Property               | Value                                                      |
| ---------------------- | ---------------------------------------------------------- |
| **Capability ID**      | `ruml:datapoints`                                          |
| **Scope**              | Root level (`payload.data` of the `ruml:datapoints` entry) |
| **Default `required`** | `false`                                                    |
| **Role**               | `data`                                                     |

DataPoints define the structured data required for decisions in the rulemap. They describe the
**schema** of the data (name, type, validation) as well as a **binding hint** that indicates how the
data should be obtained.

### Core Principle: Schema-First

RUML follows the schema-first principle:

- **In the RUML file:** Only the data definition (What is needed?)
- **At runtime:** The actual values are provided by the tool

### Embedding via the `ruml:datapoints` Capability

DataPoints are defined in the `data` object of the `ruml:datapoints` capability in the root
`capabilities` array. Reusable structured types are declared alongside in an optional `sets` object
(see [4.7.4](#474-sets-reusable-structured-types)):

```jsonc
{
  "$format": "RUML",
  "$specVersion": "1.0",
  "capabilities": [
    {
      "id": "ruml:datapoints",
      "payload": {
        "sets": {
          "set_person": {/* ... */},
          "set_beschaeftigung": {/* ... */}
        },
        "data": {
          "dp_annual_income": {/* ... */},
          "dp_credit_score": {/* ... */}
        }
      }
    }
  ],
  "metadata": {/* ... */},
  "rulemap": {/* ... */}
}
```

**Note:** For map structures like `data`, the object key (e.g., `"dp_annual_income"`) serves as the
unique identifier. A separate `id` field is therefore not required (see
[Chapter 3.2.6](../03-data-model/3-2-data-types-and-formats.md) — design principle "Key = ID").

**Note on usage by other capabilities:** DataPoints exclusively define the data schema and
procurement. The collected data is available to other capabilities as a foundation — e.g.,
`ruml:query` for calculations and evaluations (see [Chapter 4.8](4-8-ruml-query.md)) or
`ruml:ai-query` for AI-powered decisions (see [Chapter 4.9](4-9-ruml-ai-query.md)).

### Basic Structure

```jsonc
"dp_annual_income": {
  "name": "Jahreseinkommen",
  "description": "Brutto-Jahreseinkommen des Antragstellers",
  "type": "currency",
  "unit": "EUR",
  "validation": {
    "required": true,
    "min": 0,
    "max": 10000000
  },
  "binding": {
    "type": "input"
  }
}
```

### Required Fields

| **Field** | **Type** | **Description**                                                                          |
| --------- | -------- | ---------------------------------------------------------------------------------------- |
| `name`    | String   | MUST contain a display name ([`DP-01`](../08-validation/index.md#rule-dp-01))                                               |
| `type`    | Enum     | MUST specify one of the defined data types (see [4.7.1](#471-data-types)) ([`DP-01`](../08-validation/index.md#rule-dp-01)) |
| `binding` | Object   | MUST specify how the data is obtained (see [4.7.2](#472-binding-types)) ([`DP-01`](../08-validation/index.md#rule-dp-01))   |

**Note:** The object key serves as the unique ID of the DataPoint. It MUST match the pattern
`[a-z_][a-z0-9_]*` ([`DP-02`](../08-validation/index.md#rule-dp-02)).

### Optional Fields

| **Field**     | **Type** | **Description**                                                                                                                                                                                                                                                        |
| ------------- | -------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `description` | String   | MAY contain a detailed description ([`DP-03`](../08-validation/index.md#rule-dp-03))                                                                                                                                                                                                                      |
| `unit`        | String   | **MUST** be present when `type: "currency"`; MAY be present when `type: "number"` or `type: "percentage"` (e.g., `"EUR"`, `"kg"`, `"%"`) ([`DP-03`](../08-validation/index.md#rule-dp-03), [`DP-05`](../08-validation/index.md#rule-dp-05)). MUST NOT be used with other types ([`DP-04`](../08-validation/index.md#rule-dp-04)).                                               |
| `format`      | String   | MAY refine the type when it is `location` (see [Location Type](#location-type)), `identifier` (see [Identifier Type](#identifier-type)) or `address` (see [Address Type](#address-type)) ([`DP-03`](../08-validation/index.md#rule-dp-03)). MUST NOT be used with other types ([`DP-04`](../08-validation/index.md#rule-dp-04)).             |
| `options`     | Array    | **MUST** be present and non-empty when `type: "enum"` — the permitted values (see [Enum Type](#enum-type)) ([`DP-06`](../08-validation/index.md#rule-dp-06)). MUST NOT be used with other types ([`DP-04`](../08-validation/index.md#rule-dp-04)).                                                                                           |
| `validation`  | Object   | MAY contain validation rules (see [4.7.3](#473-validation)) ([`DP-03`](../08-validation/index.md#rule-dp-03))                                                                                                                                                                                             |
| `sensitive`   | Boolean  | MAY indicate whether the data is sensitive. Default: `false` ([`DP-03`](../08-validation/index.md#rule-dp-03))                                                                                                                                                                                            |
| `set`         | String   | **MUST** be present when `type: "object"` — the id of the set type in `sets` (see [4.7.4](#474-sets-reusable-structured-types)) ([`DP-07`](../08-validation/index.md#rule-dp-07)). MUST NOT be used with other types ([`DP-04`](../08-validation/index.md#rule-dp-04)).                                                                      |
| `cardinality` | Object   | MAY be present when `type: "object"` — `{ "min": Integer, "max": Integer }` for repetition; `min` MUST be at least 0 and `max` at least 1 ([`DP-08`](../08-validation/index.md#rule-dp-08)). Absent = single instance; `max > 1` = a list of instances. MUST NOT be used with other types ([`DP-04`](../08-validation/index.md#rule-dp-04)). |

### 4.7.1 Data Types

The `type` field of a DataPoint defines the expected data type. RUML distinguishes between primitive
and specialized data types.

### Primitive Types

| **Type**   | **Description**                | **Example Value**        |
| ---------- | ------------------------------ | ------------------------ |
| `string`   | Text                           | `"Max Mustermann"`       |
| `number`   | Number (integer or decimal)    | `50000`, `3.14`          |
| `boolean`  | Boolean value                  | `true`, `false`          |
| `date`     | Date without time              | `"2024-01-01"`           |
| `datetime` | Date with time                 | `"2024-01-01T10:00:00Z"` |
| `time`     | Time without date              | `"14:30:00"`             |
| `integer`  | Integer (positive or negative) | `42`, `-7`               |

### Specialized Types

| **Type**     | **Description**                     | **Format**                                                                                          | **Example Value**                                     |
| ------------ | ----------------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------------------- |
| `currency`   | Monetary amount                     | Number, unit via `unit`                                                                             | `50000` (with `"unit": "EUR"`)                        |
| `percentage` | Percentage                          | Number between 0 and 100                                                                            | `32.5`                                                |
| `duration`   | Time duration                       | ISO 8601 Duration                                                                                   | `"P2Y3M"` (2 years, 3 months)                         |
| `email`      | Email address                       | RFC 5322                                                                                            | `"max@example.com"`                                   |
| `phone`      | Phone number                        | E.164                                                                                               | `"+491234567890"`                                     |
| `location`   | Geographic location                 | See location formats                                                                                | `"DE"`, `"DE-BY"`, `"80331"`                          |
| `identifier` | Official identifier                 | String with `format` hint                                                                           | `"DE123456789"` (VAT ID)                              |
| `iban`       | Bank account                        | ISO 13616                                                                                           | `"DE89370400440532013000"`                            |
| `count`      | Count/quantity                      | Non-negative integer                                                                                | `3`                                                   |
| `url`        | URL/URI                             | RFC 3986                                                                                            | `"https://example.com/bescheid/123"`                  |
| `address`    | Structured postal address           | See address formats                                                                                 | `{"street": "Musterstr. 1", ...}`                     |
| `enum`       | Selection from value list           | Value from `options`                                                                                | `"married"`                                           |
| `object`     | Instance of a reusable **set** type | References a `set`; may repeat via `cardinality` (see [4.7.4](#474-sets-reusable-structured-types)) | `{ "dp_vorname": "Eva", "dp_nachname": "Schneider" }` |

### Location Type

The `location` type allows specifying geographic locations at various levels. The optional `format`
field specifies the expected granularity:

| **Format**     | **Description**                       | **Example Value**         |
| -------------- | ------------------------------------- | ------------------------- |
| `country`      | Country (ISO 3166-1 alpha-2)          | `"DE"`, `"AT"`, `"CH"`    |
| `region`       | Country with subdivision (ISO 3166-2) | `"DE-BY"`, `"AT-9"`       |
| `union`        | State union                           | `"EU"`, `"EFTA"`, `"EEA"` |
| `postal`       | Postal code                           | `"80331"`, `"1010"`       |
| `municipality` | Municipality key                      | `"09162000"` (Munich)     |
| `coordinates`  | GPS coordinates                       | `"48.1351,11.5820"`       |

**Example:**

```jsonc
"dp_residence": {
  "name": "Wohnsitz",
  "description": "Land des Hauptwohnsitzes",
  "type": "location",
  "format": "country",
  "validation": {
    "required": true,
    "enum": ["DE", "AT", "CH"]
  },
  "binding": {
    "type": "input"
  }
}
```

```jsonc
"dp_jurisdiction": {
  "name": "Rechtsraum",
  "description": "Anwendbarer Rechtsraum",
  "type": "location",
  "format": "union",
  "validation": {
    "enum": ["EU", "EWR", "EFTA"]
  },
  "binding": {
    "type": "input"
  }
}
```

### Address Type

The `address` type allows specifying structured postal addresses.

| **Field**    | **Type** | **Description**              |
| ------------ | -------- | ---------------------------- |
| `street`     | String   | Street and house number      |
| `postalCode` | String   | Postal code                  |
| `city`       | String   | City                         |
| `region`     | String   | State/canton (ISO 3166-2)    |
| `country`    | String   | Country (ISO 3166-1 alpha-2) |

**Example:**

```jsonc
"dp_residence_address": {
  "name": "Wohnadresse",
  "description": "Hauptwohnsitz des Antragstellers",
  "type": "address",
  "validation": {
    "required": true
  },
  "binding": {
    "type": "input"
  }
}
```

### Identifier Type

The `identifier` type is used for official identifiers. The `format` field SHOULD specify the type
of identifier:

| **Format**       | **Description**            | **Example Value** |
| ---------------- | -------------------------- | ----------------- |
| `taxId`          | Tax identification number  | `"12345678901"`   |
| `vatId`          | VAT ID                     | `"DE123456789"`   |
| `socialSecurity` | Social security number     | `"12345678A123"`  |
| `passport`       | Passport number            | `"C01X00T47"`     |
| `nationalId`     | National ID card number    | `"L01X00T47"`     |
| `commercial`     | Commercial register number | `"HRB 12345"`     |
| `custom`         | User-defined               | Arbitrary         |

**Example:**

```jsonc
"dp_tax_id": {
  "name": "Steuer-ID",
  "description": "Deutsche Steueridentifikationsnummer",
  "type": "identifier",
  "format": "taxId",
  "validation": {
    "required": true,
    "pattern": "^[0-9]{11}$"
  },
  "binding": {
    "type": "input"
  }
}
```

### Enum Type

The `enum` type allows selection from a predefined value list. The `options` field MUST define the
permitted values:

```jsonc
"dp_marital_status": {
  "name": "Familienstand",
  "type": "enum",
  "options": [
    {
      "value": "single",
      "label": "Ledig"
    },
    {
      "value": "married",
      "label": "Verheiratet"
    },
    {
      "value": "divorced",
      "label": "Geschieden"
    },
    {
      "value": "widowed",
      "label": "Verwitwet"
    }
  ],
  "binding": {
    "type": "input"
  }
}
```

**Note:** The `options` array MUST contain at least one entry. Each entry MUST contain a `value`
field and SHOULD contain a `label` field for display purposes ([`DP-06`](../08-validation/index.md#rule-dp-06)).

### Usage Notes

**Currency:**

- The `currency` type MUST be used together with the `unit` field ([`DP-05`](../08-validation/index.md#rule-dp-05))
- The unit SHOULD conform to the ISO 4217 currency code (e.g., `"EUR"`, `"USD"`, `"CHF"`)

```jsonc
"dp_loan_amount": {
  "name": "Kreditsumme",
  "type": "currency",
  "unit": "EUR",
  "binding": {
    "type": "input"
  }
}
```

**Duration:**

- Time durations MUST be specified in ISO 8601 Duration format
- Format: `P[n]Y[n]M[n]DT[n]H[n]M[n]S`

| **Example**  | **Meaning**                |
| ------------ | -------------------------- |
| `"P1Y"`      | 1 year                     |
| `"P6M"`      | 6 months                   |
| `"P30D"`     | 30 days                    |
| `"PT24H"`    | 24 hours                   |
| `"P2Y3M15D"` | 2 years, 3 months, 15 days |

**Date and DateTime:**

- `date` MUST conform to the format `YYYY-MM-DD`
- `datetime` MUST conform to the ISO 8601 format and SHOULD include a timezone

**Time:**

- Times MUST be specified in the format `HH:MM:SS` (ISO 8601)
- The seconds component MAY be omitted: `"14:30"` is valid

**Integer:**

- The `integer` type allows positive and negative integers
- For non-negative integers (counts), `count` SHOULD be used instead

**Count:**

- The `count` type MUST be a non-negative integer
- Typical usage: number of children, number of employees, etc.

```jsonc
"dp_children_count": {
  "name": "Anzahl Kinder",
  "type": "count",
  "validation": {
    "min": 0,
    "max": 20
  },
  "binding": {
    "type": "input"
  }
}
```

**URL:**

- URLs MUST conform to the RFC 3986 format
- Tools SHOULD NOT check reachability at validation time

### 4.7.2 Binding Types

The `binding` field of a DataPoint indicates how the data should be obtained at runtime. It serves
as a hint for the executing tool and enables clear categorization of data sources.

### Basic Structure

```jsonc
"binding": {
  "type": "input"
}
```

### Binding Types

| **Type**   | **Description**                                        | **Tool Behavior**                                          |
| ---------- | ------------------------------------------------------ | ---------------------------------------------------------- |
| `input`    | User input required                                    | Tool generates form field or chatbot question              |
| `external` | External data source                                   | Tool displays configuration dialog for data source         |
| `computed` | Derived from other DataPoints via a JSONata expression | Tool computes the value at evaluation time — no user input |

### Input Binding

The `input` type signals that this value must be entered by the user. The tool SHOULD automatically
generate an appropriate input element based on the DataPoint schema.

```jsonc
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
```

**Optional fields for input binding:**

| **Field**      | **Type** | **Description**                                                 |
| -------------- | -------- | --------------------------------------------------------------- |
| `hint`         | String   | MAY contain a hint text for the user ([`DP-09`](../08-validation/index.md#rule-dp-09))             |
| `placeholder`  | String   | MAY contain placeholder text for the input field ([`DP-09`](../08-validation/index.md#rule-dp-09)) |
| `defaultValue` | Any      | MAY provide a default value ([`DP-09`](../08-validation/index.md#rule-dp-09))                      |

**Example with optional fields:**

```jsonc
"binding": {
  "type": "input",
  "hint": "Bitte geben Sie Ihr Brutto-Jahreseinkommen an",
  "placeholder": "z.B. 45000",
  "defaultValue": 0
}
```

### External Binding

The `external` type signals that this value is obtained from an external source. The tool MUST
provide the user with a way to configure the data source.

```jsonc
"dp_credit_score": {
  "name": "Bonitätsscore",
  "type": "number",
  "binding": {
    "type": "external",
    "ref": "schufa_api",
    "description": "SCHUFA-Schnittstelle zur Bonitätsprüfung"
  }
}
```

**Required fields for external binding:**

| **Field** | **Type** | **Description**                                                     |
| --------- | -------- | ------------------------------------------------------------------- |
| `ref`     | String   | MUST contain a symbolic reference to the data source ([`DP-10`](../08-validation/index.md#rule-dp-10)) |

**Optional fields for external binding:**

| **Field**     | **Type** | **Description**                                                                             |
| ------------- | -------- | ------------------------------------------------------------------------------------------- |
| `description` | String   | MAY contain a description of the expected data source ([`DP-09`](../08-validation/index.md#rule-dp-09))                        |
| `sourceType`  | Enum     | MAY specify the type of source: `"api"`, `"database"`, `"file"`, `"rulemap"` ([`DP-09`](../08-validation/index.md#rule-dp-09)) |
| `fallback`    | Object   | MAY define an alternative binding if the external source is unavailable ([`DP-09`](../08-validation/index.md#rule-dp-09))      |

**Example with fallback:**

```jsonc
"binding": {
  "type": "external",
  "ref": "schufa_api",
  "description": "SCHUFA-Schnittstelle",
  "sourceType": "api",
  "fallback": {
    "type": "input",
    "hint": "Automatische Abfrage nicht verfügbar. Bitte manuell eingeben."
  }
}
```

**Tool workflow for external bindings:**

1. When loading the RUML file, the tool collects all `external` bindings
2. The tool displays an overview: "The following data sources must be configured:"
3. For each `ref`, the tool enables assignment to a concrete data source
4. The assignment is stored in the tool configuration, NOT in the RUML file

### Complete Example

```jsonc
"data": {
  "dp_annual_income": {
    "name": "Jahreseinkommen",
    "type": "currency",
    "unit": "EUR",
    "binding": {
      "type": "input",
      "hint": "Brutto-Jahreseinkommen"
    },
    "validation": {
      "required": true,
      "min": 0
    }
  },
  "dp_credit_score": {
    "name": "Bonitätsscore",
    "type": "number",
    "binding": {
      "type": "external",
      "ref": "schufa_api",
      "description": "SCHUFA-Schnittstelle",
      "fallback": {
        "type": "input"
      }
    }
  }
}
```

### Computed Binding

The `computed` type derives the value from **other DataPoints** via a JSONata expression. A
calculation result thereby becomes a named, typed value — e.g. a monetary amount for a legal
consequence, a deadline date, or a value for a notice. Unlike `ruml:query`, which yields a **truth
value** for a node, a computed DataPoint yields a **value** that other capabilities can consume
(e.g. document templates, text snippets).

```jsonc
"dp_einkommensteuer": {
  "name": "Festzusetzende Einkommensteuer",
  "type": "currency",
  "unit": "EUR",
  "binding": {
    "type": "computed",
    "expression": "(dp_zve - 11604) * 0.14"
  }
}
```

**Fields for computed binding:**

| **Field**     | **Type** | **Description**                                                                                |
| ------------- | -------- | ---------------------------------------------------------------------------------------------- |
| `expression`  | String   | MUST contain a JSONata expression ([`DP-11`](../08-validation/index.md#rule-dp-11)). Other DataPoints are referenced by their ID. |
| `description` | String   | MAY describe the calculation ([`DP-09`](../08-validation/index.md#rule-dp-09))                                                    |

**Rules:**

- The computed value MUST conform to the DataPoint's `type` and `validation`.
- The expression MAY reference other DataPoints, including other computed ones; references MUST NOT
  be cyclic (directly or transitively) ([`DP-11`](../08-validation/index.md#rule-dp-11), [`DP-12`](../08-validation/index.md#rule-dp-12)).
- Tools MUST NOT request user input for a computed DataPoint — the value is determined at evaluation
  time.

### 4.7.3 Validation

The optional `validation` field of a DataPoint defines rules for checking entered or obtained data
values at runtime. Tools SHOULD apply these rules before a value is used in the decision logic.

### Basic Structure

```jsonc
"validation": {
  "required": true,
  "min": 0,
  "max": 100000,
  "message": "Bitte geben Sie einen gültigen Wert ein"
}
```

### Validation Rules

| **Rule**    | **Type**         | **Description**                                              |
| ----------- | ---------------- | ------------------------------------------------------------ |
| `required`  | Boolean          | If `true`, a value MUST be present                           |
| `min`       | Number or String | Minimum value; its type depends on the data type (see Notes) |
| `max`       | Number or String | Maximum value; its type depends on the data type (see Notes) |
| `minLength` | Integer          | Minimum character length (see Notes)                         |
| `maxLength` | Integer          | Maximum character length (see Notes)                         |
| `pattern`   | String           | Regular expression for format validation                     |
| `enum`      | Array            | List of permitted values                                     |
| `message`   | String           | Custom error message                                         |

### Applicability by Data Type

| **Data Type** | **Applicable Rules**                                               |
| ------------- | ------------------------------------------------------------------ |
| `string`      | `required`, `minLength`, `maxLength`, `pattern`, `enum`, `message` |
| `number`      | `required`, `min`, `max`, `enum`, `message`                        |
| `boolean`     | `required`, `message`                                              |
| `date`        | `required`, `min`, `max`, `message`                                |
| `datetime`    | `required`, `min`, `max`, `message`                                |
| `time`        | `required`, `min`, `max`, `message`                                |
| `integer`     | `required`, `min`, `max`, `enum`, `message`                        |
| `currency`    | `required`, `min`, `max`, `message`                                |
| `percentage`  | `required`, `min`, `max`, `message`                                |
| `duration`    | `required`, `min`, `max`, `message`                                |
| `email`       | `required`, `pattern`, `message`                                   |
| `phone`       | `required`, `pattern`, `message`                                   |
| `location`    | `required`, `enum`, `message`                                      |
| `identifier`  | `required`, `minLength`, `maxLength`, `pattern`, `message`         |
| `iban`        | `required`, `pattern`, `message`                                   |
| `count`       | `required`, `min`, `max`, `message`                                |
| `url`         | `required`, `pattern`, `message`                                   |
| `address`     | `required`, `message`                                              |
| `enum`        | `required`, `message`                                              |
| `object`      | `required`, `message`                                              |

A `validation` rule MUST NOT be used with a data type the table does not list it for ([`DP-04`](../08-validation/index.md#rule-dp-04)).

### Examples

**Required field with value range:**

```jsonc
"dp_annual_income": {
  "name": "Jahreseinkommen",
  "type": "currency",
  "unit": "EUR",
  "validation": {
    "required": true,
    "min": 0,
    "max": 10000000,
    "message": "Bitte geben Sie ein gültiges Jahreseinkommen an"
  },
  "binding": {
    "type": "input"
  }
}
```

**Text field with length restriction and pattern:**

```jsonc
"dp_postal_code": {
  "name": "Postleitzahl",
  "type": "string",
  "validation": {
    "required": true,
    "minLength": 5,
    "maxLength": 5,
    "pattern": "^[0-9]{5}$",
    "message": "Bitte geben Sie eine gültige deutsche Postleitzahl ein"
  },
  "binding": {
    "type": "input"
  }
}
```

**Selection from permitted values:**

```jsonc
"dp_country": {
  "name": "Land",
  "type": "location",
  "format": "country",
  "validation": {
    "required": true,
    "enum": ["DE", "AT", "CH"],
    "message": "Diese Regelung gilt nur für Deutschland, Österreich und die Schweiz"
  },
  "binding": {
    "type": "input"
  }
}
```

**Date range:**

```jsonc
"dp_birth_date": {
  "name": "Geburtsdatum",
  "type": "date",
  "validation": {
    "required": true,
    "min": "1900-01-01",
    "max": "2010-12-31",
    "message": "Das Geburtsdatum muss zwischen 1900 und 2010 liegen"
  },
  "binding": {
    "type": "input"
  }
}
```

**Identifier with format validation:**

```jsonc
"dp_vat_id": {
  "name": "Umsatzsteuer-ID",
  "type": "identifier",
  "format": "vatId",
  "validation": {
    "required": false,
    "pattern": "^DE[0-9]{9}$",
    "message": "Bitte geben Sie eine gültige deutsche USt-ID ein (Format: DE123456789)"
  },
  "binding": {
    "type": "input"
  }
}
```

### Notes

**Pattern:**

- The `pattern` field MUST contain a valid regular expression ([`DP-13`](../08-validation/index.md#rule-dp-13))
- The expression is matched against the entire value (implicit `^...$`)
- Tools MUST support ECMAScript-compatible regular expressions (ECMA-262)

**Min and Max:**

`min` and `max` MUST have the type listed for their data type ([`DP-14`](../08-validation/index.md#rule-dp-14)):

| **Data Type**                                 | **Type of `min` and `max`**                                                                                     | **Example**                   |
| --------------------------------------------- | --------------------------------------------------------------------------------------------------------------- | ----------------------------- |
| `number`, `integer`, `currency`, `percentage` | Number                                                                                                          | `0`                           |
| `count`                                       | Non-negative integer                                                                                            | `1`                           |
| `date`                                        | String, a `full-date` as defined in [RFC 3339, section 5.6](https://www.rfc-editor.org/rfc/rfc3339#section-5.6) | `"1900-01-01"`                |
| `datetime`                                    | String, a date and time in the format `YYYY-MM-DDTHH:MM`, optionally with seconds, a fraction and an offset     | `"2024-01-01T08:00:00+01:00"` |
| `time`                                        | String, a time in the format `HH:MM` or `HH:MM:SS`, optionally with a fraction of a second and an offset        | `"08:00"`, `"17:30:00+01:00"` |
| `duration`                                    | String, an ISO 8601 duration                                                                                    | `"P18Y"`                      |

- A `datetime` or `time` bound needs no offset, just as a `datetime` or `time` value needs none (see
  [4.7.1](#471-data-types)).
- Tools MUST compare dates, times and durations by their value, not as strings.

**MinLength and MaxLength:**

- `minLength` and `maxLength` MUST be integers from 0 to 2<sup>53</sup> − 1, the range of integers
  that JSON implementations exchange reliably
  ([RFC 8259, section 6](https://www.rfc-editor.org/rfc/rfc8259#section-6)) ([`DP-08`](../08-validation/index.md#rule-dp-08)).

**Enum in Combination with Other Rules:**

- If `enum` is defined, the value MUST be contained in the list
- Other rules such as `min`, `max`, `pattern` are checked additionally

**Message:**

- If `message` is not defined, the tool SHOULD generate a default error message
- The message SHOULD help the user correct the error

### 4.7.4 Sets (Reusable Structured Types)

A **set** is a reusable, named structure — a group of DataPoints that belong together (a person, an
employment, a bank account) or a section of inputs in a questionnaire. Sets solve the fact that
`data` is otherwise a flat map with no grouping.

The pattern separates **definition** from **use**:

- A **set** (the reusable template) is defined once in the `sets` registry.
- An **object** (an instance) is a DataPoint of `type: "object"` that references a set.

#### Defining sets

Set types are declared in the `sets` object of the `ruml:datapoints` capability, keyed by their id:

```jsonc
"sets": {
  "set_person": {
    "name": "Person",
    "fields": {
      "dp_vorname": {
        "name": "Vorname",
        "type": "string",
        "binding": {
          "type": "input"
        }
      },
      "dp_nachname": {
        "name": "Nachname",
        "type": "string",
        "binding": {
          "type": "input"
        }
      },
      "dp_geburtsdatum": {
        "name": "Geburtsdatum",
        "type": "date",
        "binding": {
          "type": "input"
        }
      },
      "dp_beschaeftigung": {
        "name": "Beschäftigung",
        "type": "object",
        "set": "set_beschaeftigung",
        "binding": {
          "type": "input"
        }
      }
    }
  },
  "set_beschaeftigung": {
    "name": "Beschäftigung",
    "fields": {
      "dp_arbeitgeber": {
        "name": "Arbeitgeber",
        "type": "string",
        "binding": {
          "type": "input"
        }
      },
      "dp_beginn": {
        "name": "Beginn der Beschäftigung",
        "type": "date",
        "binding": {
          "type": "input"
        }
      },
      "dp_nettoeinkommen": {
        "name": "Monatliches Nettoeinkommen",
        "type": "currency",
        "unit": "EUR",
        "validation": {
          "min": 0
        },
        "binding": {
          "type": "input"
        }
      }
    }
  }
}
```

| **Field**     | **Type** | **Description**                                                                                                          |
| ------------- | -------- | ------------------------------------------------------------------------------------------------------------------------ |
| `name`        | String   | MUST contain a display name for the set ([`DP-15`](../08-validation/index.md#rule-dp-15))                                                                   |
| `fields`      | Object   | MUST contain the member DataPoints, keyed by their ids. A field MAY itself be `type: "object"` (nesting) ([`DP-15`](../08-validation/index.md#rule-dp-15)). |
| `description` | String   | MAY describe the set ([`DP-15`](../08-validation/index.md#rule-dp-15))                                                                                      |

#### Using sets

A DataPoint instantiates a set with `type: "object"` and a `set` reference:

```jsonc
"data": {
  "dp_antragsteller": {
    "name": "Antragsteller",
    "type": "object",
    "set": "set_person",
    "binding": {
      "type": "input"
    }
  },
  "dp_buergen": {
    "name": "Bürgen",
    "type": "object",
    "set": "set_person",
    "cardinality": {
      "min": 0,
      "max": 3
    },
    "binding": {
      "type": "input"
    }
  }
}
```

- **`set`** MUST reference an id declared in `sets` ([`DP-16`](../08-validation/index.md#rule-dp-16)).
- **`cardinality`** (`{ min, max }`) controls repetition: absent → a single object; `max > 1` → a
  list of objects (e.g. a questionnaire "add another" list, FIM _Multiplizität_).
- **Nesting:** because a `fields` entry may itself be `type: "object"`, sets compose (in the
  example, `set_person` has a `set_beschaeftigung` field).

#### Referencing fields

Fields inside an object are referenced by path (JSONata) from the DataPoint id, e.g.
`dp_antragsteller.dp_geburtsdatum` in a `ruml:query` expression. For a repeated object
(`cardinality.max > 1`) the value is an array and members are indexed, e.g.
`dp_buergen[0].dp_nachname`.

**Rules:**

- Every `set` reference MUST resolve to an id in `sets` ([`DP-16`](../08-validation/index.md#rule-dp-16)).
- Set `fields` keys and set ids MUST match the pattern `[a-z_][a-z0-9_]*` ([`DP-02`](../08-validation/index.md#rule-dp-02)).
- Set definitions MAY nest but MUST NOT be recursive (a set MUST NOT reference itself directly or
  transitively) ([`DP-17`](../08-validation/index.md#rule-dp-17)).

## Conformance tests

- [4.7 DataPoints](../../../tests/04-capabilities/4-7-data-points.test.yaml)
