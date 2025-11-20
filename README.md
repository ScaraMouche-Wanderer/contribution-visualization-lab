# Contribution visualization lab

**Explicitly synthetic activity fixtures and a Python data generator.**

This is a visualization experiment, not a record of project work performed on
the displayed dates. Author dates are generated sample timestamps. Committer
timestamps record when the history was actually constructed.

## Sample distribution

- Range: 2025-11-19 through 2026-10-31, spanning 2025 and 2026.
- Samples per day: 0–6, weighted toward empty days and smaller values.
- Generated commits: 385.
- Active days: 170; empty days: 177.
- Generated at: 2026-10-31T10:17:10+00:00.

The schedule is probabilistic test data. It is not a behavioral model or proof
of work. Actual project histories are maintained separately.

## Reproduce the data

```bash
python3 generate_fixtures.py --start 2025-11-19 --end 2026-10-31 --seed 11770762193834033159 --output generated
```

The Python utility writes JSON and CSV fixtures. It does not create Git commits.
`fixtures/activity.csv` and `schedule.json` are generated data, excluded from
source-language statistics. GitHub identifies the actual generator as Python.
