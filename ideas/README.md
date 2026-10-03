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

## Pull quotes

To repeat a line in large type as an attention grabber, wrap it in the
draft:

```markdown
That was when I noticed <span class="pull">the sentence never had anyone
else in it</span>, and I started listening for it.
```

The line stays in the paragraph as normal text, and a large copy appears
just before that paragraph. One or two per post at most, or they stop
standing out.

## From idea to post

1. Pick an idea from `parent-articles.md` and check its gate column.
2. Open the cited microsaas source. Most arguments already exist there and
   the work is voice and cuts, not new thinking.
3. Draft in `drafts/<slug>.md`. Check it against `../rules-ledger.md`,
   especially §2 (the register).
4. When it's ready, move it to `../src/_posts/YYYY-MM-DD-<slug>.md`, remove
   the `status:` line, and mark the idea as published in the list.
