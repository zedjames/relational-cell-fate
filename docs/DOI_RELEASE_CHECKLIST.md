# Public release checklist

This repository is the public reproducibility companion to the manuscript archived at DOI **10.5281/zenodo.22969066**.

## Completed release surface

- [x] Define the public/private release boundary.
- [x] Add source accession and upstream-code authority.
- [x] Publish paper-facing frozen result artifacts for the principal manuscript claims.
- [x] Add an automated numerical verification script.
- [x] Run the numerical verifier in GitHub Actions.
- [x] Add paper-specific figure regeneration from released result artifacts.
- [x] Add public source-acquisition support.
- [x] Link the repository to the published manuscript DOI.
- [x] Finalize licensing for scholarly content and paper-specific code.
- [x] Add a claim-to-artifact result map.
- [x] Add a release artifact manifest.
- [x] Run the release verification workflow on the finalized public state.

## Release principle

The public release reproduces the paper's computations and evidence surface. It does not expose the private research environment or provide a reusable implementation of the broader calculus.

The manuscript itself is archived on Zenodo. The GitHub repository is its computational reproducibility companion.

## Optional convenience step

A GitHub release/tag such as `v1.0-preprint` may be created for navigation, but it is not required for the scientific release architecture because the manuscript already has a stable DOI and the repository is linked directly from the paper.
