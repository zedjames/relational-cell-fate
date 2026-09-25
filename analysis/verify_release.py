#!/usr/bin/env python3
"""Verify the frozen paper-facing numerical claims from released derived artifacts.

This script is intentionally paper-specific. It verifies the manuscript's reported
counts and boundaries from the public result tables; it is not a reusable
implementation of the underlying research calculus.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"


def rows(path: str):
    with (ROOT / path).open(newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition: bool, message: str) -> None:
    if not condition:
        raise AssertionError(message)


def as_bool(value: str) -> bool:
    return value == "True"


def main() -> None:
    checks = 0

    # ReSisTrace: every decision-eligible corrected-state stratum remains nonexact.
    r10 = rows("results/resistrace/recovery_matrix.csv")
    p5b = [r for r in r10 if r["package"] == "P5b_correctedBiologicalState" and as_bool(r["decision_eligible"])]
    require(len(p5b) == 8, "ReSisTrace P5b stratum count")
    checks += 1
    require(all(not as_bool(r["exact_recovery"]) and int(r["majority_residual"]) > 0 for r in p5b),
            "ReSisTrace nonrecovery boundary")
    checks += 1

    # Rewind: 13 decision-eligible packages; joint nine-gene state remains mixed.
    r11 = rows("results/rewind/recovery_matrix.csv")
    eligible11 = [r for r in r11 if as_bool(r["decision_eligible"])]
    require(len(eligible11) == 13, "Rewind decision-eligible package count")
    checks += 1
    nine = next(r for r in r11 if r["package"] == "P2_nineGeneFateBlindVector")
    require((int(nine["cell_count"]), int(nine["partition_size"]), int(nine["pure_fiber_count"]),
             int(nine["mixed_fiber_count"]), int(nine["cells_in_mixed_fibers"]),
             int(nine["majority_residual"])) == (162, 86, 71, 15, 63, 18),
            "Rewind nine-gene geometry")
    checks += 1
    perm11 = rows("results/rewind/fate_permutation.csv")
    nine_perm = next(r for r in perm11 if r["package"] == "P2_nineGeneFateBlindVector")
    require(abs(float(nine_perm["empirical_lower_tail_p"]) - 1/1001) < 1e-15,
            "Rewind permutation tail")
    checks += 1

    # Watermelon snapshot residuals.
    temporal = rows("results/watermelon/temporal_residuals.csv")
    expected = {
        ("0", "P4_twelveProjectionState"): 10,
        ("3", "P4_twelveProjectionState"): 53,
        ("7", "P4_twelveProjectionState"): 17,
        ("0", "P5_twelveProjectionDistribution"): 1,
        ("3", "P5_twelveProjectionDistribution"): 21,
        ("7", "P5_twelveProjectionDistribution"): 6,
    }
    got = {(r["time"], r["package"]): int(r["majorityResidual"]) for r in temporal}
    require(all(got[k] == v for k, v in expected.items()), "Watermelon temporal residuals")
    checks += 1

    # Compression boundary on the 748-lineage H037 carrier.
    pareto = rows("results/watermelon/compression_pareto_frontier.csv")
    h037 = [r for r in pareto if r["carrier"] == "H037" and as_bool(r["decisionEligible"])]
    exact_h037 = [r for r in h037 if as_bool(r["exactRecovery"])]
    require(exact_h037 and min(int(r["quotientCardinality"]) for r in exact_h037) == 748,
            "H037 exact quotients remain injective")
    checks += 1
    q747 = [r for r in h037 if int(r["quotientCardinality"]) == 747]
    require(q747 and min(int(r["majorityResidual"]) for r in q747) == 1,
            "H037 first registered 747-state collision boundary")
    checks += 1

    # Paired terminal realization.
    paired = rows("results/watermelon/paired_replicate_fates.csv")
    require(len(paired) == 1550, "Watermelon paired-lineage carrier")
    checks += 1
    concordant = sum(as_bool(r["concordant"]) for r in paired)
    discordant = sum(as_bool(r["discordant"]) for r in paired)
    require((concordant, discordant) == (837, 713), "Watermelon replicate concordance")
    checks += 1
    fates = {r["replicate1_fate"] for r in paired} | {r["replicate2_fate"] for r in paired}
    require(len(fates) == 190, "Watermelon raw terminal fate count")
    checks += 1

    # Persistence checkpoints.
    support = rows("results/watermelon/critical_support_levels.csv")
    k1 = next(r for r in support if int(r["supportLevel"]) == 1)
    require((int(k1["classCount"]), int(k1["largestClass"]), int(k1["stableLineageCount"])) == (31, 128, 1550),
            "Watermelon k=1 persistence geometry")
    checks += 1
    # The critical-level table records only thresholds where the partition changes.
    # Its identity endpoint is k=111, so the final nonself relation persists through k=110.
    identity_endpoint = max(int(r["supportLevel"]) for r in support)
    endpoint_row = next(r for r in support if int(r["supportLevel"]) == identity_endpoint)
    require(identity_endpoint == 111 and int(endpoint_row["edgeCount"]) == 0,
            "Watermelon identity endpoint")
    checks += 1

    # Independent CellTag LSK state/future geometry.
    lsk = rows("results/celltag/lsk_state_fate_recovery.csv")
    lsk_p5 = next(r for r in lsk if r["package"] == "P5" and r["endpoint"] == "finePooled")
    require((int(lsk_p5["cloneCount"]), int(lsk_p5["partitionSize"]),
             int(lsk_p5["mixedFibers"]), int(lsk_p5["discordantPairCount"])) ==
            (1453, 1065, 168, 2564) and not as_bool(lsk_p5["recovers"]),
            "CellTag LSK rich-RNA nonrecovery geometry")
    checks += 1

    lsk_rna = rows("results/celltag/lsk_rna_recovery.csv")
    lsk_atac = rows("results/celltag/lsk_atac_recovery.csv")
    lsk_joint = rows("results/celltag/lsk_joint_recovery.csv")
    rna5 = next(r for r in lsk_rna if r["package"] == "P5" and r["endpoint"] == "finePooled")
    atac5 = next(r for r in lsk_atac if r["package"] == "A5" and r["endpoint"] == "finePooled")
    joint5 = next(r for r in lsk_joint if r["package"] == "J5" and r["endpoint"] == "finePooled")
    require((int(rna5["partitionSize"]), int(rna5["discordantPairCount"])) == (184, 32),
            "CellTag LSK RNA fine-fate collisions")
    checks += 1
    require((int(atac5["partitionSize"]), int(atac5["discordantPairCount"])) == (195, 11),
            "CellTag LSK ATAC fine-fate collisions")
    checks += 1
    require((int(joint5["cloneCount"]), int(joint5["partitionSize"]),
             int(joint5["discordantPairCount"])) == (201, 201, 0)
            and as_bool(joint5["recovers"]) and as_bool(joint5["stateInjective"]),
            "CellTag LSK joint-state fingerprint endpoint")
    checks += 1

    # CellTag iEP temporal history in two biological replicates.
    iep_snap = rows("results/celltag/iep_snapshot_recovery.csv")
    iep_hist = rows("results/celltag/iep_history_recovery.csv")

    def pick(table, replicate, modality, depth, representation, endpoint="fineDay21Fate"):
        return next(
            r for r in table
            if r["replicate"] == replicate
            and r["modality"] == modality
            and r["packageDepth"] == str(depth)
            and r["representation"] == representation
            and r["endpoint"] == endpoint
        )

    r1_rna_snap5 = pick(iep_snap, "r1", "RNA", 5, "snapshotDay3")
    r2_rna_snap5 = pick(iep_snap, "r2", "RNA", 5, "snapshotDay3")
    r1_rna_hist5 = pick(iep_hist, "r1", "RNA", 5, "orderedHistory")
    r2_rna_hist5 = pick(iep_hist, "r2", "RNA", 5, "orderedHistory")
    require((int(r1_rna_snap5["majorityResidual"]), int(r2_rna_snap5["majorityResidual"]),
             int(r1_rna_hist5["majorityResidual"]), int(r2_rna_hist5["majorityResidual"])) ==
            (18, 10, 5, 0),
            "CellTag iEP RNA snapshot/history residuals")
    checks += 1
    require(int(r2_rna_hist5["cloneCount"]) == 159 and int(r2_rna_hist5["partitionSize"]) == 159
            and as_bool(r2_rna_hist5["recovers"]) and as_bool(r2_rna_hist5["stateInjective"]),
            "CellTag iEP replicate-2 RNA fingerprint exactness")
    checks += 1

    r1_atac_hist5 = pick(iep_hist, "r1", "ATAC", 5, "orderedHistory")
    r2_atac_hist5 = pick(iep_hist, "r2", "ATAC", 5, "orderedHistory")
    require((int(r1_atac_hist5["cloneCount"]), int(r1_atac_hist5["partitionSize"]),
             int(r2_atac_hist5["cloneCount"]), int(r2_atac_hist5["partitionSize"])) ==
            (27, 27, 35, 35)
            and as_bool(r1_atac_hist5["recovers"]) and as_bool(r2_atac_hist5["recovers"])
            and as_bool(r1_atac_hist5["stateInjective"]) and as_bool(r2_atac_hist5["stateInjective"]),
            "CellTag iEP ATAC fingerprint histories")
    checks += 1

    r1_multi_snap5 = pick(iep_snap, "r1", "MULTI", 5, "snapshotDay3")
    r2_multi_snap5 = pick(iep_snap, "r2", "MULTI", 5, "snapshotDay3")
    require((int(r1_multi_snap5["cloneCount"]), int(r1_multi_snap5["partitionSize"]),
             int(r2_multi_snap5["cloneCount"]), int(r2_multi_snap5["partitionSize"])) ==
            (17, 17, 24, 24)
            and as_bool(r1_multi_snap5["recovers"]) and as_bool(r2_multi_snap5["recovers"])
            and as_bool(r1_multi_snap5["stateInjective"]) and as_bool(r2_multi_snap5["stateInjective"]),
            "CellTag iEP strict multimodal snapshot exactness")
    checks += 1

    # Cross-replicate transport authority at deepest ordered history.
    transfer = rows("results/celltag/iep_cross_replicate_state_transfer.csv")
    deep = {
        r["modality"]: (int(r["sharedStateValueCount"]), int(r["fatePreservingSharedStateValueCount"]))
        for r in transfer
        if r["packageDepth"] == "5"
        and r["representation"] == "orderedHistory"
        and r["endpoint"] == "fineDay21Fate"
    }
    require(deep == {"RNA": (2, 0), "ATAC": (0, 0), "MULTI": (0, 0)},
            "CellTag iEP cross-replicate transport authority")
    checks += 1

    # Cross-carrier synthesis.
    decision = json.loads((RESULTS / "cross_carrier" / "decision.json").read_text())
    required = {
        "eligibleSystemCount": 3,
        "eligibleFamilyCount": 54,
        "eligibleSurfaceCount": 958,
        "canonicalEligibleSurfaceCount": 849,
        "exactInjectiveSurfaceCount": 352,
        "exactNoninjectiveSurfaceCount": 18,
        "controlQualifiedExactNoninjectiveSurfaceCount": 0,
    }
    require(all(decision[k] == v for k, v in required.items()), "Cross-carrier synthesis census")
    checks += 1

    fingerprints = rows("results/cross_carrier/fingerprint_surfaces.csv")
    shared_exact = rows("results/cross_carrier/shared_exact_surfaces.csv")
    require(len(fingerprints) == 352 and len(shared_exact) == 18,
            "Exact-surface registries match census")
    checks += 1

    systems = rows("results/cross_carrier/biological_systems.csv")
    require(len(systems) == 3, "Biological system count")
    checks += 1
    qualified = sorted(r["system"] for r in systems if as_bool(r["qualifiedPositiveSurplus"]))
    require(qualified == ["CellTag_iEP_reprogramming", "Watermelon_PC9_osimertinib"],
            "Control-qualified positive surplus systems")
    checks += 1

    families = rows("results/cross_carrier/synthesis_families.csv")
    require(len(families) == 54, "Synthesis family count")
    checks += 1

    print(json.dumps({"passed": True, "checks": checks}, sort_keys=True))


if __name__ == "__main__":
    main()
