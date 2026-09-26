# v1.0-preprint

Public reproducibility release for:

**Relational Anatomy of Cell Fate Across Lineage-Resolved Perturbation Experiments**  
*A finite relational calculus for state, identity, history, and fate across biological systems*

**Manuscript DOI:** 10.5281/zenodo.22969066

## Release purpose

This release freezes the paper-specific public reproducibility surface corresponding to the published preprint. It contains the empirical result tables, controls, provenance metadata, validation scripts, source-acquisition helper, figure-regeneration workflow, and release manifest required to reproduce or inspect the manuscript's reported numerical results.

The broader private research environment and general-purpose formal calculus are not distributed.

## Reproduction

```bash
make verify
make setup
make figures
```

The release verifier checks the manuscript-facing numerical results from the frozen public artifacts. Figure regeneration rebuilds the empirical manuscript figure assets from those released tables.

## Manuscript

The authoritative manuscript copy is archived on Zenodo:

https://doi.org/10.5281/zenodo.22969066

A PDF need not be duplicated in the repository release; Zenodo remains the manuscript source of record.


## Licensing

See `LICENSE.md`.

- manuscript-related material, figures, documentation, and original derived result tables: CC BY-NC-ND 4.0;
- paper-specific executable scripts and build helpers: PolyForm Noncommercial 1.0.0;
- third-party datasets remain under their original terms.
