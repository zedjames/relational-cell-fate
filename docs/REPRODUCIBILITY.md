# Reproducibility guide

The public release is designed around two levels of checking.

## Level 1 — reproduce manuscript numerics from frozen derived artifacts

This is the primary release target. A reader should be able to recompute the reported carrier counts, state/future collision geometry, residuals, permutation summaries, persistence statistics, molecular summaries, cross-carrier identity/future metrics, tables, and figure inputs from the frozen paper-specific derived files.

## Level 2 — reconstruct derived artifacts from public sources

Where source size and licensing permit, acquisition and preprocessing instructions will reconstruct the paper-specific finite inputs from the original public data. Raw third-party data are generally retrieved from their original repositories rather than mirrored here.

## Formal verification

Formal verification was performed in the private research environment. The public release will provide verification metadata and frozen hashes sufficient to identify the checked manuscript statements and release state, without distributing the broader private formal-development environment.

## Release freeze

The DOI-backed release will freeze:

- manuscript source and PDF;
- source and artifact manifests;
- paper-specific derived data;
- analysis / validation scripts;
- controls and deterministic seeds;
- figure inputs and outputs;
- final validation receipt.
