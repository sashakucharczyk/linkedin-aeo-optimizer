# Repository guidance

This repository packages a portable Agent Skill for improving LinkedIn posts. Keep the public skill generic; keep user-specific positioning and experiment data local.

## Invariants

- The distributable skill lives in `.agents/skills/linkedin-aeo-optimizer/`.
- Personal names, positioning, unpublished results, and other private context belong in `private/`, which must remain ignored by Git.
- Treat claims about LinkedIn-generated URLs, hashtags, and downstream AI retrieval as hypotheses to test, not platform facts.
- Prefer human readability, factual accuracy, and credibility over keyword, hashtag, or URL optimization.
- Do not add network calls, external packages, databases, APIs, MCP servers, or publishing automation.

## Working conventions

- Keep `SKILL.md` concise and route detailed guidance to `references/`.
- Keep reusable output scaffolds in `assets/`.
- Put draft posts in `posts/drafts/` and copies of published posts in `posts/published/`; do not place sensitive positioning data in either folder.
- Preserve claim qualifiers and never manufacture evidence, credentials, outcomes, or retrieval results.
- Do not publish to LinkedIn or modify an external account without explicit user authorization.

## Validation

Run from any directory:

```bash
python .agents/skills/linkedin-aeo-optimizer/scripts/validate_skill.py
```

Before committing, also confirm that private files are ignored:

```bash
git check-ignore -v private/positioning-profile.md private/experiments.md
```
