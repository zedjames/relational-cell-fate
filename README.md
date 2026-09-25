# Relational Cell Fate

Reproducibility materials for **“Relational Anatomy of Cell Fate Across Lineage-Resolved Perturbation Experiments.”**

## Purpose

This repository is the public, paper-specific reproducibility record for the accompanying manuscript. It contains the finite data products, result tables, controls, figure inputs, validation scripts, provenance records, and release manifests needed to reproduce and inspect the reported empirical results.

It is **not** a public release of the private research environment in which the work was developed, and it does not distribute the broader formal calculus, unrelated theorem libraries, research orchestration, or other private research programs.

The intended reproducibility direction is:

```
public source data
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

A frozen manuscript PDF and source will be added at the release freeze corresponding to the archival DOI.

## What this repository will let a reader reproduce

The release is organized to reproduce or independently check the numerical results underlying:

- ReSisTrace preterminal state / future-observation geometry;
- Rewind positive-resistant fate fibers and permutation controls;
- Watermelon snapshot, history, compression, repeated-realization, persistence, and molecular analyses;
- CellTag-multi hematopoietic RNA/ATAC/multimodal state comparisons;
- CellTag-multi reprogramming temporal-history and cross-replicate authority analyses;
- the cross-carrier identity–future synthesis, including the registered surface census and fate-selective surplus.

## Repository boundary

This repository exposes only the material needed for this paper. It does **not** contain the private development repository, its tier architecture, generic research-generation machinery, or reusable implementation of the broader calculus.

Formal checking performed in the private research environment is reported as verification metadata in the release record. Public reproducibility is centered on the empirical computations and paper-specific validation artifacts.

## Structure

```
analysis/        paper-specific reproduction / validation code
data/            source manifest and release-level derived inputs
docs/            provenance, release boundary, and reproducibility guide
manuscript/      frozen manuscript artifacts at release
results/         frozen result tables and figure inputs
```

## Source data

Third-party raw datasets are not mirrored here by default. `data/source_manifest.tsv` records public accessions, publications, and source-code authority. The release will include deterministic acquisition / preprocessing instructions and paper-specific derived artifacts where redistribution is appropriate.

## Citation and archival release

`CITATION.cff` identifies the manuscript release. The archival DOI assigned to this work is **10.5281/zenodo.22969066**. The DOI-backed release is the immutable computational companion to the preprint.

## Status

**Release preparation in progress.** The current repository is being populated from the frozen analysis authority used for the manuscript.
