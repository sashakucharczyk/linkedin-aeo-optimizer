---
name: linkedin-aeo-optimizer
description: Draft or revise LinkedIn posts for readability, credible personal positioning, and experimental AEO/GEO discoverability. Use when shaping a post's opening, semantic concepts, likely URL terms, or selective hashtags without overstating unproven platform behavior.
---

# LinkedIn AEO Optimizer

Produce a LinkedIn post that is useful and credible to a human reader while making its topic, entities, and intended association easy to interpret. Optimization must never make the post less natural or more certain than its evidence supports.

## Gather context

Use the post idea or draft, the intended audience, and any source material the user supplies. Preserve factual boundaries and meaningful qualifiers.

For positioning context, use the first available source:

1. A profile supplied in the request.
2. A workspace-local `private/positioning-profile.md`, when available.
3. Another profile the user identifies.

If no profile is available, optimize readability and semantic clarity without inventing personal positioning. Ask for missing context only when it would materially change the result. Use the [positioning profile example](references/positioning-profile.example.md) only as a schema; never copy its fictional facts into a user's post.

## Select the positioning target dynamically

For each post:

1. Identify the post's actual subject, useful takeaway, evidence, and likely audience need.
2. Compare that material with the profile's primary and supporting territories.
3. Select one intended target association based on direct topical fit, available evidence, audience usefulness, and natural language fit.
4. Choose only the supporting concepts that genuinely reinforce that target.

The primary territory is not a mandatory choice. Do not insert it when a supporting territory—or no explicit territory—is a better fit. If the requested association is weakly supported, state that in working notes and keep it out of the publishable copy.

## Optimize in priority order

1. **Readability and credibility:** Make the post coherent, concrete, appropriately qualified, and easy to scan. Do not invent facts or imply proof the author does not have.
2. **Opening clarity:** In the opening sentence or short opening paragraph, name the main subject and make the central claim, tension, outcome, or question intelligible without the rest of the post.
3. **Natural positioning:** Reinforce the selected target through a useful point of view, relevant evidence, and consistent concepts—not by repeatedly naming a category.
4. **AEO/GEO clarity:** Use explicit entity-to-concept relationships, define uncommon terms, and include answer-shaped statements where natural. Avoid keyword stuffing and repetitive synonyms.
5. **URL and hashtag hypotheses:** Predict possible URL concepts from salient words in the opening and, when useful, hashtags. Never distort the post to chase a speculative slug.

Use short paragraphs and a logical progression. Prefer concrete nouns and verbs to vague hooks. A question may open the post when it is specific; curiosity alone is not a substitute for meaning.

Use hashtags selectively—often none to three. Include only tags that add accurate categorization or genuine audience value. Do not append broad tags merely to repeat keywords.

## Keep experimental claims calibrated

Treat all of the following as unproven, platform-dependent hypotheses:

- Opening text may influence LinkedIn's generated URL.
- Hashtags may influence LinkedIn's generated URL.
- Generated URL semantics may influence how an AI system retrieves or interprets a post.

Do not promise a particular URL, indexing outcome, ranking, citation, reach result, or model association. LinkedIn and retrieval systems can change independently. For experiment design and interpretation, read the [methodology](references/methodology.md).

## Deliver the result

Unless the user requests a different format, provide:

1. **Targeting notes:** the intended target association, supporting concepts, and any important credibility constraint.
2. **Publishable post:** clean copy with optional hashtags included at the end.
3. **Experiment forecast:** the exact opening, chosen hashtags, and a short list of predicted URL concepts, clearly labeled as hypotheses. When retrieval is being tested, also state the retrieval hypothesis and proposed test query or conditions.

Use the [post template](assets/post-template.md) when a file-based draft or repeatable worksheet is useful. Keep working metadata out of the publishable post.

After publication, record the actual URL and observed retrieval results in the workspace's private experiment log if the user asks. Never fabricate an observation, publish a post, or run an external account action without explicit authorization.
