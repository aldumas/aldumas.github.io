# misterinevitable.com

The business website of Adam Dumas (Minecraft mods), published at
https://misterinevitable.com through GitHub Pages.

It's plain static HTML in `site/`, with no build step. Pushing changes under
`site/` to `main` deploys it (`.github/workflows/deploy.yml`).

To preview locally: `python3 -m http.server -d site 8000`, then open
http://localhost:8000.
