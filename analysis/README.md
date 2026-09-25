# Analysis

This directory contains only paper-specific reproduction and validation code. It is intentionally not a general implementation of the relational calculus.

## Quick start

```bash
make verify
make setup
make figures
```

- `verify_release.py` checks the manuscript-facing numerical results against the frozen released artifacts using only the Python standard library.
- `regenerate_figures.py` rebuilds the empirical PDF figure assets used by the manuscript from the public result tables.
- `acquire_public_sources.py` retrieves public GEO source authority and the frozen upstream CellTag-multi code commit; raw GEO archives are optional because they are large.

See `../docs/RESULT_MAP.md` for the claim-to-artifact map and `../docs/RELEASE_BOUNDARY.md` for the explicit public/private boundary.
