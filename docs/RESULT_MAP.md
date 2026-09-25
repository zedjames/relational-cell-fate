# Manuscript result map

This map points from major manuscript result surfaces to the released artifacts that reproduce or verify them. It is intentionally paper-specific.

| Manuscript result | Public artifact(s) | Public check / regeneration |
| --- | --- | --- |
| ReSisTrace eight condition–replicate strata retain mixed future-observation fibers | `results/resistrace/recovery_matrix.csv` | `analysis/verify_release.py`; Figure 2 via `analysis/regenerate_figures.py` |
| Rewind positive-fate nonrecovery; 9-gene state = 86 fibers, 71 pure, 15 mixed, residual 18 | `results/rewind/recovery_matrix.csv` | `analysis/verify_release.py` |
| Rewind permutation control | `results/rewind/fate_permutation.csv` | `analysis/verify_release.py`; Figure 2 |
| Watermelon instantaneous residuals | `results/watermelon/temporal_residuals.csv` | `analysis/verify_release.py`; Figure 3 |
| Watermelon exact history at lineage-identifying resolution | `results/watermelon/history_summary.csv` | Figure 3 |
| Watermelon compression boundary | `results/watermelon/compression_pareto_frontier.csv` | `analysis/verify_release.py`; Figure 4 |
| Watermelon paired terminal realization: 1,550 lineages; 837 concordant / 713 discordant; 190 raw fates | `results/watermelon/paired_replicate_fates.csv` | `analysis/verify_release.py`; Figure 5 |
| Persistent fate filtration | `results/watermelon/critical_support_levels.csv` | `analysis/verify_release.py`; persistence figures |
| Marginal-preserving whole-profile null | `results/watermelon/persistence_profile_nulls.csv` | released null distribution |
| Sampling-depth-conditioned and alternative-fate robustness | `results/watermelon/robustness_summary.csv` | robustness panels |
| Terminal molecular persistence profile | `results/watermelon/molecular_persistence_profile.csv` | molecular figure |
| Matched random-gene molecular controls | `results/watermelon/molecular_random_gene_banks.csv` | molecular control panel |
| CellTag LSK RNA preterminal nonrecovery | `results/celltag/lsk_state_fate_recovery.csv` | `analysis/verify_release.py` |
| CellTag LSK RNA / ATAC / joint multimodal completion | `results/celltag/lsk_rna_recovery.csv`, `lsk_atac_recovery.csv`, `lsk_joint_recovery.csv` | `analysis/verify_release.py` |
| CellTag iEP snapshot and ordered-history recovery | `results/celltag/iep_snapshot_recovery.csv`, `iep_history_recovery.csv`, `iep_multimodal_history_recovery.csv` | `analysis/verify_release.py` |
| CellTag iEP cross-replicate transport authority | `results/celltag/iep_cross_replicate_state_transfer.csv` | `analysis/verify_release.py` |
| 3 systems / 54 families / 958 surfaces / 849 canonical partitions | `results/cross_carrier/decision.json`, `synthesis_families.csv` | `analysis/verify_release.py` |
| 352 injective exact; 18 noninjective exact; 0 control-qualified noninjective exact | `results/cross_carrier/fingerprint_surfaces.csv`, `shared_exact_surfaces.csv`, `decision.json` | `analysis/verify_release.py`; Figure 8 |
| Cross-carrier identity–future geometry and fate-selective surplus | `results/cross_carrier/phase_plane_data.csv`, `biological_systems.csv` | Figure 8 |

## One-command checks

```bash
make verify
make setup
make figures
```

`make verify` uses only the Python standard library. Figure regeneration additionally installs the small plotting dependency set declared in `analysis/requirements.txt`.
