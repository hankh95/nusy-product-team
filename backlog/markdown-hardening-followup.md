# Markdown Hardening Follow-up (Mechanical Cleanup)

Goal: Gradually clean legacy Markdown to pass strict lint rules without changing meaning.

## Scope (priority order)

- `santiago-pm/strategic-charts/` (baseline suppressions added; convert gradually)
- `santiago-pm/templates/`
- `santiago-pm/tackle/`
- Other long-form notes under `santiago-pm/`

## Mechanical Fix Checklist

- Tabs → spaces (MD010)
- Ordered list prefixes normalized (MD029)
- Headings surrounded by blank lines (MD022)
- Lists/fences surrounded by blank lines (MD032/MD031)
- Fenced code blocks specify language (MD040)
- Remove trailing spaces and ensure single trailing newline (MD009/MD047)
- Avoid inline HTML or replace with plaintext placeholders (MD033)

## Process

- File-by-file PRs limited to mechanical changes; no content rewrite.
- Run: `npx markdownlint-cli2 "<target>/**/*.md"` before commit.
- Keep suppressions at top; remove them as each file becomes compliant.

## Acceptance

- No new lint errors in touched paths.
- Visual content unchanged aside from whitespace/fence language.
