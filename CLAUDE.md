# misterinevitable.com

The business website of Adam Dumas (Minecraft mods), published at
**https://misterinevitable.com** through GitHub Pages from this repo
(`aldumas/aldumas.github.io`). It's plain static HTML in `site/` with no
build step; `README.md` has the preview command.

The personal blog that used to live here, with its rulebook
(`rules-ledger.md`), article ideas and own `CLAUDE.md`, is in the private
repo `aldumas/blog-archive`. This repo's history was rewritten on
2026-10-26 to start with the site, so none of it is here any more. Keep
it that way: nothing from the blog comes back into this public repo.

## Rules

- **Never `git push` without Adam's explicit permission, every time.**
  Permission for one push doesn't carry over to the next. Commit locally,
  tell him what's waiting (`git log origin/main..main`), and wait. A push to
  `main` that touches `site/**` or the workflow deploys the site
  (`.github/workflows/deploy.yml`). `.claude/settings.json` makes Claude Code
  ask before any push or manual workflow run.
- **The repo is public.** Nothing private goes in any file.
- Any text Claude drafts in Adam's voice starts with a notice that it's
  Claude-generated and not yet his.

## Fizzy

Adam's ideas for work that isn't about one mod with its own board (this
site, work across mods, mods without a repo yet) are cards on the
**Workshop** Fizzy board. Read `docs/agents/fizzy-api.md` before any Fizzy
call: it names the board, and the only two changes agents may make there.
Write "card #N" for a Fizzy card, since its numbers overlap GitHub's.
