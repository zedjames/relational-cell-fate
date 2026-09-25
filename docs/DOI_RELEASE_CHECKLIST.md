# DOI release checklist

This repository remains a pre-release reproducibility workspace until the manuscript and public artifacts are frozen together.

## Before the archival DOI

- [x] Define the public/private release boundary.
- [x] Add source accession and upstream-code authority.
- [x] Publish paper-facing frozen result artifacts for the principal manuscript claims.
- [x] Add an automated numerical verification script.
- [x] Run the numerical verifier in GitHub Actions.
- [x] Add paper-specific figure regeneration from released result artifacts.
- [ ] Complete source-reconstruction instructions / hashes for every source file used in the final release.
- [ ] Add final manuscript source, PDF, and final figure set.
- [ ] Choose the license for this public paper-specific code and derived artifacts.
- [ ] Generate the final SHA-256 artifact manifest.
- [ ] Run the final clean-room verification workflow from the frozen tag.
- [ ] Create the GitHub release tag (recommended: `v1.0-preprint`).
- [ ] Archive that exact tag in the DOI-granting repository.
- [ ] Add the DOI to `README.md`, `CITATION.cff`, and the manuscript.
- [ ] Replace the manuscript's planned-supplement inventory with the final repository/DOI reproducibility statement.

## Release principle

The DOI archive should reproduce the paper's computations and evidence surface. It should not expose the private research environment or provide a reusable implementation of the broader calculus.
