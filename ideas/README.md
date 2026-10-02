# Ideas — Not Published

_Status: `LIVING`. Created 2026-10-02._

This folder holds article ideas and drafts. **Nothing here is built into the
site.** Bridgetown only builds `src/`. But **this repository is public on
GitHub**, so everything in this folder can be read by anyone. Follow
`../rules-ledger.md` §6: `[daughter]` placeholders, no private details.

## Layout

- `parent-articles.md`: the idea list, grouped by theme, each with its one
  claim, its source in `../microsaas`, and any gate.
- `drafts/`: a post being written. One file per post, named
  `slug.md`, with the same front matter a post uses (`title:`) plus a
  `status:` line (`idea`, `drafting`, `ready`).

## From idea to post

1. Pick an idea from `parent-articles.md` and check its gate column.
2. Open the cited microsaas source. Most arguments already exist there and
   the work is voice and cuts, not new thinking.
3. Draft in `drafts/<slug>.md`. Check it against `../rules-ledger.md`,
   especially §2 (the register).
4. When it's ready, move it to `../src/_posts/YYYY-MM-DD-<slug>.md`, remove
   the `status:` line, and mark the idea as published in the list.
