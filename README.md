# misterinevitable.com

The business website of Adam Dumas (Minecraft mods), published at
https://misterinevitable.com through GitHub Pages.

It's plain static HTML in `site/`, with no build step. Pushing changes under
`site/` to `main` deploys it (`.github/workflows/deploy.yml`).

## Previewing a branch

GitHub Pages serves only `main`, so a branch has to be previewed some other
way before it's merged.

**In the browser, without cloning.** Since the repo is public,
[raw.githack.com](https://raw.githack.com) serves any commit's files as a
web page, with working links and styles:

```
https://raw.githack.com/aldumas/aldumas.github.io/<commit>/site/index.html
```

Use the commit's full SHA (`git rev-parse <branch>`, or copy it from the
branch's commit list on GitHub) rather than the branch name: githack can't
tell where a branch name with slashes, such as `claude/...`, ends. Each
link shows that one commit, so take a new SHA after every push. Use it only
to preview; don't link to it from anywhere.

**Locally.** Check out the branch, run
`python3 -m http.server -d site 8000`, then open http://localhost:8000.

## Ko-fi images

`kofi/` holds the Ko-fi page's images, which aren't part of the site:
`profile-800.png` (the profile picture) and `cover-1200x400.png` (the cover,
Ko-fi's 3:1). `tools/kofi-profile.py` and `tools/kofi-cover.py` redraw them
(`python3 tools/kofi-profile.py kofi`; they need Pillow).
