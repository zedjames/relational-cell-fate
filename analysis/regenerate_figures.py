#!/usr/bin/env python3
"""Regenerate the paper-facing empirical figures from released result artifacts.

This is intentionally a manuscript reproduction script, not a reusable
implementation of the broader relational calculus.
"""

from __future__ import annotations

import csv
import json
import math
from collections import Counter
from pathlib import Path

import matplotlib.pyplot as plt
import networkx as nx
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
RESULTS = ROOT / "results"
OUT = ROOT / "manuscript" / "figures"
OUT.mkdir(parents=True, exist_ok=True)


def read_csv(path: str):
    with (ROOT / path).open(newline="") as handle:
        return list(csv.DictReader(handle))


def save(fig, name: str):
    fig.tight_layout()
    fig.savefig(OUT / name, bbox_inches="tight")
    plt.close(fig)


def fig2_resistrace():
    rows = [
        r for r in read_csv("results/resistrace/recovery_matrix.csv")
        if r["package"] == "P5b_correctedBiologicalState" and r["decision_eligible"] == "True"
    ]
    conditions = ["carboplatin", "control", "NK_challenge", "olaparib"]
    labels = ["Carboplatin", "Control", "NK challenge", "Olaparib"]
    matrix = np.zeros((4, 2))
    mixed = np.zeros((4, 2), dtype=int)
    fibers = np.zeros((4, 2), dtype=int)
    for row in rows:
        i = conditions.index(row["condition"])
        j = int(row["replicate"]) - 1
        matrix[i, j] = int(row["majority_residual"]) / int(row["unresolved_cell_count"])
        mixed[i, j] = int(row["fate_mixed_fiber_count"])
        fibers[i, j] = int(row["fiber_count"])

    fig, ax = plt.subplots(figsize=(5.7, 4.3))
    im = ax.imshow(matrix, aspect="auto", cmap="viridis")
    ax.set_xticks([0, 1], labels=["Replicate 1", "Replicate 2"])
    ax.set_yticks(np.arange(4), labels=labels)
    cmap, norm = im.get_cmap(), im.norm
    for i in range(4):
        for j in range(2):
            r, g, b, _ = cmap(norm(matrix[i, j]))
            luminance = 0.2126*r + 0.7152*g + 0.0722*b
            ax.text(
                j, i,
                f"{100*matrix[i,j]:.1f}%\n{mixed[i,j]}/{fibers[i,j]} mixed",
                ha="center", va="center", fontsize=8,
                color="black" if luminance > 0.62 else "white",
                fontweight="medium",
            )
    ax.set_title("ReSisTrace: residual future ambiguity across eight strata")
    cbar = fig.colorbar(im, ax=ax)
    cbar.set_label("Majority residual / pre-treatment carrier")
    save(fig, "fig2_resistrace_heatmap_corrected.pdf")


def fig2_rewind():
    perm = read_csv("results/rewind/fate_permutation.csv")
    labels = [r["package"].replace("P1_", "").replace("P2_", "").replace("P3_", "").replace("P5_", "") for r in perm]
    obs = np.array([float(r["observed_majority_residual"]) for r in perm])
    nmin = np.array([float(r["null_min"]) for r in perm])
    nmean = np.array([float(r["null_mean"]) for r in perm])
    nmax = np.array([float(r["null_max"]) for r in perm])
    y = np.arange(len(labels))
    fig, ax = plt.subplots(figsize=(7.3, 5.2))
    ax.errorbar(nmean, y, xerr=np.vstack([nmean-nmin, nmax-nmean]), fmt="o", capsize=3, label="Permutation null range")
    ax.scatter(obs, y, marker="x", s=55, label="Observed residual")
    ax.set_yticks(y, labels=labels)
    ax.invert_yaxis()
    ax.set_xlabel("Majority residual")
    ax.set_title("Rewind precursor-state residuals vs fate permutations")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(axis="x", alpha=0.2)
    save(fig, "fig2a_rewind_residuals.pdf")

    rec = read_csv("results/rewind/recovery_matrix.csv")
    wanted = [
        ("P0_primedConstant", "Constant"),
        ("P2_nineGeneFateBlindVector", "9-gene"),
        ("P3_fateBlindBurden", "Burden"),
        ("P5_richPrecursorQuotient", "Rich"),
    ]
    selected = [next(r for r in rec if r["package"] == package) for package, _ in wanted]
    pure = np.array([int(r["pure_fiber_count"]) for r in selected])
    mixed = np.array([int(r["mixed_fiber_count"]) for r in selected])
    names = [label for _, label in wanted]
    x = np.arange(len(names))
    fig, ax = plt.subplots(figsize=(6.5, 4.3))
    ax.bar(x, pure, label="Fate-pure fibers")
    ax.bar(x, mixed, bottom=pure, label="Mixed fibers")
    ax.set_xticks(x, labels=names)
    ax.set_ylabel("Number of state fibers")
    ax.set_title("Rewind finite fiber geometry")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(axis="y", alpha=0.2)
    save(fig, "fig2b_rewind_fibers.pdf")


def fig3_temporal_history():
    rows = read_csv("results/watermelon/temporal_residuals.csv")
    times = [0, 3, 7]
    fig, ax = plt.subplots(figsize=(6.2, 4.2))
    for package, label in [
        ("P4_twelveProjectionState", "P4: 12-projection state"),
        ("P5_twelveProjectionDistribution", "P5: distributional state"),
    ]:
        vals = []
        for t in times:
            row = next(r for r in rows if int(r["time"]) == t and r["package"] == package)
            vals.append(int(row["majorityResidual"]))
        ax.plot(times, vals, marker="o", label=label)
    ax.set_xticks(times)
    ax.set_xlabel("Treatment day")
    ax.set_ylabel("Majority residual")
    ax.set_title("Instantaneous terminal-fate ambiguity")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.2)
    save(fig, "fig3a_temporal_residuals.pdf")

    hist = read_csv("results/watermelon/history_summary.csv")
    names = [r["carrier"].replace("H03", "H0,3").replace("H037", "H0,3,7") for r in hist]
    lineages = np.array([int(r["lineages"]) for r in hist])
    states = np.array([int(r["distinct_history_states"]) for r in hist])
    x = np.arange(len(hist))
    w = 0.34
    fig, ax = plt.subplots(figsize=(5.8, 4.2))
    ax.bar(x-w/2, lineages, width=w, label="Lineages")
    ax.bar(x+w/2, states, width=w, label="Distinct history states")
    ax.set_xticks(x, labels=names)
    ax.set_ylabel("Count")
    ax.set_title("Exact history recovery coincides with identity resolution")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(axis="y", alpha=0.2)
    save(fig, "fig3b_history_identity.pdf")

    exact = [100*int(r["random_exact_count"])/int(r["random_bank_count"]) for r in hist]
    labels = ["Through day 3", "Through day 7"]
    fig, ax = plt.subplots(figsize=(5.8, 4.2))
    bars = ax.bar(labels, exact)
    ax.set_ylabel("Matched random banks with exact recovery (%)")
    ax.set_ylim(0, 100)
    ax.set_title("Exact finite recovery in matched random histories")
    for bar, row, value in zip(bars, hist, exact):
        ax.text(bar.get_x()+bar.get_width()/2, value+2,
                f"{row['random_exact_count']}/{row['random_bank_count']}",
                ha="center", va="bottom", fontsize=9)
    ax.grid(axis="y", alpha=0.2)
    save(fig, "fig3c_random_history.pdf")


def fig4_compression():
    rows = [r for r in read_csv("results/watermelon/compression_pareto_frontier.csv") if r["carrier"] == "H037"]
    # For each quotient cardinality keep the lowest registered residual.
    best = {}
    for r in rows:
        q = int(r["quotientCardinality"])
        residual = int(r["majorityResidual"])
        best[q] = min(best.get(q, residual), residual)
    xs = np.array(sorted(best))
    ys = np.array([best[x] for x in xs])
    fig, ax = plt.subplots(figsize=(7.0, 4.8))
    ax.plot(xs, ys, marker="o", markersize=3)
    ax.scatter([747], [1], s=60, marker="x", label="First registered nontrivial collision")
    ax.scatter([748], [0], s=45, label="Exact injective endpoint")
    ax.axvline(163, linestyle="--", linewidth=1, label="Oracle lower bound (163 fates)")
    ax.set_xlabel("History quotient cardinality")
    ax.set_ylabel("Majority residual")
    ax.set_title("Compression–ambiguity frontier on 748 complete trajectories")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.2)
    save(fig, "fig4_compression_frontier.pdf")


def fig5_repeated_realization():
    rows = read_csv("results/watermelon/paired_replicate_fates.csv")
    edge_counts = Counter()
    for r in rows:
        a, b = r["replicate1_fate"], r["replicate2_fate"]
        if a == b:
            continue
        edge_counts[tuple(sorted((a, b)))] += 1
    top = edge_counts.most_common(20)
    G = nx.Graph()
    for (a, b), w in top:
        G.add_edge(a, b, weight=w)
    pos = nx.spring_layout(G, seed=7, weight="weight")
    weights = np.array([G[u][v]["weight"] for u, v in G.edges()])
    widths = 0.6 + 3.4*(weights-weights.min())/(weights.max()-weights.min()) if len(set(weights)) > 1 else np.ones_like(weights)
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    nx.draw_networkx_nodes(G, pos, node_size=520, ax=ax)
    nx.draw_networkx_edges(G, pos, width=widths, alpha=0.65, ax=ax)
    nx.draw_networkx_labels(G, pos, font_size=7, ax=ax)
    edge_labels = {(u, v): G[u][v]["weight"] for u, v in G.edges() if G[u][v]["weight"] >= 11}
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=6, rotate=False, ax=ax)
    ax.set_title("Highest-support terminal fate-pair relations")
    ax.axis("off")
    save(fig, "fig5e_top_fate_graph.pdf")

    mins = np.array([1, 2, 3, 5])
    carrier_sizes, raw_supports = [], []
    for minimum in mins:
        eligible = [r for r in rows if min(int(r["replicate1_total"]), int(r["replicate2_total"])) >= minimum]
        ec = Counter()
        for r in eligible:
            a, b = r["replicate1_fate"], r["replicate2_fate"]
            if a != b:
                ec[tuple(sorted((a, b)))] += 1
        carrier_sizes.append(len(eligible))
        raw_supports.append(max(ec.values()) if ec else 0)
    carrier_sizes = np.array(carrier_sizes)
    raw_supports = np.array(raw_supports)
    normalized = raw_supports/carrier_sizes

    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    ax.plot(mins, raw_supports, marker="o")
    for x, y, n in zip(mins, raw_supports, carrier_sizes):
        ax.text(x, y+3, f"N={n}", ha="center", fontsize=8)
    ax.set_xlabel("Minimum terminal cells per replicate")
    ax.set_ylabel("Maximum nonself support (lineages)")
    ax.set_title("Raw support depth under count-qualified carriers")
    ax.set_xticks(mins)
    ax.grid(alpha=0.2)
    save(fig, "fig5_raw_support_sensitivity.pdf")

    fig, ax = plt.subplots(figsize=(5.8, 4.0))
    ax.plot(mins, 100*normalized, marker="o")
    ax.set_xlabel("Minimum terminal cells per replicate")
    ax.set_ylabel("Maximum support / eligible paired lineages (%)")
    ax.set_title("Carrier-normalized support depth")
    ax.set_xticks(mins)
    ax.grid(alpha=0.2)
    save(fig, "fig5_normalized_support_sensitivity.pdf")


def fig6_persistence_and_robustness():
    support = read_csv("results/watermelon/critical_support_levels.csv")
    k = np.array([int(r["supportLevel"]) for r in support])
    class_count = np.array([int(r["classCount"]) for r in support])
    largest = np.array([int(r["largestClass"]) for r in support])
    stable = np.array([float(r["stableLineageFraction"]) for r in support])

    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    ax.plot(k, class_count, marker="o", label="Fate classes")
    ax.plot(k, largest, marker="o", label="Largest component")
    ax.set_xscale("log")
    ax.set_xlabel("Minimum direct lineage support, k")
    ax.set_ylabel("Count")
    ax.set_title("Support-indexed terminal fate filtration")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.2)
    save(fig, "fig5a_persistence_filtration.pdf")

    fig, ax = plt.subplots(figsize=(6.5, 4.2))
    ax.plot(k, stable, marker="o")
    ax.set_xscale("log")
    ax.set_ylim(0.5, 1.02)
    ax.set_xlabel("Minimum direct lineage support, k")
    ax.set_ylabel("Paired lineages remaining equivalent")
    ax.set_title("Lineage-level persistence across fate resolution")
    ax.grid(alpha=0.2)
    save(fig, "fig5b_stable_fraction.pdf")

    robust = read_csv("results/watermelon/robustness_summary.csv")
    metric_order = ["class_resolution_area", "pair_discrimination_area", "lineage_persistence_area"]
    labels = ["Class resolution", "Pair discrimination", "Lineage persistence"]

    def panel(analysis, filename, title):
        selected = {r["metric"]: r for r in robust if r["analysis"] == analysis}
        obs = np.array([float(selected[m]["observed"]) for m in metric_order])
        med = np.array([float(selected[m]["null_median"]) for m in metric_order])
        lo = np.array([float(selected[m]["null_2_5pct"]) for m in metric_order])
        hi = np.array([float(selected[m]["null_97_5pct"]) for m in metric_order])
        y = np.arange(3)
        fig, ax = plt.subplots(figsize=(6.7, 4.1))
        ax.errorbar(med, y, xerr=np.vstack([med-lo, hi-med]), fmt="o", capsize=4, label="Null 95% interval")
        ax.scatter(obs, y, marker="x", s=65, label="Observed")
        ax.set_yticks(y, labels=labels)
        ax.invert_yaxis()
        ax.set_xlabel("Whole-profile statistic")
        ax.set_title(title)
        ax.legend(frameon=False, fontsize=8)
        ax.grid(axis="x", alpha=0.2)
        save(fig, filename)

    panel("sampling_depth_conditioned", "fig6_depth_conditioned_null.pdf",
          "Persistence hierarchy after conditioning on lineage sampling depth")
    panel("coarse_four_part_fate", "fig6_alternative_fate_null.pdf",
          "Alternative four-part compositional fate representation")


def fig7_molecular():
    rows = read_csv("results/watermelon/molecular_persistence_profile.csv")
    names = {
        "absoluteTerminalMolecular": "Absolute",
        "classConditionedTerminalMolecular": "Class-conditioned",
        "cycleReducedTerminalMolecular": "Cycle-reduced",
    }
    fig, ax = plt.subplots(figsize=(7.0, 4.5))
    for lane, label in names.items():
        lane_rows = sorted((r for r in rows if r["lane"] == lane), key=lambda r: int(r["supportLevel"]))
        if not lane_rows:
            continue
        ax.plot(
            [int(r["supportLevel"]) for r in lane_rows],
            [float(r["pairWeightedWithin"]) for r in lane_rows],
            marker="o", label=label
        )
    ax.set_xscale("log")
    ax.set_xlabel("Fate support threshold, k")
    ax.set_ylabel("Pair-weighted within-component molecular overlap")
    ax.set_title("Terminal molecular overlap across the persistent fate hierarchy")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.2)
    save(fig, "fig6a_molecular_overlap.pdf")

    kernels = read_csv("results/watermelon/molecular_kernel_summary.csv")
    levels = [38, 62, 110]
    cond = [int(next(r["common_state_count"] for r in kernels if int(r["support_level"]) == k and r["lane"] == "conditioned")) for k in levels]
    cyc = [int(next(r["common_state_count"] for r in kernels if int(r["support_level"]) == k and r["lane"] == "cycle_reduced")) for k in levels]
    x = np.arange(3); w = 0.35
    fig, ax = plt.subplots(figsize=(6.2, 4.3))
    ax.bar(x-w/2, cond, width=w, label="Conditioned kernel")
    ax.bar(x+w/2, cyc, width=w, label="Cycle-reduced kernel")
    ax.set_xticks(x, labels=[f"k={k}" for k in levels])
    ax.set_ylabel("Common molecular states")
    ax.set_title("Root-component molecular kernel under fate refinement")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(axis="y", alpha=0.2)
    save(fig, "fig6c_kernel_sizes.pdf")

    banks = read_csv("results/watermelon/molecular_random_gene_banks.csv")
    observed = {r["lane"]: float(r["profile_area"]) for r in read_csv("results/watermelon/molecular_observed_profile.csv")}
    fig, ax = plt.subplots(figsize=(7.0, 4.4))
    ax.scatter([int(r["bank"]) for r in banks], [float(r["profileArea"]) for r in banks], label="Matched random gene banks")
    ax.axhline(observed["conditioned"], linewidth=1.5, label="Observed conditioned profile")
    ax.axhline(observed["cycle_reduced"], linewidth=1.5, linestyle="--", label="Observed cycle-reduced profile")
    ax.set_xlabel("Matched random gene bank")
    ax.set_ylabel("Whole-profile molecular area")
    ax.set_title("Observed molecular profile within matched random-gene-bank range")
    ax.legend(frameon=False, fontsize=8)
    ax.grid(alpha=0.2)
    save(fig, "fig6b_random_gene_null.pdf")


def fig8_cross_carrier():
    rows = read_csv("results/cross_carrier/phase_plane_data.csv")
    usable = [
        r for r in rows
        if r["decisionEligible"] == "True"
        and not r["duplicateOf"]
        and r["identityResolution"] not in ("", "undefinedInjective")
        and r["futureDiscordanceResolution"] not in ("", "undefinedInjective")
    ]
    system_names = {
        "Watermelon_PC9_osimertinib": ("Watermelon / Rewind", "o"),
        "CellTag_LSK_hematopoiesis": ("CellTag LSK", "s"),
        "CellTag_iEP_reprogramming": ("CellTag iEP", "^"),
    }
    bins = 20
    centers = (np.arange(bins)+0.5)/bins
    fig, ax = plt.subplots(figsize=(7.2, 5.6))
    for system, (label, marker) in system_names.items():
        mat = np.zeros((bins, bins), dtype=int)
        subset = [r for r in usable if r["system"] == system]
        for r in subset:
            I, J = float(r["identityResolution"]), float(r["futureDiscordanceResolution"])
            bx = min(bins-1, max(0, int(I*bins)))
            by = min(bins-1, max(0, int(J*bins)))
            mat[by, bx] += 1
        ys, xs = np.nonzero(mat)
        counts = mat[ys, xs]
        ax.scatter(centers[xs], centers[ys], s=18 + 32*np.sqrt(counts),
                   marker=marker, alpha=0.55, label=label)

    ax.plot([0,1], [0,1], linestyle="--", linewidth=1)
    ax.text(0.06, 0.11, r"$J<I$" + "\nidentity-heavy", fontsize=9)
    ax.text(0.08, 0.22, r"$J>I$" + "\nfate-selective surplus", fontsize=9)
    ax.annotate("identity boundary", xy=(0.985,0.985), xytext=(0.68,0.82),
                arrowprops={"arrowstyle":"->"}, fontsize=9)
    systems = read_csv("results/cross_carrier/biological_systems.csv")
    for r in systems:
        system = r["system"]
        subset = [x for x in usable if x["system"] == system]
        peak = max(subset, key=lambda x: float(x["fateSelectiveSurplus"]))
        ax.scatter([float(peak["identityResolution"])], [float(peak["futureDiscordanceResolution"])], marker="x", s=65)
    ax.set_xlim(-0.02,1.02); ax.set_ylim(-0.02,1.02)
    ax.set_xlabel(r"Identity resolution $I(Q)$")
    ax.set_ylabel(r"Future-discordance resolution $J(Q,F)$")
    ax.set_title("Cross-carrier identity-future geometry")
    ax.legend(frameon=False, fontsize=8, loc="lower right")
    ax.grid(alpha=0.15)
    save(fig, "fig8a_identity_future_phase_plane.pdf")

    decision = json.loads((RESULTS/"cross_carrier"/"decision.json").read_text())
    vals = [
        decision["exactInjectiveSurfaceCount"],
        decision["exactNoninjectiveSurfaceCount"],
        decision["controlQualifiedExactNoninjectiveSurfaceCount"],
    ]
    fig, ax = plt.subplots(figsize=(5.4,4.0))
    bars = ax.bar(["Injective\nexact", "Noninjective\nexact", "Control-qualified\nnoninjective exact"], vals)
    ax.set_ylabel("Canonical exact surfaces")
    ax.set_title("Exact recovery at the identity boundary")
    ax.set_ylim(0, max(vals)*1.08)
    for bar, value in zip(bars, vals):
        ax.text(bar.get_x()+bar.get_width()/2, value+max(vals)*0.02 if value else 5,
                str(value), ha="center", va="bottom", fontsize=10)
    ax.grid(axis="y", alpha=0.15)
    save(fig, "fig8b_exactness_census.pdf")

    order = ["Watermelon_PC9_osimertinib", "CellTag_LSK_hematopoiesis", "CellTag_iEP_reprogramming"]
    labels = ["Watermelon /\nRewind", "CellTag\nLSK", "CellTag\niEP"]
    by_system = {r["system"]: r for r in systems}
    surplus = [float(by_system[s]["bestFateSelectiveSurplus"]) for s in order]
    qualified = [by_system[s]["qualifiedPositiveSurplus"] == "True" for s in order]
    fig, ax = plt.subplots(figsize=(5.6,4.0))
    bars = ax.bar(labels, surplus)
    ax.axhline(0, linewidth=0.8)
    ax.set_ylabel(r"Maximum fate-selective surplus $S=J-I$")
    ax.set_title("Future alignment below exactness")
    for bar, value, q in zip(bars, surplus, qualified):
        ax.text(bar.get_x()+bar.get_width()/2, value+0.0015,
                f"{value:.3f}" + ("*" if q else ""), ha="center", va="bottom", fontsize=9)
    ax.text(0.02,0.95,"* familywise control-qualified",transform=ax.transAxes,ha="left",va="top",fontsize=8)
    ax.grid(axis="y", alpha=0.15)
    save(fig, "fig8c_surplus_by_system.pdf")


def main():
    fig2_resistrace()
    fig2_rewind()
    fig3_temporal_history()
    fig4_compression()
    fig5_repeated_realization()
    fig6_persistence_and_robustness()
    fig7_molecular()
    fig8_cross_carrier()
    generated = sorted(p.name for p in OUT.glob("fig*.pdf"))
    print(json.dumps({"generated": generated, "count": len(generated)}, indent=2))


if __name__ == "__main__":
    main()
