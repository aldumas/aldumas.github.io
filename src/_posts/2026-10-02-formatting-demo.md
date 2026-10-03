---
title: Formatting demo
published: false
---

<%# This post is a reference, not an article. `published: false` keeps it
    out of the real site. See it locally with:
      bin/bridgetown start --unpublished
    then open http://localhost:4000/2026/10/02/formatting-demo/ %>

This post shows every effect a post can use, with the source for each one
next to it. It never publishes (`published: false` in the front matter). To
see it, run `bin/bridgetown start --unpublished`.

* Table of contents (generated from the headings below)
{:toc}

## Pull quotes (this blog's own feature)

Wrap a phrase in `<span class="pull">`. It stays in the paragraph, and a large
copy appears just before the paragraph: floated right on wide screens,
full width on phones.

```html
The thing I keep coming back to is that <span class="pull">a plain day,
told plainly, is the most *honest* thing I can write</span>, and the rest
of the paragraph carries on.
```

The thing I keep coming back to is that <span class="pull">a plain day, told
plainly, is the most *honest* thing I can write</span>, and the rest of the
paragraph carries on as normal prose, so a reader who skips the big copy
loses nothing. Markdown inside the span (like the italics) works in both
places. Use one or two per post at most.

## Emphasis

| Effect | Source | Result |
|---|---|---|
| Italic | `*italic*` | *italic* |
| Bold | `**bold**` | **bold** |
| Both | `***both***` | ***both*** |
| Strikethrough | `~~struck~~` | ~~struck~~ |
| Highlight | `==highlighted==` | ==highlighted== |
| Inline code | `` `code` `` | `code` |
| Keyboard key | `<kbd>Ctrl</kbd>` | <kbd>Ctrl</kbd> |
| Superscript | `x<sup>2</sup>` | x<sup>2</sup> |
| Subscript | `H<sub>2</sub>O` | H<sub>2</sub>O |
| Small print | `<small>small</small>` | <small>small</small> |

## Typography that happens automatically

Straight quotes become curly: "like this" and 'like this'. Three dashes make
an em dash --- like that. Two make an en dash, for ranges like 2019--2026.
Three dots become an ellipsis...

## Links

- Inline: `[Bridgetown](https://www.bridgetownrb.com)` →
  [Bridgetown](https://www.bridgetownrb.com)
- Reference style: `[the docs][bt-docs]`, with `[bt-docs]: https://…` defined
  anywhere in the post → [the docs][bt-docs]
- Bare URL: <https://www.bridgetownrb.com>
- Another post on this blog: `[title](/2026/10/02/some-slug/)`

[bt-docs]: https://www.bridgetownrb.com/docs

## Footnotes

A footnote marker goes in the text like this.[^first] The note itself can be
written anywhere in the post and is collected at the bottom.[^second]

[^first]: Source: `like this.[^first]` and then `[^first]: The note.` on its own line.
[^second]: Footnotes are a good home for dates, sources and caveats ("this is what we did, not advice").

## Block quotes

> A quote from someone else goes in a block quote. Start each line with `>`.
>
> Two paragraphs need a `>` on the blank line between them too.

## Lists

- Bulleted items start with `-`
  - Indent two spaces to nest
- Second item

1. Numbered items start with `1.`
2. The numbers don't have to be right; Markdown renumbers them

- [x] A task list item, done (`- [x]`)
- [ ] A task list item, not done (`- [ ]`)

Definition list
: A term on one line, then `: ` and the definition on the next.

Phelan-McDermid Syndrome
: A rare genetic condition caused by a deletion or change at the end of chromosome 22.

## Abbreviations

PMS, written in the text as usual, gets a hover tooltip once an abbreviation
line is anywhere in the post: `*[PMS]: Phelan-McDermid Syndrome`.

*[PMS]: Phelan-McDermid Syndrome

## Tables

| Left aligned | Centered | Right aligned |
|:---|:---:|---:|
| `:---` | `:---:` | `---:` |
| text | text | 42 |

## Code blocks

Fence with three backticks and name the language for syntax highlighting:

```ruby
def greet(name)
  "Hello, #{name}"
end
```

## Horizontal rule

Three dashes on a line by themselves (`---`) draw a divider:

---

## Collapsible section

<details markdown="1">
<summary>Click to open (source: <code>&lt;details markdown="1"&gt;</code>)</summary>

Anything inside, **Markdown included**, stays hidden until opened. The
`markdown="1"` attribute is what lets Markdown work inside the HTML block.

</details>

## Classes and attributes on any block

Kramdown can attach a class or style to the block above it with `{: … }` on
the next line. This paragraph is centered with `{: style="text-align: center"}`.
{: style="text-align: center"}

This one has a class: `{: .post-date}` reuses the muted style from the date
under a post's title.
{: .post-date}

## Images

Put image files in `src/images/` and reference them with a leading slash:

```markdown
![Describe the picture for someone who can't see it](/images/example.jpg)
*A caption is just an italic line right under the image.*
```

Always write the description in the brackets. Screen readers read it out.

## ERB (Ruby in a post)

Posts are processed as ERB before Markdown, so Ruby works in them. This
blog's title is **<%= site.metadata.title %>**, inserted with
<code>&lt;%= site.metadata.title %&gt;</code>.

A comment that never reaches the page is written
<code>&lt;%# like this %&gt;</code>. There's one at the top of this post's
source.

**Gotcha:** an ERB tag runs even inside backticks or a code block. To *show*
one on the page, as this section does, write the angle bracket as `&lt;`
inside an HTML `<code>` tag, e.g. <code>&lt;code&gt;&amp;lt;%= … %&amp;gt;&lt;/code&gt;</code>.

## Headings and links to them

`##` is a section heading and `###` a subsection. (`#` is the post title, so
don't use it in the body.) Every heading gets an ID automatically, so this
section can be linked as `[link](#headings-and-links-to-them)`:
[back to this heading](#headings-and-links-to-them).

### Subsection

Text under a `###` heading.

## Front matter options

The block between the `---` lines at the top of a post:

```yaml
---
title: The post's title          # required
published: false                 # keep it off the site (this post)
description: One-sentence summary for search results and link previews
image: /images/example.jpg       # preview image when the link is shared
---
```

The date comes from the file name (`YYYY-MM-DD-slug.md`). A post dated in the
future won't appear on the site until that date has passed and the site is
rebuilt.
