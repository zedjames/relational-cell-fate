# Published manuscript

This directory contains the manuscript corresponding to:

**Relational Anatomy of Cell Fate Across Lineage-Resolved Perturbation Experiments**  
*A finite relational calculus for state, identity, history, and fate across biological systems*

**DOI:** 10.5281/zenodo.22969066

Files:

- `Relational_Anatomy_of_Cell_Fate.pdf` — exact published manuscript PDF;
- `Relational_Anatomy_of_Cell_Fate.tex` — manuscript source corresponding to the published text.

The empirical figure assets referenced by the manuscript are regenerated from the public result artifacts with:

```bash
make setup
make figures
```

Generated figures are written to `manuscript/figures/`.
