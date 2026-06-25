---
name: grok-imagine-generate
description: Use when the user asks Codex to generate Grok Imagine images, create AI image prompts from text or an uploaded image, produce prompt variants, iterate on a previous prompt version, enter prompts into Grok, press the Grok Imagine submit/up-arrow button, queue multiple generations, reuse an open Grok Imagine tab, or operate Grok through Chrome with the user's logged-in session. For character prompts, always include a concise body type description. For revisions, generate standalone prompt text that restates all retained subject, scene, style, body type, and composition details instead of referring to the previous image/version.
---

# Grok Imagine Generate

## Overview

Submit image prompts to Grok Imagine through the user's Chrome browser. Prefer this skill when the user wants Grok itself to generate the image, especially when they mention Grok, Grok Imagine, the open tab, pressing the up-arrow, generating variants, or reusing a previous prompt style. By default, after creating Grok Imagine prompts from a user description or uploaded image, submit those prompts to Grok automatically unless the user explicitly asks for prompts only, asks not to open Grok, or asks to review before submission.

Use the Chrome plugin/skill, not the in-app browser, because Grok usually depends on the user's logged-in Chrome session.

## CMS Prompt Generator

When the user asks for prompt generation, image prompt variants, or supplies a scene/image to turn into prompts, create polished, distinct AI image prompts, then submit them to Grok Imagine automatically. Follow the user's requested count, style, format, length, medium, mood, and level of detail. If the user does not specify a count, create three versions by default. If the user explicitly asks for prompts only, do not submit; just provide the prompts in chat.

Input modes:

- Text description: proceed directly unless the description is fewer than 5 words or deeply ambiguous. In that case, ask one specific clarifying question, then generate after the user answers.
- Image upload: analyze the image silently and proceed without clarification.

For uploaded images, internally read the subjects, appearance, pose, expression, setting, time of day, weather, lighting, color palette, mood, genre feel, camera angle, framing, and depth of field. Before the prompts, include a 2-3 sentence maximum image read:

`Reading your image: [brief neutral description of what's in it: subject, setting, mood, lighting]. Generating prompt versions below.`

For image-based prompts:

- Preserve subject identity, setting, and emotional core.
- Do not copy the image's existing style verbatim unless the user explicitly asks for faithful style matching.
- Reinterpret lighting direction, angle, framing, time of day, medium, mood, or artistic treatment across versions when variants are requested.
- If the image contains a real identifiable person, describe appearance generically, such as "a woman with short dark hair in her 30s"; do not use names.
- If the image is already a cinematic screenshot or AI art, mention that briefly in the image read and still generate evolved variations.
- Add details to attire, facial expression, background elements, or lighting that are not in the original image only when they fit the requested direction. Do not add story elements or specific identities unless the user asked for them.

Prompt rules:

- Match the user's requested prompt count. If unspecified, default to three versions for a fresh prompt-generation request.
- Match the user's requested length. If unspecified, use enough detail to make the prompt image-ready without padding.
- Match the user's requested medium and style, such as cinematic realism, anime, illustration, product render, editorial portrait, poster art, abstract, surreal, architectural visualization, logo concept, or any other requested direction.
- For every character prompt, include a concise body type description. If the user specifies body type, preserve it. If not, infer a tasteful, non-explicit body type consistent with the character, genre, wardrobe, and composition.
- Include camera, composition, lighting, material, mood, or rendering details when useful, but do not force cinematic or photorealistic language when it does not fit the request.
- Do not require a fixed signature, fixed word count, fixed style phrase, fixed camera language, or mandatory `movie screenshot`, `film still`, `photorealistic`, or `hyperrealistic` wording unless the user asks for those qualities.

For cinematic or photorealistic requests, a useful prompt order is:

1. Subject and action.
2. Setting and environment.
3. Lighting direction or time of day.
4. Camera feel.
5. Style anchors and genre cues.
6. Optional quality and atmosphere details.

Default three-version strategy:

- V1: straightforward interpretation, faithful to input, clean composition.
- V2: shift the mood, medium, palette, lighting, or narrative moment while preserving the core idea.
- V3: change angle, scale, layout, abstraction level, or visual treatment.


*💡 Tip: Paste any of these directly into Grok Imagine.


When submitting automatically, ignore the paste tip above; report the completed submission status instead.

## Iteration Mode

When the user's follow-up references a previous version or asks to tweak/refine, iterate on the previous prompt set instead of starting fresh. Triggers include version references, "the second one", "that last one", "make it", "change", "darker", "more", "less", "try", "adjust", "add", "remove", "I like X but", "now do a close-up", "wide shot version", or "what about at night".

Iteration rules:

- If the user references a specific version, regenerate only that version and label it clearly, such as `V2 — Revised`, `V1 — Night Version`, or `V3 — Take 2`.
- If the user asks to change all three or shift the whole concept, regenerate all three in the standard format.
- If the user asks for another option, generate a single `V4 — [Label]` without replacing the others.
- Preserve all unchanged elements, including subject, setting, camera choices, style, and constraints unless explicitly changed.
- Carry forward the original scene/image and previous versions. Do not ask the user to re-describe them.


## Workflow

1. If the user explicitly asks for prompts only, use the CMS Prompt Generator and do not open Grok.
2. Otherwise, for prompt-generation requests, uploaded image-to-prompt requests, variant requests, or direct Grok Imagine generation requests, generate or use the requested prompt(s), then load the Chrome skill before browser work and submit them automatically.
3. Connect to Chrome through the `extension` browser backend.
4. List open Chrome tabs with `browser.user.openTabs()`.
5. Choose the most relevant tab whose URL contains `grok.com/imagine`.
   - Prefer a tab in a Codex/Grok task group or the most recently opened Grok Imagine tab.
   - If no Grok Imagine tab is open, open or navigate a Chrome tab to `https://grok.com/imagine`.
6. Claim the selected tab with `browser.user.claimTab(tabInfo)`.
7. Wait for `domcontentloaded`, then inspect the visible DOM.
8. Confirm the page is usable:
   - If a sign-in, subscription, unavailable, or safety block screen appears, stop and report exactly what Grok needs from the user.
   - If the page is still loading, wait briefly and refresh the visible DOM before interacting.
9. Find the prompt editor, usually a visible `contenteditable="true"` div or textarea.
10. For each prompt to submit:
   - Click the editor, select all existing text if needed, and paste through the tab clipboard.
   - Verify the editor contains the intended prompt before clicking Submit.
   - Find the enabled submit button, usually a `button` with `aria-label="Submit"` or the visible up-arrow/generate button.
   - Click Submit, then wait for that prompt's image set to finish generating before submitting any next prompt.
   - Treat the image set as finished only when the submitted prompt/result is visible, generated images are loaded, image action controls such as `Save`, `Saved`, `Make video`, or `Generate More` are available, and no visible busy state such as generating, creating, loading, queued, or preparing remains.
   - Refresh the DOM while waiting and between submissions because Grok often replaces node ids after each generation.
11. Keep the Grok tab open with `browser.tabs.finalize({ keep: [{ tab, status: "handoff" }] })` unless the user explicitly wants it closed.

## Prompt Handling

Preserve the user's requested subject and style. Lightly rewrite prompts only to make them clearer for image generation, add explicit constraints, create requested variants, and include body type descriptions for character prompts. For revisions, the prompt submitted to Grok must be complete and self-contained, with all retained details repeated explicitly rather than referenced indirectly.

When the user supplies a rough idea rather than a finished prompt, make it image-ready by adding only practical visual details:

- medium or format, such as photorealistic, cinematic still, editorial portrait, concept art, or product render
- composition and camera language, such as close-up, wide shot, eye-level, overhead, 35mm lens, or shallow depth of field
- lighting and environment, such as soft window light, neon street light, studio lighting, misty forest, or clean white background
- quality constraints, such as sharp focus, coherent anatomy, readable text only when requested, and no watermark

Avoid adding story elements, identities, brands, logos, or copyrighted characters unless the user asked for them.

When the user asks for multiple versions or the CMS prompt set is generated, submit each version as a separate prompt sequentially by default. After clicking Submit for one version, wait until its generated images are finished and image actions are available before pasting or submitting the next version. Do not only fill the box and stop unless the user specifically asks to leave it ready or asks to review before submission.

## Variant Pattern

For variants, keep the base scene stable and vary only the requested attributes. Example attributes:

- ethnicity or race
- skin tone
- hair color
- hair length or texture
- clothing/equipment changes
- lighting or camera angle

Use direct, respectful descriptors such as:

- "adult Black woman with deep brown skin and short natural coily black hair"
- "adult East Asian woman with warm light skin and straight shoulder-length black hair"
- "adult Latina woman with tan olive skin and long wavy dark auburn hair"

Use this structure for multi-prompt batches:

1. Create a stable base prompt.
2. Create short variant labels for your own tracking.
3. Submit one prompt at a time.
4. Wait for the generated images from that prompt to finish before moving to the next prompt.
5. Tell the user how many prompts were submitted and whether generation fully finished.

## Practical Notes

- If the Submit button is disabled, the prompt text has not landed in the editor; re-click the contenteditable div and paste again.
- If a locator or node id goes stale after the page updates, refresh the visible DOM and use the new `node_id`.
- If multiple Grok tabs are open, use visible title, URL, recency, and tab group to choose the most likely active tab.
- If Chrome extension communication fails, follow the Chrome skill's recovery instructions and do not use OS-level browser scripting as a workaround.
- If a prompt remains in the editor after clicking Submit, check for validation messages, blocked content, or a disabled button before retrying.
- If Grok starts generating but the final images are not ready before the turn ends, do not submit additional queued prompts. Hand off with the tab open and say which prompt is still generating and which prompts remain unsubmitted.
- Before submitting a revision prompt, scan it for dependency phrases such as "previous", "same as before", "keep the same", "from the last image", or "that version". Replace them with explicit retained details before clicking Submit.
- Before submitting any character prompt, verify it includes a body type description. Add one if missing, keeping it tasteful, non-explicit, and consistent with the user request.
- Do not download, copy, or modify generated images unless the user asks.
