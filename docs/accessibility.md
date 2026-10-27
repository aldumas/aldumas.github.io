# Accessibility guidelines

The site's bar is **WCAG 2.2 Level AA**. Every change to `site/**` meets it.
The one way out is Adam's explicit permission for a specific departure. A
departure also needs a reason recorded under [Exceptions](#exceptions).

Why 2.2 AA: it has been the current W3C Recommendation since October 2023.
The laws that cite WCAG (the US ADA Title II rule, the EU's EN 301 549) name
2.1 AA, and 2.2 AA is a superset of that, apart from 4.1.1 Parsing, which 2.2
removed. WCAG 3 is still a Working Draft (March 2026), so it isn't a target.
The numbers in brackets below are WCAG 2.2 success criteria. Their full
wording is at https://www.w3.org/TR/WCAG22/, and how to meet each one is at
https://www.w3.org/WAI/WCAG22/Understanding/.

## Checking a change

The work is done when every rule below that bears on the change has been
applied to every page the change touches, and each check gives its pass
result. A change to `style.css` touches every page.

1. **Contrast.** Compute the ratio for each colour pair the change adds or
   alters, against the background it actually sits on. For text over the
   hero image, use the image's lightest pixel behind the text. Relative
   luminance is `0.2126 R + 0.7152 G + 0.0722 B`, with each sRGB channel `c`
   (0–1) linearised as `c / 12.92` if `c <= 0.04045`, else
   `((c + 0.055) / 1.055) ^ 2.4`. The ratio is
   `(lighter + 0.05) / (darker + 0.05)`. It passes at the thresholds under
   [Colour and contrast](#colour-and-contrast).
2. **Keyboard.** Load each page in Playwright (Chromium is pre-installed in
   cloud sessions). Serve it with `python3 -m http.server -d site 8000`.
   Press Tab through the page. It passes when every link and control is
   reached in reading order, and each one shows a visible focus indicator
   that isn't hidden behind anything.
3. **Reflow.** Set the viewport to 320 × 640 CSS px, the equivalent of a
   1280 px window zoomed to 400%. It passes when
   `document.documentElement.scrollWidth <= innerWidth` and no text is cut
   off or overlapping. Repeat at 200% text size: set the root `font-size`
   to 200% in the page.
4. **Structure.** Read the changed HTML against
   [Structure and semantics](#structure-and-semantics) and
   [Images](#images). It passes when every rule there holds.
5. **Automated scan (optional).** If axe-core can be loaded, run it on each
   page. A scan catches roughly a third of failures, so a clean result never
   replaces steps 1–4.

Report each step's result when presenting the change.

## Structure and semantics

- `<html lang="en">` on every page. Text in another language is wrapped
  with its own `lang` [3.1.1, 3.1.2].
- Each page has a unique `<title>` that names the page first and the site
  second, as the existing pages do [2.4.2].
- Exactly one `<h1>` per page, then headings in order with no skipped
  level. Headings describe the section below them [1.3.1, 2.4.6]. Pick a
  heading's level for the outline, then style it in CSS.
- Landmarks: `<header>`, `<nav>`, `<main>`, `<footer>`. When a page has
  more than one `<nav>`, give each its own `aria-label` (for example
  "Main" and "Footer").
- Provide a "Skip to content" link as the first focusable element, visible
  on focus, that jumps to `<main>` [2.4.1].
- Lists are `<ul>`, `<ol>` or `<dl>`, and tables are only for tabular data,
  with `<th>` headers [1.3.1].
- Use native HTML first: `<a href>` to go somewhere, `<button>` to do
  something. Add ARIA only where HTML has no element for the job. Every
  ARIA attribute must be correct, because wrong ARIA is worse than none
  [4.1.2].
- Navigation keeps the same links, in the same order, on every page
  [3.2.3]. The same function keeps the same name everywhere [3.2.4]. The
  contact link stays in the footer of every page [3.2.6].
- Reading order in the HTML matches the visual order [1.3.2]. Keep the
  visual layout following the source order.

## Images

- An informative `<img>` has `alt` text that says what the image conveys
  in context, not "image of" [1.1.1]. The avatar's alt is the model.
- A decorative image has `alt=""`, or is a CSS background, like the grass
  edge and the hero sky.
- Text goes in HTML, not in images. The pixel-art style is applied with
  CSS and fonts [1.4.5]. The Ko-fi images in `kofi/` aren't part of the
  site.
- Every `<img>` has `width` and `height`, so the layout doesn't jump as it
  loads.
- An inline SVG that carries meaning has `role="img"` and a `<title>`. A
  decorative SVG has `aria-hidden="true"`.

## Colour and contrast

- Body text: at least **4.5:1** against its background. Large text (at
  least 24 px, or 18.66 px bold): at least **3:1** [1.4.3]. The Tiny5
  pixel font is thin for its size, so hold its text to 4.5:1 whatever its
  size.
- Non-text items people need to perceive: at least **3:1** against what's
  next to them [1.4.11]. That covers focus indicators, control borders,
  and icons that carry meaning.
- Colour is never the only signal [1.4.1]. Links inside running text are
  underlined. The current page in the nav is underlined as well as
  coloured.
- Contrast is measured without the text shadow. The text must pass on its
  own, so the shadow only adds to it.
- The site has one dark theme, set with `color-scheme: dark`. A new colour
  gets a `--name` in `:root`, so it's computed once and reused.

## Text and layout

- Content reflows to a single column at 320 CSS px with no horizontal
  scroll [1.4.10]. Long words and URLs wrap (`overflow-wrap: anywhere`).
- Text can be zoomed to 200% without loss [1.4.4]. Size text in `px` or
  `rem` and let it scale. The viewport `meta` never sets
  `maximum-scale` or `user-scalable=no`.
- Text survives user spacing overrides [1.4.12]: line height 1.5, paragraph
  spacing 2em, letter spacing 0.12em, word spacing 0.16em. Text containers
  size to their content, never with a fixed `height`.
- Running text is set in Inter. Tiny5 is reserved for headings and short
  labels: its pixel shapes slow reading, especially for dyslexic readers.
- Lines stay at 80 characters or fewer (`.wrap` caps them at 780 px).
  Text is left-aligned, not justified, and running text is in sentence
  case [1.4.8, AAA but cheap here].
- Write plainly: short sentences, common words, terms explained on first
  use.

## Links, keyboard and focus

- Link text says where it goes when read out of context, or with its
  sentence [2.4.4]. Write "More about Night Warden" rather than "Click
  here". An email link shows the address.
- A link that opens a new tab or leaves for another site's download says so
  in its text. The default is to open in the same tab, without
  `target="_blank"`.
- Everything works with the keyboard alone, with no traps [2.1.1, 2.1.2].
  `tabindex` is only ever `0` or `-1`.
- Focus is always visible [2.4.7]. Focusable elements get a
  `:focus-visible` outline: at least 2 px, at least 3:1 against the background, and never
  `outline: none` without a replacement. A focused element is never fully
  hidden by other content [2.4.11].
- An embedded `<iframe>` has a `title` naming what it holds [4.1.2]. Inside
  it, focus styles belong to the provider: keyboard focus moves into the
  embedded page (the Ko-fi form), where the site's CSS can't reach.
- Targets are at least 24 × 24 CSS px, or spaced so a 24 px circle on each
  doesn't overlap another [2.5.8]. Links inside a sentence are exempt.
- Hover and focus behave the same. Anything shown on hover is also shown
  on focus, can be dismissed with Escape, and stays while the pointer is
  over it [1.4.13].

## Motion and media

- Animation and smooth scrolling are wrapped in
  `@media (prefers-reduced-motion: no-preference)`, so the default is
  still.
- Nothing flashes more than three times a second [2.3.1].
- Nothing moves, blinks or plays for more than 5 seconds unless it has a
  pause control [2.2.2]. Audio never plays on its own [1.4.2].
- Video has captions, and an audio description or a transcript. Audio has
  a transcript [1.2.1–1.2.5]. A trailer embedded from YouTube gets its
  captions checked, and a text summary next to it.

## Forms

The site has no forms now: contact is by email and tips go through Ko-fi.
If a form is added:

- Every field has a visible `<label>` tied to it, and the label's text is
  in the field's accessible name [1.3.1, 2.5.3, 3.3.2].
- Fields for personal data have `autocomplete` (`name`, `email`) [1.3.5].
- Errors name the field and say how to fix it, in text [3.3.1, 3.3.3]. They
  are announced through `aria-live` or by moving focus to them.
- No information is asked for twice in one process [3.3.7]. No CAPTCHA or
  memory test is the only way through [3.3.8].

## Exceptions

A departure from a rule above is allowed only with Adam's explicit
permission for that departure. Each permission covers that one departure.
Record it here, and in the commit message that introduces it.

| Date | Page or file | Rule departed from | Reason | Permitted by |
| --- | --- | --- | --- | --- |
| | | | | |
