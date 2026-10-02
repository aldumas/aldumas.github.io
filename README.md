# Mister Inevitable

Source for [blog.misterinevitable.com](https://blog.misterinevitable.com),
Adam Dumas's personal blog about his family's life with Phelan-McDermid
Syndrome. Built with [Bridgetown](https://www.bridgetownrb.com) and deployed
to GitHub Pages by `.github/workflows/deploy.yml` on every push to `main`.

## Local development

Requires Ruby 3.3 and Node 22+ (see `.tool-versions`).

```sh
bundle install
npm install
bin/bridgetown start                              # http://localhost:4000
BRIDGETOWN_ENV=production bin/bridgetown deploy   # build into output/
```

## Layout

- `src/`: the site. Posts go in `src/_posts/YYYY-MM-DD-slug.md`.
- `ideas/`: article ideas and drafts. Not built into the site, but public
  in this repo.
- `rules-ledger.md`: how this blog is written.
- `CLAUDE.md`: orientation for Claude Code sessions.
