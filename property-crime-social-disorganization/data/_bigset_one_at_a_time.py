"""Populate one BigSet dataset at a time; merge unique source_url rows."""
from __future__ import annotations

import csv
import subprocess
import time
from pathlib import Path

BIGSET = r"C:\Users\Owner\AppData\Roaming\npm\bigset.cmd"
ROOT = Path(r"c:\Users\Owner\OneDrive\Capstone\data")
JOBS = [
    {
        "id": "jd76egy011hjzj15966cj4p9v58dtmf7",
        "name": "security_prices",
        "csv": ROOT / "control_cost" / "bigset_security_prices.csv",
        "target": 80,
    },
    {
        "id": "jd7ahsc4xbjd3wtrwxre0snm018dtpmx",
        "name": "property_crime_news",
        "csv": ROOT / "feature_selection_corpus" / "bigset_property_crime_news.csv",
        "target": 200,
    },
    {
        "id": "jd72cgyf6qmj29f8mrz3p6b0s98dvx71",
        "name": "cde_gaps",
        "csv": ROOT / "cde_gaps" / "bigset_cde_gaps.csv",
        "target": 200,
    },
]
MAX_ATTEMPTS = 8
IDLE_COOLDOWN_S = 75


def run(args: list[str]) -> str:
    return subprocess.check_output([BIGSET, *args], text=True, stderr=subprocess.STDOUT)


def status(dataset_id: str) -> tuple[str, int]:
    text = run(["status", dataset_id])
    st, rows = "unknown", 0
    for line in text.splitlines():
        if line.startswith("Status:"):
            st = line.split(":", 1)[1].strip()
        if line.startswith("Rows:"):
            rows = int(line.split(":", 1)[1].strip())
    return st, rows


def wait_idle(dataset_id: str) -> tuple[str, int]:
    while True:
        st, rows = status(dataset_id)
        print(f"  {st} rows={rows}", flush=True)
        if st != "building":
            return st, rows
        time.sleep(20)


def read_rows(path: Path) -> tuple[list[str], list[dict]]:
    if not path.exists() or path.stat().st_size == 0:
        return [], []
    with path.open(encoding="utf-8", newline="") as f:
        reader = csv.DictReader(f)
        return list(reader.fieldnames or []), list(reader)


def write_rows(path: Path, fields: list[str], rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def merge(master: Path, batch: Path) -> int:
    fa, ra = read_rows(master)
    fb, rb = read_rows(batch)
    fields = list(dict.fromkeys(fa + fb))
    seen = {r.get("source_url", "") for r in ra}
    out = list(ra)
    added = 0
    for row in rb:
        key = row.get("source_url", "")
        if not key or key in seen:
            continue
        seen.add(key)
        out.append(row)
        added += 1
    if fields:
        write_rows(master, fields, out)
    return added


def fill(job: dict) -> None:
    print(f"=== {job['name']} target={job['target']} ===", flush=True)
    zeros = 0
    for attempt in range(1, MAX_ATTEMPTS + 1):
        _, current = read_rows(job["csv"])
        if len(current) >= job["target"]:
            print(f"reached {len(current)}", flush=True)
            return
        print(f"attempt {attempt}/{MAX_ATTEMPTS} have={len(current)} cooldown={IDLE_COOLDOWN_S}s", flush=True)
        time.sleep(IDLE_COOLDOWN_S)
        st, _ = status(job["id"])
        if st != "building":
            run(["populate", job["id"]])
        wait_idle(job["id"])
        batch = job["csv"].with_name(job["csv"].stem + "._batch.csv")
        run(["export", job["id"], "--csv", str(batch)])
        added = merge(job["csv"], batch)
        batch.unlink(missing_ok=True)
        _, current = read_rows(job["csv"])
        print(f"added {added}; unique={len(current)}", flush=True)
        if added == 0:
            zeros += 1
            if zeros >= 2:
                print("stopped after two empty merges", flush=True)
                return
        else:
            zeros = 0


def main() -> None:
    for job in JOBS:
        fill(job)
    print("done", flush=True)


if __name__ == "__main__":
    main()
