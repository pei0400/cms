---
name: cms-image-generator
description: Create detailed, production-ready text prompts for Crimson Muse Studio (CMS) image concepts, then use the Grok Imagine image-generation skill to submit those prompts and generate images. Use when the user asks to make CMS product images, lifestyle images, promotional visuals, social content, ads, mockups, or other image assets through Grok Imagine from a brief idea, rough direction, product name, theme, or campaign concept.
---

# CMS Image Generator

## Overview

Turn a short CMS image idea into a clear, detailed image-generation prompt, then hand it to `$grok-imagine-generate` so Grok Imagine creates the image. Optimize for visually rich, commercially useful results that fit the requested product, audience, placement, and style.

## Workflow

1. Collect or infer the essentials:
   - Subject or product being shown
   - Intended use, such as product listing, social post, ad creative, hero image, lifestyle scene, or mockup
   - Desired style, mood, season, color palette, background, and aspect ratio when provided
   - Any text, logo, or branding requirements

2. If required details are missing, make reasonable CMS-friendly assumptions instead of blocking. Ask a concise question only when the image would likely be wrong without the answer, such as an unknown product identity or mandatory text.

3. Write one detailed prompt before using Grok Imagine. Include:
   - Main subject and composition
   - Setting, props, lighting, lens or rendering style, color direction, and mood
   - Surface/material details relevant to the product
   - Commercial polish, realism level, and quality cues
   - Aspect ratio or format if known
   - Clear negative constraints for artifacts, warped text, extra limbs, misspelled words, clutter, watermarks, logos, or off-brand elements

4. Show the final prompt to the user in the response when helpful, especially if they requested the prompt itself or may want to reuse it.

5. Use `$grok-imagine-generate` to send the prompt to Grok Imagine and generate the images. Follow that skill's instructions for operating Chrome/Grok, submitting prompts, queueing multiple generations, and handling iteration.

## Prompt Pattern

Use this structure, adapting naturally to the request:

```text
Create [asset type] for Crimson Muse Studio featuring [subject/product]. The scene shows [composition and focal point] in/against [setting/background]. Style: [photorealistic/editorial/3D render/etc.], [mood], [lighting], [camera/lens or render cues]. Include [materials, textures, props, seasonal details, color palette]. Make it suitable for [commerce/social/ad/listing/use case], polished, high-resolution, sharp focus, balanced negative space where needed. Avoid [negative constraints].
```

## CMS Defaults

When the user does not provide direction, prefer:

- Clean, premium, e-commerce-ready visuals with strong product clarity
- Natural lighting or soft studio lighting, depending on the asset type
- A composed scene with enough context to feel intentional, but not so much clutter that the product is lost
- Color palettes that feel polished and saleable rather than overly monochrome
- No readable text unless the user explicitly asks for text
- No invented brand logos unless the user provides or requests them

## Variations

For multi-image requests, create distinct prompt variants rather than repeating the same wording. Vary useful dimensions such as:

- Scene type: studio, lifestyle, flat lay, close-up, packaging mockup, seasonal setup
- Mood: elegant, cozy, bold, minimalist, playful, dramatic
- Format: square product image, vertical social post, wide banner, transparent-background cutout if supported by the target tool
- Audience or occasion: giftable, boutique, holiday, self-care, event, launch campaign

## Handoff

After drafting the prompt, invoke `$grok-imagine-generate` and pass the exact prompt text. If Grok Imagine returns options or requires iteration, refine the prompt based on the visible result and resubmit through `$grok-imagine-generate`.
