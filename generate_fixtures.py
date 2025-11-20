#!/usr/bin/env python3
"""Generate labeled, sparse synthetic activity fixtures for visualization tests.

This utility writes data files. It does not create commits or claim historical
project work. The seed makes an experimental schedule reproducible.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import random
from pathlib import Path


DAILY_COUNTS = tuple(range(7))
DAILY_WEIGHTS = (50, 20, 13, 8, 5, 3, 1)


def make_schedule(start: dt.date, end: dt.date, seed: int) -> list[dict]:
    if end < start:
        raise ValueError("The end date must be on or after the start date.")
    rng = random.Random(seed)
    schedule = []
    for offset in range((end - start).days + 1):
        day = start + dt.timedelta(days=offset)
        count = rng.choices(DAILY_COUNTS, weights=DAILY_WEIGHTS, k=1)[0]
        schedule.append({"date": day.isoformat(), "commits": count})
    return schedule


def write_fixtures(destination: Path, schedule: list[dict], seed: int) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    metadata = {"synthetic": True, "seed": seed, "timezone": "UTC", "days": schedule}
    (destination / "schedule.json").write_text(json.dumps(metadata, indent=2) + "\n")
    with (destination / "activity.csv").open("w", newline="") as output:
        writer = csv.writer(output)
        writer.writerow(["date", "sample", "synthetic"])
        for day in schedule:
            for sample in range(1, day["commits"] + 1):
                writer.writerow([day["date"], sample, "true"])


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--start", required=True, type=dt.date.fromisoformat)
    parser.add_argument("--end", required=True, type=dt.date.fromisoformat)
    parser.add_argument("--seed", required=True, type=int)
    parser.add_argument("--output", type=Path, default=Path("generated"))
    args = parser.parse_args()
    try:
        schedule = make_schedule(args.start, args.end, args.seed)
    except ValueError as error:
        parser.error(str(error))
    write_fixtures(args.output, schedule, args.seed)
    active = sum(day["commits"] > 0 for day in schedule)
    total = sum(day["commits"] for day in schedule)
    print(f"Synthetic fixtures: {total} samples, {active} active days, {len(schedule) - active} empty days.")


if __name__ == "__main__":
    main()
