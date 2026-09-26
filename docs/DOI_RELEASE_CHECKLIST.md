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
- [x] Add the published manuscript PDF and source.
- [x] Finalize licensing for scholarly content and paper-specific code.
- [x] Add the manuscript DOI to repository metadata.
- [x] Add a claim-to-artifact result map.
- [x] Generate the release checksum / artifact manifest.
- [x] Run the release verification workflow on the frozen artifact state.

## Release principle

The public release reproduces the paper's computations and evidence surface. It does not expose the private research environment or provide a reusable implementation of the broader calculus.

## Optional repository convenience step

A GitHub release/tag such as `v1.0-preprint` may be created for navigation, but the scholarly manuscript archive is already identified by DOI **10.5281/zenodo.22969066**.
