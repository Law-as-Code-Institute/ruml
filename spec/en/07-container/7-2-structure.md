<!-- SPDX-FileCopyrightText: 2026 Rulemapping Group GmbH -->
<!-- SPDX-License-Identifier: CC-BY-SA-4.0 -->

## 7.2 Container Structure

### ZIP Layout

A RUML container is a ZIP archive with the following structure:

```
document.rumlc (ZIP)
├── rulemap.json                          # RUML file (bare JSON)
├── ext/                                  # Sidecar files (optional)
│   └── bank.json
├── results/                              # Result files (optional)
│   └── 2026-03-15.json
├── assets/                               # Referenced files (optional)
│   ├── estg-2024.pdf
│   └── bgh-urteil.pdf
├── signatures/                           # Signature files (optional)
│   ├── rulemap.json.sig
│   └── ext/bank.json.sig
├── encrypted/                            # Encrypted files (optional)
│   └── results/2026-03-15.json.enc
└── manifest.json                         # Container index (MUST be present)
```

### Required Files

A RUML container MUST contain exactly one `manifest.json` in the root directory.

A RUML container MUST contain at least one content file (type `ruml`, `ruml-ext`, or `ruml-result`).

### Directory Conventions

| Directory     | Content                                                              |
| ------------- | -------------------------------------------------------------------- |
| Root (`/`)    | RUML files and manifest                                              |
| `ext/`        | RUML-EXT sidecar files                                               |
| `results/`    | RUML-Result files                                                    |
| `assets/`     | Referenced files (PDFs, texts, images, etc.)                         |
| `signatures/` | Signature files — path structure mirrors the source file             |
| `encrypted/`  | Encrypted versions of files — path structure mirrors the source file |

The path structure in `signatures/` and `encrypted/` MUST mirror the path structure of the source
file. Example: The signature for `ext/bank.json` is located at `signatures/ext/bank.json.sig`.

### Filename Conventions

| Layer      | Suffix | Example                                 |
| ---------- | ------ | --------------------------------------- |
| Signature  | `.sig` | `signatures/rulemap.json.sig`           |
| Encryption | `.enc` | `encrypted/results/2026-03-15.json.enc` |

### manifest.json

The manifest is the central index of the container. It describes all content files and their
integrity layers.

```jsonc
{
  "$format": "RUML-Container",
  "$specVersion": "1.0",
  "created": "2026-03-15T10:30:00+01:00",
  "files": {
    "rulemap.json": {
      "type": "ruml",
      "hash": {
        "algorithm": "sha3-256",
        "value": "4e03657aea45a94fc7d47c89e3f5a2b7c4d8e9f0a1b2c3d4e5f6a7b8c9d0e1f2"
      },
      "signature": {
        "path": "signatures/rulemap.json.sig",
        "format": "jws-detached"
      }
    },
    "ext/bank.json": {
      "type": "ruml-ext",
      "hash": {
        "algorithm": "sha3-256",
        "value": "9a1c0d5e7b3f48261e0a9c7d5b3f1e2a4c6d8f0b2a4c6e8f1a3b5c7d9e0f1a2b"
      },
      "signature": {
        "path": "signatures/ext/bank.json.sig",
        "format": "cms-detached"
      }
    },
    "results/2026-03-15.json": {
      "type": "ruml-result",
      "hash": {
        "algorithm": "sha3-256",
        "value": "c2f4a6b8d0e1f3a5c7b9d1e3f5a7c9b1d3e5f7a9c1b3d5e7f9a1c3b5d7e9f1a3"
      },
      "encryption": {
        "path": "encrypted/results/2026-03-15.json.enc",
        "format": "jwe",
        "algorithm": "RSA-OAEP-256"
      }
    },
    "assets/estg-2024.pdf": {
      "type": "asset",
      "hash": {
        "algorithm": "sha3-256",
        "value": "07b5d3f1e9c7a5b3d1f9e7c5a3b1d9f7e5c3a1b9d7f5e3c1a9b7d5f3e1c9a7b5"
      }
    },
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
  }
}
```

#### Manifest Required Fields

| Field          | Type     | Description                                                                                                                                                                                                                           |
| -------------- | -------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `$format`      | String   | MUST have the value `"RUML-Container"`                                                                                                                                                                                                |
| `$specVersion` | String   | MUST specify the spec version ([2.3](../02-file-format-basics/2-3-versioning.md#the-specversion-field))                                                                                                                               |
| `created`      | DateTime | MUST specify the creation timestamp of the container                                                                                                                                                                                  |
| `files`        | Object   | MUST contain one entry per content file. Key is the relative path of the file; for an encrypted file, the path of its plaintext. Signature files and encrypted files are referenced from these entries and have no entry of their own |

#### Fields per File Entry

| Field        | Type   | Required                          | Description                                                                                                                                              |
| ------------ | ------ | --------------------------------- | -------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `type`       | String | MUST (except for `manifest.json`) | File type: `ruml`, `ruml-ext`, `ruml-result`, or `asset`                                                                                                 |
| `uri`        | String | MAY                               | The URI of the immutable RUML version this file represents (see [Bundled RUML Files](#bundled-ruml-files)). MUST NOT be present if `type` is not `ruml`. |
| `hash`       | Object | MAY                               | Hash information (see [7.3](7-3-hashing.md))                                                                                                             |
| `signature`  | Object | MAY                               | Signature information (see [7.4](7-4-signatures.md))                                                                                                     |
| `encryption` | Object | MAY                               | Encryption information (see [7.5](7-5-encryption.md))                                                                                                    |

#### Manifest Self-Reference

The manifest MAY reference itself in the `files` object. This allows the manifest itself to be
hashed and signed. When the manifest is signed, a chain of trust is established over the entire
container content: the manifest signature protects the manifest contents, which in turn contain the
hashes of all other files.

If any content file in the container carries a `signature`, the manifest SHOULD itself be signed. An
unsigned manifest cannot protect its hashes from substitution: a party with write access to the
container can replace a file and the corresponding hash in the manifest without detection. Only a
manifest signature — requiring the private key — prevents this attack.

When computing the manifest hash, the `manifest.json` entry in the `files` object MUST be excluded —
it does not yet exist at that point. The hash is computed over the canonicalized (RFC 8785) version
of the manifest in which the key `"manifest.json"` has been removed from the `files` object.

### Bundled RUML Files

A container MAY hold several RUML files: a rulemap together with the RUML files its node anchors
point into (for example the law it implements, see
[Chapter 4.15](../04-capabilities/4-15-ruml-tree-reference.md#bundling-for-export)). Each bundled
file that is the target of node anchors MUST have the version URI it represents in its manifest
entry's `uri` field:

```json
"files": {
  "rulemap.json": { "type": "ruml" },
  "gmbhg.json": {
    "type": "ruml",
    "uri": "https://rulemapping.org/rulemapping/gmbhg:2025-01-01"
  }
}
```

Within one container, each `uri` MUST be unique. A parser resolves a node anchor against the bundled
file whose `uri` equals the anchor's RUML URI before fetching it from elsewhere.

### Validation

When opening a RUML container, a parser MUST:

1. Verify that `manifest.json` is present and contains valid JSON
2. Verify that at least one content file (type `ruml`, `ruml-ext`, or `ruml-result`) is present
3. Verify that every file the manifest lists or references exists in the container: each content
   file, or its encrypted version if the entry has `encryption`, and each signature file

A parser MUST NOT process a file that the manifest neither lists nor references, and SHOULD issue a
warning for it.

### Container Size Limits

A container SHOULD NOT exceed 1 GB in total uncompressed content size. Parsers MAY enforce lower
limits; any enforced limit MUST be documented.
