# Fizzy API: administration

The account-management side of the Fizzy API (board access and publishing, users, tokens, exports, webhooks, settings), and every write agents don't make. Setup, conventions, shapes and the everyday endpoints are in `fizzy-api.md`; read it first. Most of these need an admin or owner role, and agents send none of the writes here (`fizzy-api.md`, "What agents may change").

Every path starts with `/:account_slug` unless marked "no slug". `204` = no body; `201` = the new object.

## Boards

| Method & path | Does | Body / notes |
|---------------|------|--------------|
| `PUT /boards/:id` | Set who can access a board (board admin) | `user_ids[]` at **top level**, beside `board`: `{"board": {"all_access": false}, "user_ids": ["…", "…"]}`. The complete list, not a merge. The docs nest it inside `board`, where the source (`boards_controller.rb`) ignores it. Returns the board, or 204 if you removed your own access |
| `GET /boards/:id/accesses` | Who has access | Paginated; `{board_id, all_access, users: [User + has_access, involvement (watching \| access_only \| null)]}` |
| `PUT /boards/:id/entropy` | Board auto-postpone period | `board: {auto_postpone_period_in_days}` → board |
| `POST` / `DELETE /boards/:id/publication` | Publish (public read-only link) / unpublish | POST → 201 + board with `public_url`; returns the existing publication if already published |

## Users and you

| Method & path | Does | Body / notes |
|---------------|------|--------------|
| `PUT /users/:id` | Rename / avatar | `user: {name, avatar}` (avatar as multipart) → user |
| `DELETE /users/:id/avatar` | Remove avatar | 204 |
| `DELETE /users/:id` | Deactivate | 403 no permission, 422 the only owner |
| `POST /users/:id/email_addresses` | Start your own email change | `{"email_address"}` → 201; the emailed token confirms with `POST /users/:id/email_addresses/:token/confirmation` (no auth, expires in 30 minutes, 5 an hour) |
| `PATCH /my/timezone` | Your timezone (notification emails) | `{"timezone_name": "America/Phoenix"}` → 204 |
| `GET` / `PUT /notifications/settings` | Notification email bundling | PUT `user_settings: {bundle_email_frequency*}` = `never` \| `every_few_hours` \| `daily` \| `weekly` → 204 |

## Account

| Method & path | Does | Body / notes |
|---------------|------|--------------|
| `GET /account/settings` | The account | `{id, name, cards_count, created_at, auto_postpone_period_in_days}` |
| `PUT /account/entropy` | Default auto-postpone period (admin) | `entropy: {auto_postpone_period_in_days}` → account |
| `GET /account/join_code` | Invite link | `{code, usage_count, usage_limit, url, active}` |
| `PUT` / `DELETE /account/join_code` | Set the limit / regenerate (admin) | PUT `account_join_code: {usage_limit*}` → 204 |

## Access tokens (no slug)

| Method & path | Does | Body / notes |
|---------------|------|--------------|
| `GET /my/access_tokens` | Your tokens, without their secrets | |
| `POST /my/access_tokens` | Create one (with a write token) | `access_token: {description, permission: read \| write}` → 201 `{token, description, permission}`; `token` is shown only this once. Upstream's create example puts the account slug first (`/1234567/my/access_tokens`); try that if the bare path 404s |
| `DELETE /my/access_tokens/:id` | Revoke | 204 |

## Exports

Asynchronous: start one, then poll until `status` is `completed` (from `pending`, `processing`; or `failed`). A completed export has a `download_url` (fetched with the same token) for 24 hours.

| Method & path | Does |
|---------------|------|
| `POST /account/exports`, `GET /account/exports/:id` | Whole account (admin or owner) |
| `POST /users/:id/data_exports`, `GET /users/:id/data_exports/:id` | Your own data |

## Webhooks (account admin)

| Method & path | Does | Body / notes |
|---------------|------|--------------|
| `GET` / `POST /boards/:id/webhooks` | List / create | POST `webhook: {name, url, subscribed_actions[]}` → 201; the response names the URL `payload_url` and includes `signing_secret` |
| `GET` / `PATCH` / `DELETE /boards/:id/webhooks/:wid` | Read / update / delete | PATCH ignores `url`, which can't change |
| `POST /boards/:id/webhooks/:wid/activation` | Reactivate a deactivated one | → 201 |
| `GET /boards/:id/webhooks/:wid/deliveries` | Delivery log | `{id, state, request {headers}, response {code, error}, event}`; `request` and `response` are null until delivered |

`subscribed_actions` are the activity actions (`fizzy-api.md`, Shapes) except `card_title_changed`. Each delivery carries `X-Webhook-Signature`, the hex HMAC-SHA256 of the raw body keyed by `signing_secret`, and `X-Webhook-Timestamp`, the event's time in ISO 8601 (source: `app/models/webhook/delivery.rb`; the docs leave it out).

## Writes agents don't make

The rest of the API's writes. Agents send none of them, nor any write elsewhere in this file: their only two writes are in `fizzy-api.md` ("What agents may change"). These are here so the effects of the user's own changes can be understood. `204` = no body; `201` = the new object.

### Cards

| Method & path | Does | Body / notes |
|---------------|------|--------------|
| `POST /boards/:board_id/cards` | Create, in triage | `card: {title*, description, image, created_at, last_active_at}` → 201 |
| `DELETE /cards/:n` | Delete (creator or board admin) | 204 |
| `DELETE /cards/:n/image` | Remove header image | 204 |
| `POST /cards/:n/not_now` | Postpone | 204 |
| `POST` / `DELETE /cards/:n/closure` | Close (Done) / reopen | 204 |
| `PUT /cards/:n/board` | Move to another board | `{"board_id"}` → card |
| `POST /cards/:n/taggings` | Toggle a tag | `{"tag_title"}` → 204 |
| `POST /cards/:n/assignments` | Toggle an assignee | `{"assignee_id"}` → 204 |
| `POST` / `DELETE /cards/:n/watch` | Watch / unwatch | 204 |
| `POST` / `DELETE /cards/:n/goldness` | Mark / unmark golden | 204 |
| `POST` / `DELETE /cards/:n/pin` | Pin / unpin for you | 204 |

### Steps, comments, reactions

| Method & path | Does | Body / notes |
|---------------|------|--------------|
| `POST /cards/:n/steps` | Add step | `step: {content*, completed}` → 201 |
| `PUT /cards/:n/steps/:step_id` | Edit / tick | `step: {content, completed}` → step |
| `DELETE /cards/:n/steps/:step_id` | Delete | 204 |
| `POST /cards/:n/comments` | Add | `comment: {body*, created_at}` → 201 |
| `PUT /cards/:n/comments/:id` | Edit (own only) | `comment: {body*}` → comment |
| `DELETE /cards/:n/comments/:id` | Delete (own only) | 204 |
| `POST /cards/:n/reactions` | Boost a card | `reaction: {content*}` (≤16 chars) → 201 |
| `DELETE /cards/:n/reactions/:id` | Remove your boost | 204 |
| `POST /cards/:n/comments/:cid/reactions` | React to a comment | `reaction: {content*}` → 201 |
| `DELETE /cards/:n/comments/:cid/reactions/:id` | Remove your reaction | 204 |

### Boards, columns, tags, users, activity

| Method & path | Does | Body / notes |
|---------------|------|--------------|
| `POST /boards` | Create | `board: {name*, all_access (default true), auto_postpone_period_in_days, public_description}` → 201 |
| `PUT /boards/:id` | Update (board admin) | `board: {name, all_access, auto_postpone_period_in_days, public_description}`; access list under Boards above |
| `DELETE /boards/:id` | Delete (board admin) | 204 |
| `POST /boards/:id/columns` | Create | `column: {name*, color}` → 201 |
| `PUT /boards/:id/columns/:cid` | Update | `column: {name, color}` → column |
| `DELETE /boards/:id/columns/:cid` | Delete | 204 |
| `POST` / `DELETE /notifications/:id/reading` | Mark read / unread | 204 |
| `POST /notifications/bulk_reading` | Mark all read | 204 |

- `DELETE /cards/:n/triage` sends a card back to triage → 204.
- File uploads (a card's header image) go as `multipart/form-data`: `curl -F "card[image]=@file.png"` with the usual two headers.
- To attach a file: `POST /:account_slug/rails/active_storage/direct_uploads` with `blob: {filename, byte_size, checksum (Base64 MD5 of the content), content_type}` → `PUT` the bytes to `direct_upload.url` with `direct_upload.headers` (a storage host, which has to be an allowed host as well) → embed `<action-text-attachment sgid="SIGNED_ID"></action-text-attachment>` in the HTML, with `signed_id` from the first response.
