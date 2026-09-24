# LinkedIn AEO Optimizer

A portable Agent Skill for drafting and revising LinkedIn posts for human readability, credible personal positioning, and experimental answer-engine/generative-engine discoverability (AEO/GEO).

The skill treats URL and hashtag effects as testable hypotheses. It does not claim that LinkedIn exposes a stable URL-generation formula or that semantically descriptive URLs improve AI retrieval.

## What it does

- Chooses the positioning territory that best fits each post instead of forcing one primary theme everywhere.
- Makes the opening semantically clear to people and machines.
- Uses concrete concepts and selective hashtags without keyword stuffing.
- Predicts possible LinkedIn URL concepts for later comparison with the generated URL.
- Records publication and retrieval observations in a private experiment log.
- Gives readability and credibility priority over every optimization tactic.

## Repository layout

```text
.agents/skills/linkedin-aeo-optimizer/
  SKILL.md
  references/
  assets/
  scripts/
private/                 Local positioning and experiment data; ignored by Git
posts/drafts/            Working post drafts
posts/published/         Local copies of published posts
```

## Use

1. Keep your personal positioning in `private/positioning-profile.md`. Start from the public example if you are setting up a new copy of the repository.
2. Ask an Agent Skills-compatible assistant to use `linkedin-aeo-optimizer` on a topic or draft.
3. Review the selected target association, final post, hashtags, and predicted URL concepts.
4. After publishing, add the actual URL and any controlled retrieval observations to `private/experiments.md`.

The `private/` directory is intentionally not part of the distributable skill and will not be present in a fresh clone.

## Validate

The validator uses only the Python standard library and resolves repository paths independently of the current working directory. From the repository root, run:

```bash
python .agents/skills/linkedin-aeo-optimizer/scripts/validate_skill.py
```

It checks the public scaffold, skill frontmatter, local links from `SKILL.md`, and Git privacy protections. GitHub Actions runs the same command when relevant files change.
