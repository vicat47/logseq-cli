---
name: logseq-cli
description: Prefer the local `logseq` CLI whenever a user mentions a Logseq page, a Logseq graph path, or asks for Logseq operations such as reading pages, updating blocks, creating pages, querying the graph, or working with journals. Use this skill to remind Codex that `logseq` exists, to check `logseq --help` or subcommand help when needed, and to favor pipeline-style one-liners when the downstream `logseq` command explicitly supports consuming the needed field from piped NDJSON before editing files directly.
---

# Logseq CLI First

## Overview

Treat Logseq work as CLI-first, not file-first. When the prompt refers to a Logseq page or asks for Logseq graph operations, check whether the `logseq` CLI can do the job before reading or editing Markdown files manually.

## What Logseq Is

Logseq is a local-first knowledge management tool built around an outline-shaped graph. Its core unit is the block rather than the document: each bullet is an addressable node, pages collect blocks, and references connect pages and blocks into a graph that can be queried.

For AI agents, the useful mental model is:
- Pages are named containers that usually map to Markdown files.
- Blocks are nested bullets with parent-child structure determined by indentation.
- `[[Page Name]]` creates a page reference.
- `((block-uuid))` creates a block reference to a specific block.
- `key:: value` stores page or block properties used for metadata and queries.
- Journal pages are date-based pages stored separately from regular named pages.

## Logseq Markdown Shape

Logseq commonly stores Markdown as an outline instead of a flat prose document.

Guidelines:
- Top-level content is usually written as bullet blocks beginning with `- `.
- Child blocks are nested by indentation under a parent block.
- Page-level properties usually appear near the top of the page as `key:: value`.
- Blocks may also carry their own properties, references, tasks, and normal Markdown content.
- Hierarchical page names may be encoded in filenames even when the displayed page title contains `/`.

## Workflow

1. First check whether the `logseq` command exists by running `logseq --help`.
2. If the command is missing or not found, stop and tell the user explicitly that this skill depends on the separately installed `logseq` CLI and that the skill itself does not bundle the executable.
3. When the CLI is missing, give concrete recovery steps:
   - Windows PowerShell: `py -m pip install --user .` from the `logseq-cli` repo, or `pipx install .` if the user prefers `pipx`.
   - If install succeeds but `logseq` is still not found on Windows, tell the user to add their user Python Scripts directory to `PATH`, for example `%APPDATA%\Python\Python310\Scripts`.
   - macOS / Linux: `python3 -m pip install --user .`, then add `~/.local/bin` to `PATH` if needed.
   - If the repo is already present locally but not installed, tell the user the skill only provides instructions and does not run the repo as an adjacent bundled tool automatically.
4. After `logseq --help` works, inspect the relevant subcommand help such as `logseq page --help`, `logseq block --help`, or `logseq query --help`.
5. Prefer pipeline-style CLI usage when the downstream command explicitly supports piped input for the field it needs.
6. Prefer the CLI for page lookup, block operations, graph queries, and other supported mutations.
7. Fall back to direct file edits only when the CLI cannot perform the task or when the task is explicitly about raw Markdown files.

## Page References

When the user mentions a Logseq page, treat it as a concrete graph object. Resolve the page through Logseq-aware tools first instead of assuming the file path. For hierarchical pages such as `My-Project/My-Sub-Project`, remember that the underlying page file may encode `/` as `%2F`.

## Journal and Search Rules

Follow the graph instructions for journal filenames and date resolution. Search narrowly before reading: target the named page, journal date, or specific property instead of scanning the graph broadly.

## Pipeline Pattern

The `logseq` CLI is designed to compose through pipes, but support is selective rather than universal. Prefer one-liners and narrow pipelines when the downstream command explicitly accepts omitted arguments from piped NDJSON.

Guidelines:
- Start with the narrowest object, usually `logseq page get "Page Name"` or a targeted query.
- Pipe command output into the next `logseq` command only when that command's help text says an omitted argument can be read from piped NDJSON.
- Match the field type carefully. For example, `logseq block get` can read a piped `.uuid`, but it expects a block UUID, not a page UUID.
- Use manual inspection only when the pipeline approach is unclear or the command surface does not support the next step cleanly.

Example starting point:

```powershell
logseq page get "My-Project/My-Sub-Project"
```

Observed behavior on this machine:
- `logseq page get "My-Project/My-Sub-Project" | logseq page get --plain` works.
- `logseq page get "My-Project/My-Sub-Project" --fields name,uuid | logseq page get --fields originalName,uuid --plain` works.
- `logseq page get "My-Project/My-Sub-Project" | logseq page refs` does not work because `page refs` requires an explicit `NAME`.
- Piping a page object into `block get` is not valid unless the piped UUID is actually a block UUID.

If the next operation can consume the piped object correctly, prefer a pipeline instead of copying values by hand.

## Command Pattern

Start with these commands:

```powershell
logseq --help
logseq page --help
logseq block --help
logseq query --help
```

If `logseq --help` fails because the command is missing, say so plainly and include the install and `PATH` steps from the workflow above before attempting any Logseq CLI operations.

Use the least invasive command that answers the question. If the user asks about a page and the CLI can retrieve it, use that route before opening `pages/*.md` directly. When possible, build a short `logseq ... | logseq ...` pipeline first.
