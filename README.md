# Relational Cell Fate

Public reproducibility materials for **“Relational Anatomy of Cell Fate Across Lineage-Resolved Perturbation Experiments.”**

**Manuscript DOI:** 10.5281/zenodo.22969066

## Purpose

This repository is the paper-specific reproducibility record for the accompanying manuscript. It contains the finite result tables, controls, provenance records, numerical validation code, and figure-generation workflow needed to reproduce and inspect the reported empirical results.

It is **not** a public release of the private research environment in which the work was developed. It does not distribute the broader formal calculus, unrelated theorem libraries, research orchestration, or other private research programs.

The intended reproducibility direction is:

```
public source authority
        ↓
paper-specific finite carriers / derived maps
        ↓
registered analyses and controls
        ↓
reported tables, statistics, and figures
```

## Manuscript

**Relational Anatomy of Cell Fate Across Lineage-Resolved Perturbation Experiments**  
*A finite relational calculus for state, identity, history, and fate across biological systems*

The published manuscript is archived at DOI **10.5281/zenodo.22969066**. The exact published PDF and manuscript source are included under `manuscript/`.

## What this repository lets a reader reproduce

The released artifacts support reproduction or independent checking of the numerical results underlying:

- ReSisTrace preterminal state / future-observation geometry;
- Rewind positive-resistant fate fibers and permutation controls;
- Watermelon snapshot, history, compression, repeated-realization, persistence, and molecular analyses;
- CellTag-multi hematopoietic RNA/ATAC/multimodal state comparisons;
- CellTag-multi reprogramming temporal-history and cross-replicate authority analyses;
- the cross-carrier identity–future synthesis, including the registered surface census and fate-selective surplus.

A claim-to-artifact map is provided in `docs/RESULT_MAP.md`.

## Repository boundary

This repository exposes only the material needed to reproduce and inspect this paper. It does **not** contain the private development repository, its tier architecture, generic research-generation machinery, or reusable implementation of the broader calculus.

Formal checking performed in the private research environment is reported in the manuscript as part of the development and verification history. Public reproducibility here is centered on the empirical computations and paper-specific validation artifacts.

## Quick start

```bash
make verify
make setup
make figures
```

- `make verify` checks the released manuscript-facing numerical results using only the Python standard library.
- `make setup` installs the small plotting dependency set.
- `make figures` regenerates the empirical figure assets from released result tables.

## Structure

```
analysis/        paper-specific reproduction / validation code
data/            source manifest and source-authority metadata
docs/            provenance, release boundary, result map, and release notes
manuscript/      published manuscript PDF and source
results/         frozen result tables and paper-facing derived summaries
```

## Source data

Third-party raw datasets are not mirrored here by default. `data/source_manifest.tsv` records public accessions, publications, and source-code authority. `analysis/acquire_public_sources.py` provides deterministic public-source acquisition support for the datasets used in the manuscript.

## Licensing

See `LICENSE.md`.

In summary:

- manuscript, figures, documentation, and original derived result tables: **CC BY-NC-ND 4.0**;
- paper-specific executable scripts and build helpers: **PolyForm Noncommercial 1.0.0**;
- third-party source data remain governed by their original licenses and terms.

## Release status

This repository is the public computational companion to the manuscript archived at DOI **10.5281/zenodo.22969066**. The release manifest and checksums identify the frozen paper-specific artifact state.
