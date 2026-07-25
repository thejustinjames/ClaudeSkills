# Evidence

One block per item. The `## E<n> | type: ... | source: ... | date: ...` header
format is parsed by `evidence_lint.py`, so keep it exact.

Types: `primary` · `internal-data` · `secondary` · `anecdote` · `expert`.
There is no type for a number a model produced — see
`references/evidence-protocol.md`.

Record the parts that cut against the decision. They are the most informative
lines in the file.

<!-- Delete the examples below once real evidence is in. -->

## E1 | type: primary | source: Interview — <role, company> | date: YYYY-MM-DD
<What was said or observed, including what they declined to commit to.>

## E2 | type: internal-data | source: <system, export date> | date: YYYY-MM-DD
<The figures, as exported. Not remembered.>

## E3 | type: secondary | source: <URL> | date: YYYY-MM
<What it claims, and whether the methodology is disclosed.>
