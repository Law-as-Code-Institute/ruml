<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.7 Versioning

### Single Version (Default)

In the default case, a container holds a single version of a file. Versioning is managed through the
metadata of the RUML file itself:

- `metadata.version` — the version number
- `metadata.replaces` — UUID of the replaced version
- `metadata.replacedBy` — UUID of the successor version

Each version is its own container — independently signable and distributable.

### Multiple Versions (Archive)

A container MAY contain multiple versions of the same file. This is useful for:

- **Audit archiving:** Complete version history in a single file
- **Comparison:** Old and new version side by side
- **Transition periods:** Current and previous version during a migration

Multiple versions are organized via subdirectories:

```
archive.rumlc (ZIP)
├── versions/
│   ├── 1.0/
│   │   └── rulemap.json
│   ├── 2.0/
│   │   └── rulemap.json
│   └── 2.1-draft/
│       └── rulemap.json
├── signatures/
│   └── versions/2.0/rulemap.json.sig
└── manifest.json
```

The manifest declares each version as a separate file:

```jsonc
{
  "$format": "RUML-Container",
  "$specVersion": "1.0",
  "created": "2026-03-15T10:30:00+01:00",
  "files": {
    "versions/1.0/rulemap.json": {
      "type": "ruml",
      "hash": {
        "algorithm": "sha3-256",
        "value": "1b3d5f7a9c1e3b5d7f9a1c3e5b7d9f1a3c5e7b9d1f3a5c7e9b1d3f5a7c9e1b3d"
      }
    },
    "versions/2.0/rulemap.json": {
      "type": "ruml",
      "hash": {
        "algorithm": "sha3-256",
        "value": "4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
      },
      "signature": {
        "path": "signatures/versions/2.0/rulemap.json.sig",
        "format": "jws-detached"
      }
    },
    "versions/2.1-draft/rulemap.json": {
      "type": "ruml"
    }
  }
}
```

Each version MAY be independently hashed, signed, and encrypted. An archived version without a
signature is valid — only the current, legally effective version typically requires a signature.

### Version Identification

The version identifier in the directory name (e.g., `1.0`, `2.0`, `2.1-draft`) is a human-readable
label only. Parsers MUST NOT use directory names as a source of version information. The normative
version is provided exclusively by `metadata.version` within the respective RUML file. The directory
name label SHOULD match `metadata.version` for readability, but this is not enforced.
