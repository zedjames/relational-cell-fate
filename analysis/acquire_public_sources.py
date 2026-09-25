#!/usr/bin/env python3
"""Acquire public source authorities used by the manuscript.

Raw third-party data remain in their original repositories. This helper
retrieves GEO metadata by default and optionally the corresponding raw
supplementary archives. It also freezes the public CellTag-multi source-code
commit used by the paper.

This script performs source acquisition only; it does not expose or recreate
the private research environment.
"""

from __future__ import annotations

import argparse
import hashlib
import shutil
import subprocess
import urllib.request
from pathlib import Path

GEO_ACCESSIONS = {
    "resistrace": "GSE223003",
    "rewind": "GSE161299",
    "watermelon": "GSE150949",
    "celltag_lsk_rna": "GSE216606",
    "celltag_lsk_atac": "GSE216506",
    "celltag_iep_rna": "GSE216518",
    "celltag_iep_atac": "GSE217119",
}

CELLTAG_CODE_REPO = "https://github.com/morris-lab/CellTag-multi-2023"
CELLTAG_CODE_COMMIT = "5fd3778bd3b056239b04a583ebf5911242c5f4ed"

# Hashes frozen in the original public-source audit for the LSK authorities.
KNOWN_SHA256 = {
    "GSE216606_RAW.tar": "bea4668feb3df6f3b06e4bf34defa91ae1e6e83390ae59c7b9753a9947df0d61",
    "GSE216506_RAW.tar": "e79e9b8b5da32e8348b7c1f6601cd7e9d08bb779f113a3cf485a706f5a6488d2",
    "GSE216606_family.soft.gz": "11e7054fbf45674659d3d2e90c8596ff16f4328f48de5ea29d0aab32aaa9715b",
    "GSE216506_family.soft.gz": "0794a80809103832183386b7954a3704cc0988a04772aee3fce0d455205b4c9a",
}


def geo_series_prefix(accession: str) -> str:
    # GSE223003 -> GSE223nnn
    digits = accession[3:]
    return f"GSE{digits[:-3]}nnn"


def geo_base(accession: str) -> str:
    return f"https://ftp.ncbi.nlm.nih.gov/geo/series/{geo_series_prefix(accession)}/{accession}"


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            h.update(block)
    return h.hexdigest()


def fetch(url: str, target: Path) -> None:
    target.parent.mkdir(parents=True, exist_ok=True)
    if target.exists():
        return
    partial = target.with_suffix(target.suffix + ".partial")
    with urllib.request.urlopen(url) as source, partial.open("wb") as sink:
        shutil.copyfileobj(source, sink)
    partial.replace(target)


def verify_if_known(path: Path) -> None:
    expected = KNOWN_SHA256.get(path.name)
    if expected is None:
        return
    got = sha256(path)
    if got != expected:
        raise RuntimeError(f"SHA-256 mismatch for {path.name}: {got} != {expected}")


def acquire_geo(accession: str, root: Path, raw: bool) -> None:
    target = root / accession
    base = geo_base(accession)

    family = target / f"{accession}_family.soft.gz"
    fetch(f"{base}/soft/{accession}_family.soft.gz", family)
    verify_if_known(family)

    filelist = target / "filelist.txt"
    try:
        fetch(f"{base}/suppl/filelist.txt", filelist)
    except Exception:
        # Some GEO records do not expose a separate filelist endpoint.
        pass

    if raw:
        archive = target / f"{accession}_RAW.tar"
        fetch(f"{base}/suppl/{accession}_RAW.tar", archive)
        verify_if_known(archive)

    for path in sorted(target.glob("*")):
        if path.is_file():
            print(f"{accession}\t{path.name}\t{sha256(path)}")


def acquire_celltag_code(root: Path) -> None:
    target = root / "CellTag-multi-2023"
    if not (target / ".git").is_dir():
        subprocess.run(["git", "clone", CELLTAG_CODE_REPO, str(target)], check=True)
    subprocess.run(["git", "-C", str(target), "fetch", "origin", CELLTAG_CODE_COMMIT], check=True)
    subprocess.run(["git", "-C", str(target), "checkout", "--detach", CELLTAG_CODE_COMMIT], check=True)
    print(f"celltag_code\t{CELLTAG_CODE_REPO}\t{CELLTAG_CODE_COMMIT}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dest", type=Path, default=Path("downloads"))
    parser.add_argument("--raw", action="store_true",
                        help="also download GEO *_RAW.tar archives (large)")
    parser.add_argument("--sources", nargs="*", choices=sorted(GEO_ACCESSIONS),
                        default=sorted(GEO_ACCESSIONS))
    parser.add_argument("--skip-celltag-code", action="store_true")
    args = parser.parse_args()

    args.dest.mkdir(parents=True, exist_ok=True)
    for key in args.sources:
        acquire_geo(GEO_ACCESSIONS[key], args.dest, args.raw)

    if not args.skip_celltag_code:
        acquire_celltag_code(args.dest)


if __name__ == "__main__":
    main()
