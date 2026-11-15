<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.1 Overview

### Dual-Mode Concept

RUML files exist in two modes:

| Mode          | Format | File Extension                       | Purpose                                            |
| ------------- | ------ | ------------------------------------ | -------------------------------------------------- |
| **Bare**      | JSON   | `.ruml`, `.ruml-ext`, `.ruml-result` | Development, drafting, embedding in other systems  |
| **Container** | ZIP    | `.rumlc`                             | Distribution, archiving, legally binding documents |

Container files use the extension `.rumlc`. Bare files retain their original extensions (`.ruml`,
`.ruml-ext`, `.ruml-result`).

**Bare mode:** The file is plain JSON without integrity layers. For development and drafting — no
hash, no signature, no encryption.

**Container mode:** The file is a ZIP archive containing the JSON document together with hash,
signature, and encryption data. Each integrity layer is optional — a container MAY contain any
combination of them, e.g. just hashes, just signatures, or all three layers.

### File Types in a Container

A container MAY contain arbitrary combinations of the following file types:

| Type        | Description                             | Manifest Type |
| ----------- | --------------------------------------- | ------------- |
| RUML        | Rulemap (core structure)                | `ruml`        |
| RUML-EXT    | Sidecar file with capability data       | `ruml-ext`    |
| RUML-Result | Evaluation result                       | `ruml-result` |
| Asset       | Arbitrary file (PDF, text, image, etc.) | `asset`       |

There is no restriction on which combinations are permitted:

- A container with only a rulemap is valid
- A container with only an EXT file is valid (the base rulemap is referenced via `$base`)
- A container with a rulemap + multiple result files is valid
- A container with multiple versions of the same rulemap is valid

### Design Principles

1. **Layers are independent:** Each file in the container MAY be independently hashed, signed, and
   encrypted — including the manifest itself.
2. **Formats are declarative:** The manifest declares which algorithms and formats are used. The
   container does not prescribe a specific cryptography implementation.
3. **Bare is always valid:** A bare JSON file is a fully valid RUML file. The container adds layers
   but does not change the content.
