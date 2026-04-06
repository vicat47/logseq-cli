# TODO

Backlog ideas.

This project should stay centered on the Logseq local HTTP API, structured output,
and shell composition. The items below focus on useful gaps without turning the
tool into a file-editor wrapper.

## High Priority

- Add page and journal search commands.
  Add explicit search commands such as `page search <text>` and possibly
  `page search-regex <pattern>` that return NDJSON and support `--fields`
  and `--plain`.

- Add journal date convenience commands.
  This CLI already has `page journal <YYYY-MM-DD>`, but it would be useful to
  support flags like `--today`, `--yesterday`, and `--days-ago N`, or dedicated
  commands like `page journal-today` and `page journal-offset <n>`.

- Add page content/tree retrieval commands for AI workflows.
  AI agents often need the full block tree of a page, not just page metadata.
  Add a command such as `page tree <name>` or `page blocks <name>` with
  `--fields`, `--plain`, and predictable NDJSON output.

- Add alias-aware page discovery.
  If Logseq exposes enough data through the API, add a way to search by aliases
  as well as page names so agents can resolve pages more robustly.

## Medium Priority

- Add raw content extraction helpers.
  An API-native way to print journal or page content directly would be useful
  for scripting and agents, for example `page export-text <name>` that flattens
  a page tree into readable text while keeping stdout pipe-safe.

- Add append/prepend-from-stdin text modes.
  The current CLI supports identifier auto-stdin, but not content-from-stdin for
  note capture. Add commands or flags that accept block content from stdin, such
  as `block append --stdin <page>` or `block insert --stdin --uuid <uuid>`.

- Add bulk page operations.
  Search becomes much more useful if it can feed into safe bulk actions like
  rename, delete, property updates, or export. Keep these explicit and pipe-safe.

- Add block search.
  Searching only pages is limiting for agents. A `block search <text>` command
  could support finding actionable blocks, tasks, or references directly.

- Add task-oriented commands if the HTTP API supports them cleanly.
  Useful examples would be listing TODO/DOING blocks, scheduled items, or blocks
  with deadlines. This fits the graph/API model better than file scanning.

## Low Priority

- Add fuzzy selection helpers only if they remain non-interactive by default.
  This project should avoid making TUI interaction central, but optional fuzzy
  filtering output could still help.

- Add a safer "capture" command as a higher-level wrapper.
  A command like `capture journal <content>` or `capture page <name> <content>`
  could simplify common note-entry flows while still mapping to the existing
  service-layer operations.

- Add richer date parsing for journal operations.
  Support inputs like `today`, `yesterday`, and ISO dates in one place, while
  still printing resolved absolute dates in output and errors.

## Explicit Non-Goals Unless There Is A Strong Reason

- Opening an external editor as the primary workflow.
- Direct filesystem mutation of Logseq Markdown/Org files.
- Supporting Org mode via file parsing instead of the HTTP API.
- Replacing structured graph commands with a shortcut-heavy TUI-style interface.
