# Assumption ledger

Parsed by `scripts/rank_assumptions.py`. Keep the column order.

Exact vocabulary — the script errors on anything else rather than guessing,
because a synonym would silently exempt an assumption from the verdict rule:

- `load_bearing`: `yes` | `no`
- `status`: `untested` | `testing` | `passed` | `failed` | `accepted`
- `importance`, `uncertainty`: 1-5
- `test`: a specific action. `TBD`, `none`, and blanks count as no test.

`load_bearing` is `yes` only when the decision genuinely flips if the assumption
is false. Marking everything load-bearing destroys the signal.

Priority = importance x uncertainty. A load-bearing assumption at priority >= 16
with status `untested` forces the verdict to `test`.

| id | assumption | load_bearing | importance | uncertainty | test | cost | status |
|----|-----------|--------------|------------|-------------|------|------|--------|
| A1 |  | yes | 5 | 4 |  |  | untested |
