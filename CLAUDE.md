# Mister Inevitable — Adam's Personal Blog

A personal blog by Adam Dumas about his family's life with their daughter,
who has Phelan-McDermid Syndrome (PMS). It's published at
**https://blog.misterinevitable.com** through GitHub Pages from this repo
(`aldumas/aldumas.github.io`). The history was reset on 2026-10-02 and the
old programming blog was removed.

This is **not** the business. The micro-SaaS Adam is planning lives in
`../microsaas` and has its own rules, gates and (later) its own blog. The
business site may one day host or link to this blog, but the two stay
separate. See `rules-ledger.md` §5.

## Before writing anything for the blog

**Read `rules-ledger.md`.** It is the standing rulebook. §2 (the register,
honor never pity) governs every sentence, and §1 governs anything about
her. The rules that trip most often:

- Her real name never appears anywhere in this repo. Use `[daughter]`
  until the decision in `rules-ledger.md` §7 is made and dated.
- **The repo is public.** `ideas/` and drafts aren't built into the site,
  but they're readable on GitHub. Nothing private goes in any file.
- Never preach to other parents about their own life (`rules-ledger.md`
  §2c). Arguments about worth and inclusion are aimed at friends and
  onlookers.
- Peer experience, never advice (`rules-ledger.md` §4).
- Nothing offers or pitches the product (`rules-ledger.md` §5).
- Any text Claude drafts in Adam's voice starts with a notice that it's
  Claude-generated and not yet his (`rules-ledger.md` §6).

## Where things are

```
src/                 the site Bridgetown builds (the only published folder)
  _posts/            published posts: YYYY-MM-DD-slug.md
  _layouts/          default, page, post (ERB)
  _partials/         head (seo + feed tags), footer
  _components/shared navbar
  _data/site_metadata.yml   title, tagline, description, author
  CNAME              blog.misterinevitable.com (copied to output)
frontend/styles/     index.css (light and dark)
config/initializers.rb   url, timezone, plugins (bridgetown-feed, -seo-tag)
ideas/               NOT published: idea list and drafts (see ideas/README.md)
  parent-articles.md the article idea list, with sources in ../microsaas
  drafts/            posts being written
rules-ledger.md      how this blog is written; check before drafting
.github/workflows/deploy.yml   builds and deploys to Pages on push to main
```

## Commands

Bridgetown 2.2 needs **Node 22+** and Ruby 3.3 (`.tool-versions`). Adam's
shell puts nvm's Node 20 ahead of mise's Node 22, and the build fails with
`fsLib.globSync is not a function`. Put Node 22 first on `PATH` for the
session, e.g.
`export PATH=$(mise where node@22)/bin:$PATH` (and drop `.nvm` entries
if Ruby's subshell still finds Node 20).

```
bin/bridgetown start                              # dev server, http://localhost:4000
BRIDGETOWN_ENV=production bin/bridgetown deploy   # production build into output/
```

Deploying is just pushing `main`. The workflow builds and publishes.

## Working with the microsaas workspace

- `../microsaas` is a **read-only source** from this repo. Cite its docs by
  path (`../microsaas/docs/...`), and never edit it from a blog session.
- Its docs follow a rule this one keeps too: **a section number is never
  given alone, always with its file** (`rules-ledger.md` §2, not "§2").
  Shorthand used in this repo: **blog ledger** = `rules-ledger.md`;
  **microsaas ledger** = `../microsaas/docs/rules-ledger.md`. Both have a §5,
  so the name is required.
- Don't copy gate states (employer disclosure, validation) into this repo.
  They change. Read `../microsaas/docs/opportunity-plan.md` §6 when it
  matters.

## Conventions

- Date significant decisions `YYYY-MM-DD` and keep `_Last updated_` lines
  current in `rules-ledger.md` and `ideas/parent-articles.md`.
- A rule change updates `rules-ledger.md` in the same commit.
- When an idea is published, mark it in `ideas/parent-articles.md`.
- Adam is an experienced Rails developer. Explain Bridgetown specifics
  only when they differ from Rails or Jekyll habits.
