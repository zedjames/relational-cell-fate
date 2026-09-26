# Manuscript record

The published manuscript associated with this reproducibility repository is:

**Relational Anatomy of Cell Fate Across Lineage-Resolved Perturbation Experiments**  
*A finite relational calculus for state, identity, history, and fate across biological systems*

**DOI:** 10.5281/zenodo.22969066

The archival manuscript PDF is maintained in the Zenodo record above. This GitHub repository is the accompanying public reproducibility record for the empirical computations reported in that manuscript.

The manuscript's empirical figure assets are regenerated from the released result artifacts with:

```bash
make setup
make figures
```

Generated figures are written to `manuscript/figures/`.

The manuscript archive and this repository therefore have distinct roles:

```
Zenodo DOI  -> archival paper
GitHub repo -> reproducibility materials
```
