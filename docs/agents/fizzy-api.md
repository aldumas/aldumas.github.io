# Fizzy API reference

Fizzy (fizzy.do, 37signals' kanban tracker) as an agent drives it over its REST API: boards, columns, cards and what hangs off them. Account administration (tokens, users, exports, webhooks, board publishing and settings) is in `fizzy-api-admin.md`, next to this file, with every write agents don't make.

Copied from `aldumas/night-warden` (`docs/agents/fizzy-api.md`, with `fizzy-api-admin.md`) on 2026-10-26 and adapted for this repo's board. Condensed from the official docs in `basecamp/fizzy` (`docs/api/`, commit `49fe788`, 2026-10-19). Where the docs and Fizzy's source disagree, this file follows the source and says so. The reads (identity, boards, columns, card lists, single cards, comments, users, `ETag`) were checked against the live API on 2026-10-20, and the two writes agents make on 2026-10-20 (card #29, issue #58); the rest is from the docs and source. When a call behaves differently from this file, check upstream (`https://github.com/basecamp/fizzy/tree/main/docs/api`, then `app/controllers/`), and update this file.

## This repo's board

Each repo works on one Fizzy board only. This one's is **Workshop**, id `03h4eofs9rn73574unoz6p0ys`: the user's general board, for work that isn't about any one mod that has its own board (this website, work across mods, ideas for mods that have no repo yet). Each mod with a repo has its own board, read only by that repo's agents (Night Warden's is in `aldumas/night-warden`). The token may reach those boards: never read, search or change them from here. Read cards through `GET /boards/03h4eofs9rn73574unoz6p0ys/…` or with `board_ids[]=03h4eofs9rn73574unoz6p0ys`, never across the account, and before either write check that the card's `board.id` is this one; if it isn't, stop and tell the user. If the board is missing or renamed, stop and ask rather than picking another by name.

Today this is a rule only: Fizzy doesn't enforce it until each repo has its own Fizzy user.

## What agents may change

The user writes their ideas on this board; an accepted idea becomes GitHub issues. A card about this website gets an issue in this repo (`aldumas/aldumas.github.io`); a card about another repo, such as a mod that has one, gets its issue there, following that repo's own issue conventions. If a card turns out to be about a mod that has its own board, tell the user rather than filing it, so they can move the card. The token can write, but agents make only these two writes, and only to a card whose idea has just become a GitHub issue (recipe "File a card's idea as an issue"):

1. Add a link to the issue to the card's description (`PUT /cards/:n`).
2. Move the card into the board's **Issue filed** column (`POST /cards/:n/triage`).

Anything else that changes Fizzy (creating, deleting, closing, commenting, tagging, assigning, any change to boards or columns) is for the user, even when a task seems to need it: tell them, and let them do it. If the board has no "Issue filed" column, stop and say so rather than creating one.

## Setup

There's no Fizzy connector, and the user turned down third-party Fizzy MCP servers (they'd see the token), so agents call the REST API with curl.


- **Host**: `https://app.fizzy.do`, which the session's cloud environment must allow (its settings: Network access, Allowed domains). A `CONNECT tunnel failed, response 403` from curl means this session's environment doesn't allow it.
- **Token**: a personal access token in `FIZZY_TOKEN`, set in the cloud environment, never in a file: this repo is public. It is a `Read + Write` token, since Fizzy has no narrower scope; the limit above is a rule, not something Fizzy enforces. A `Read` token's write gets `401`. Keep the token out of files, commits, logs and command echoes.

```bash
fizzy() {  # fizzy METHOD PATH [JSON]   e.g. fizzy GET /my/identity
	curl -sS -X "$1" "https://app.fizzy.do$2" \
		-H "Authorization: Bearer $FIZZY_TOKEN" -H "Accept: application/json" \
		${3:+-H "Content-Type: application/json" -d "$3"} -w '\n%{http_code}\n'
}
```

## First call: find the account slug

Almost every path starts with `/:account_slug`. `GET /my/identity` (no slug) lists the accounts the token can reach:

```json
{ "id": "03gs…", "accounts": [ { "id": "03gs…", "name": "37signals", "slug": "/897362094",
    "created_at": "…", "user": { "id": "03gs…", "name": "…", "role": "owner", … } } ] }
```

`slug` already carries its leading slash: prefix it as is (`/897362094/boards`). `user.id` is *your* user in that account (for `assignee_ids[]`, `creator_ids[]`).

## Model

Account → boards → cards. A card's place on its board is one of:

| Place | How it shows in a card | Get there |
|-------|------------------------|-----------|
| Triage ("Maybe?") | no `column` field, `closed: false` | `DELETE /cards/:n/triage`; new cards start here |
| A workflow column | `column: {id, name, color}` | `POST /cards/:n/triage` with `column_id` |
| Not Now (postponed) | `postponed: true`, no `column` | `POST /cards/:n/not_now`; also automatic after the board's `auto_postpone_period_in_days` of inactivity |
| Done | `closed: true`, no `column` | `POST /cards/:n/closure`; reopen with `DELETE` |

- **Card number vs id**: card paths take the per-account `number` (`/cards/42`), counted across all the account's boards, so one board's numbers have gaps. They also overlap GitHub's issue numbers: write "card #N" for a card. Filters (`card_ids[]`) and everything else take ids.
- **A board can have no columns**: `GET /boards/:id/columns` then returns `[]`, and every open card is in triage or Not Now.
- **Steps** are a card's checklist; **comments** are rich text; **reactions** ("boosts" on cards) are ≤16 characters; **tags** are account-wide; **golden** marks a card as important; **pins** and **watching** are per-user.
- **Status**: API-created cards are always `published`. The docs list a `status` parameter on create and update, but the source ignores it (`cards_controller.rb` permits only `title, description, image, created_at, last_active_at`), so the API can't make or edit drafts.

## Conventions and gotchas

- **Body wrapping**: bodies nest under the resource name (`{"card": {…}}`, `{"step": …}`, `{"comment": …}`); most controllers also accept the same fields unwrapped. The single-field actions send their parameter at top level: triage `{"column_id"}`, move board `{"board_id"}`, taggings `{"tag_title"}`, assignments `{"assignee_id"}`.
- **Creates return `201 Created`** with a `Location` header (`/897362094/cards/42.json`) and, per the source (`render :show, status: :created`), the new object, though the docs show no body.
- **Toggles**: `taggings` and `assignments` flip state, so a retry undoes the first call. Read the card first (`tags`, `assignees`) and call only when it needs to change. Tagging is the only way to tag a card (the `tag_ids` the docs list on create and update is ignored by the source); it creates a missing tag and strips a leading `#`.
- **Validate before sending**: a wrong type (a string in a number field) usually returns `500`, not `422`. A `422` may carry `{"field": ["message"]}`.
- **Pagination**: lists are paginated with a dynamic page size (early pages are smaller). Follow the `Link` header's `rel="next"` URL until it's absent.
- **List parameters** repeat with `[]`: `?tag_ids[]=a&tag_ids[]=b`. A parameter's values are ORed, except `terms[]`, whose terms must all match; different parameters are ANDed.
- **URLs in responses** (`url`, `comments_url`, `cards_url`…) are opaque absolute URLs: follow them as given.
- **Caching**: responses carry `ETag`; send it back as `If-None-Match` and a `304` means unchanged.
- **Errors**: `400` malformed, `401` bad token (or a `Read` token writing), `403` not allowed (a non-admin), `404` missing *or* not visible to you, `422` validation, `429` rate limited (wait for `Retry-After`), `500` see above. Searching (`GET /cards` with `terms[]`) is limited to 300 an hour per user with a token, then `429` with `Retry-After: 60` (source: `search_rate_limiting.rb`).

## Rich text

Card `description` and comment `body` take HTML, sanitized server-side. Responses give `description` / `description_html` (cards) and `body.plain_text` / `body.html` (comments). An empty description is `""`, but its `description_html` is still an `action-text-content` `<div>` with an empty paragraph, so test `description`. Paragraphs in `description` are separated by several blank lines.

An update replaces the whole description. `description_html` comes wrapped in Action Text's layout, `<div class="action-text-content">…</div>` (source: `app/views/layouts/action_text/contents/_content.html.erb`); send back only what is inside it, or each edit nests another `<div>`.

## Shapes

Lists and nested objects reuse these. Fields marked † appear only sometimes.

- **User**: `id, name, role (owner|admin|member|system), active, email_address, created_at, url, avatar_url`. The `system` user, named "System", with a null `email_address`, writes the automatic comments; `GET /users` leaves it out.
- **Board**: `id, name, all_access, created_at, auto_postpone_period_in_days, url, creator (User), public_description†, public_description_html†, public_url†` (the last three only when published, wherever a board appears); `GET /boards/:id` adds `user_ids†` (only when `all_access` is false).
- **Column**: `id, name, color, created_at, cards_url`. `color` is `{name, value}` everywhere, though the docs show a bare string in column lists (source: `Column::Colored#color` returns a `Color` struct, and every view uses the same `columns/_column` partial). Sending a color takes the `value`: `var(--color-card-default)` Blue, then `var(--color-card-N)` for N = 1 Gray, 2 Tan, 3 Yellow, 4 Lime, 5 Aqua, 6 Violet, 7 Purple, 8 Pink.
- **Card**: `id, number, title, status, description, description_html, image_url, has_attachments, tags (titles), closed, postponed, golden, last_active_at, created_at, url, board (Board), column† (only when triaged), creator (User), assignees, has_more_assignees, comments_url, reactions_url`; `GET /cards/:n` adds `steps: [Step]`. `image_url` is null without an image. The docs say list items may omit `closed` and `postponed`; they were present in every list read so far, but read the single card when they matter.
- **Step**: `id, content, completed`
- **Comment**: `id, created_at, updated_at, body {plain_text, html}, creator (User), card {id, url}, reactions_url, url`. A card's comments include Fizzy's own event notes ("<name> changed the title from … to …"), by the `system` user: skip `creator.role == "system"` to get what people wrote.
- **Reaction**: `id, content, reacter (User), url`
- **Tag**: `id, title, created_at, url`
- **Activity**: `id, action, created_at, description (a sentence), particulars, url, eventable_type (Card | Comment), eventable, board, creator`. `particulars` by action: `card_assigned` / `card_unassigned` `{assignee_ids}`, `card_board_changed` `{old_board, new_board}`, `card_title_changed` `{old_title, new_title}`, `card_triaged` `{column}`; `{}` for `card_auto_postponed`, `card_closed`, `card_postponed`, `card_published`, `card_reopened`, `card_sent_back_to_triage`, `comment_created`. Ignore unknown keys and actions. The feed shows current state (a moved card's history moves with it, deleted items vanish), so it isn't an audit log.

## Endpoints

Every path starts with `/:account_slug`. These are the reads plus the two writes agents make; every other write is in `fizzy-api-admin.md`, for reference.

### Cards

| Method & path | Does | Body / notes |
|---------------|------|--------------|
| `GET /cards` | List cards you can see | Query below |
| `GET /cards/:n` | One card, with `steps` | |
| `PUT /cards/:n` | Update; agents send only `description` (see the top of this file) | `card: {title, description, image, last_active_at}` → card |
| `POST /cards/:n/triage` | Into a column; agents use only "Issue filed" | `{"column_id"}` (a column of the card's board) → 204 |
| `GET /my/pins` | Your pinned cards | Not paginated, ≤100 |

`GET /cards` query: `board_ids[]`, `column_ids[]`, `tag_ids[]`, `assignee_ids[]`, `creator_ids[]`, `closer_ids[]`, `card_ids[]`, `terms[]` (search), `indexed_by` = `all` (default) \| `maybe` \| `closed` \| `not_now` \| `stalled` \| `postponing_soon` \| `golden`, `sorted_by` = `latest` (default) \| `newest` \| `oldest`, `assignment_status=unassigned`, `creation` / `closure` = `today` \| `yesterday` \| `thisweek` \| `lastweek` \| `thismonth` \| `lastmonth` \| `thisyear` \| `lastyear`.

### Steps, comments, reactions

| Method & path | Does | Body / notes |
|---------------|------|--------------|
| `GET /cards/:n/steps/:step_id` | One step | All steps come with `GET /cards/:n` |
| `GET /cards/:n/comments` | Comments, oldest first | Paginated; includes system event notes (Shapes) |
| `GET /cards/:n/comments/:id` | One comment | |
| `GET /cards/:n/reactions` | List boosts on a card | |
| `GET /cards/:n/comments/:cid/reactions` | List reactions to a comment | |

### Boards, columns, tags, users, activity

| Method & path | Does | Body / notes |
|---------------|------|--------------|
| `GET /boards` | Boards you can access | |
| `GET /boards/:id` | One board | |
| `GET /boards/:id/columns` | Columns in position order | |
| `GET /boards/:id/columns/:cid` | One column | |
| `GET /boards/:id/columns/:cid/cards` | Open cards triaged into that column | Paginated, Card shape |
| `GET /tags` | All tags, alphabetical | Paginated |
| `GET /users` | Active users (for assignee ids) | Paginated; not the `system` user |
| `GET /users/:id` | One user | |
| `GET /activities` | Activity feed, newest first | Paginated; `creator_ids[]`, `board_ids[]` |
| `GET /notifications` | Your notifications, unread first | |

## Recipes

**Read the board**: with this repo's board id (above), `GET /boards/:id/columns` → `GET /boards/:id/columns/:cid/cards` per column. Triage, Not Now and Done are in no column: `GET /cards?board_ids[]=<this board>&indexed_by=maybe|not_now|closed`.

**File a card's idea as an issue** (the only writes agents make; see the top of this file): find the **Issue filed** column on this repo's board (`GET /boards/:id/columns`, by `name`) → create the GitHub issue(s), each body linking the card's `url` → `GET /cards/:n`, and stop unless its `board.id` is this repo's board → unless `description_html` already links every issue, `PUT /cards/:n` with `{"card": {"description": "<the inside of description_html><p>GitHub: <a href=\"…\">#N</a></p>"}}` → `POST /cards/:n/triage {"column_id"}` → `GET /cards/:n` and check the old description survived, the link is there and `column.name` is "Issue filed". If a response differs from this file, stop, tell the user, and fix this file.

**Search**: `GET /cards?board_ids[]=<this board>&terms[]=login&terms[]=mobile` (this board's cards matching both), narrowed further with `indexed_by`. Always pass `board_ids[]`.
