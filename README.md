# RUML – Rulemapping Logic Format

RUML is an open, JSON-based file format for the machine-executable representation of legal
decision logic. A RUML file holds a rulemap: the conditions of a legal norm or a decision as
a tree of nodes, together with the data it needs and the text it is derived from.

This repository is the home of the format: the specification, its JSON Schemas and its
conformance tests. The specification is published at [ruml.org](https://ruml.org); the
[releases](https://github.com/Law-as-Code-Institute/ruml/releases) list the versions.

| Folder | Contents |
| --- | --- |
| [`spec/`](spec/en/index.md) | The specification, in English (`en/`) and German (`de/`) |
| [`schemas/`](schemas/README.md) | The JSON Schemas for `.ruml`, `.ruml-result` and `.ruml-ext` files |
| [`tests/`](spec/en/appendix/A-spec-tests/index.md) | The conformance tests: descriptors and fixtures per chapter |
| `packages/` | The packaging of the schemas for npm and Python |

## Reading the specification

Start with [`spec/en/index.md`](spec/en/index.md) or, in German,
[`spec/de/index.md`](spec/de/index.md). Each page shows its examples inline; the complete
example files are next to the pages, in the `*.examples/` folders. The validation rules, with
their identifiers, are in [chapter 8](spec/en/08-validation/index.md).

## Using the schemas

The schemas are the files in [`schemas/`](schemas/); [`schemas/README.md`](schemas/README.md)
says how to validate with them. Each release also publishes them as packages.

**Python**, from PyPI:

```sh
pip install ruml-schema
```

```python
from ruml_schema import load_ruml_schema, load_ruml_result_schema, load_ruml_ext_schema

schema = load_ruml_schema()
```

**JavaScript and TypeScript**, from npm:

```sh
npm install @law-as-code/ruml-schema
```

```js
import schema from "@law-as-code/ruml-schema" with { type: "json" };
import resultSchema from "@law-as-code/ruml-schema/result" with { type: "json" };
import extSchema from "@law-as-code/ruml-schema/ext" with { type: "json" };
```

## Testing an implementation

The conformance tests in `tests/` are data: a test names a RUML file and what a conformant
implementation makes of it. Validation tests say whether a file is accepted or rejected, and
by which rule; evaluation tests say what an evaluation yields for given inputs.
[Appendix A](spec/en/appendix/A-spec-tests/index.md) describes the suite and the
[runner contract](spec/en/appendix/A-spec-tests/runner-contract.md) how to run it;
`tests/schema/` holds the schema of the test descriptors.

## Parsers

| Language | Repository |
| --- | --- |
| TypeScript | [ruml-js](https://github.com/Law-as-Code-Institute/ruml-js) |
| Python | [ruml-python](https://github.com/Law-as-Code-Institute/ruml-python) |

## Contributing

Feedback is welcome as issues; pull requests are not accepted yet. See
[CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

The specification text in `spec/` is licensed under CC BY-SA 4.0. Everything else – the
schemas, the tests, the packages and the examples inside `spec/` – is licensed under
Apache-2.0. [LICENSE.md](LICENSE.md) and `REUSE.toml` state this per path; the licence texts
are in `LICENSES/`.

RUML is a trademark of Rulemapping Group GmbH; an application for registration as an EU trade
mark has been filed.

Published by Law as Code Institut GmbH. Copyright 2026 Rulemapping Group GmbH.
