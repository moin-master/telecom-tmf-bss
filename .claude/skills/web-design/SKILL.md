---
name: web-design
description: Visual design rules for the web app: clean, minimal, professional, on a white or blackish-gray background with lemon yellow (#FFF700) as the single accent. Read before styling any page or component in /web.
---

# Web design: lemon on white and blackish gray

Palette source: https://paletadecolores.org/en/colors/lemon-yellow.html (lemon yellow `#FFF700`). The storefront is called **Lemon Mobile**. The look is clean, calm and confident: neutral surfaces, generous whitespace, one bright accent used with restraint. It should feel like a serious product, not a theme.

## Themes: white and dark

Both themes are first-class and the visitor chooses: a toggle button (sun and moon icons, no emoji) sits in the header next to the cart.

- The theme lives on `<html data-theme="light|dark">`. CSS uses `:root[data-theme='dark'] ...`, never `@media (prefers-color-scheme)` directly.
- First visit follows the system setting; after the visitor toggles, the choice is stored in `localStorage` (`bss.theme`, always inside try/catch). Until they choose, system changes are followed live.
- A small inline script in `index.html` sets `data-theme` before first paint so there is no flash. `hooks/useTheme.ts` owns the state and updates the `theme-color` meta tag.
- Every new component must look right in both themes; use the tokens, never fixed colours (the lemon, `--ink` and burst dots are the only fixed colours).

## Palette (CSS variables in `src/styles/tokens.css`)

| Role | Light | Dark |
|------|-------|------|
| Page background | white `#FFFFFF` | blackish gray `#141414` |
| Surface (cards) | white `#FFFFFF` | `#1C1C1C` |
| Band / subtle fill | `#F6F6F3` | `#242424` |
| Text | blackish gray `#1C1C1A` | `#F4F4F1` |
| Muted text | `#5C5C57` | `#A8A8A0` |
| Lines | `#E6E6E1` | `rgb(255 255 255 / 0.1)` |
| Accent | lemon `#FFF700` | lemon `#FFF700` |

Lemon scale from the palette: tints `#FFFED9`, `#FFFDB2`, `#FFFB80`, `#FFF94C`; shades `#CCC600`, `#999400`, `#666300`, `#333100`.

## How lemon is used

- **Always with dark text.** Black text on lemon is 18.6:1; white on lemon is 1.1:1 and is never allowed. Lemon text on a white background is never allowed either.
- Where it appears: primary buttons, the selected filter chip, the cart count badge, small badges, one highlighter-style underline on a headline phrase, the circle behind each product emoji, the hero panel, check marks. Not everywhere: if more than about a tenth of a screen is lemon, tone it down.
- In dark mode lemon also works as text and as links, because it is 17:1 on blackish gray. In light mode links and headings stay blackish gray (underlined links), with lemon only as a highlight behind them.
- Hover shade: `#FFEF00`. Tints `#FFFED9` and `#FFFDB2` are for soft backgrounds (icon tiles, badges) on white.

## Type and shape

- One family, **Inter** (400, 500, 600, 700, 800). Headings 700 to 800, tight tracking (-0.03em to -0.04em), sizes clamp(2.2rem, 5vw, 3.8rem) for hero. Body 16 px and up, line height 1.55. Numbers use `font-variant-numeric: tabular-nums`. Sentence case everywhere.
- Radius 16 to 24 px. 1 px borders. Shadows are light and layered (`0 1px 2px` plus a soft larger one). No gradients, no hard shadows, no thick borders, no rotation.
- Plenty of whitespace: 24 to 32 px gaps in grids, 64 to 96 px between sections.

## Motion

Small and purposeful: 150 to 300 ms eases, hover lift of 2 to 4 px, a gentle fade-up on cards, a confetti burst (dark and lemon dots) when an item is added. `prefers-reduced-motion` turns all of it off.

## Copy

Clear and plain. Say what it is and what it costs. No slang, no exclamation marks.

## Per-page checklist

1. One idea per screen, with a clear primary action in lemon.
2. At least two considered details beyond the default (for example the highlighter underline, the lemon circle behind product emoji, a sticky order summary, a tidy empty state).
3. Looks right at 390 px and 1280 px, in light and dark.
4. Looked at in a real browser or screenshot, and revised once after looking. Ask: does it look like a real company's product? If it looks like a template or a costume, simplify.

## Guardrails (not optional)

- WCAG AA contrast: 4.5:1 for text, 3:1 for large text and UI borders. Check lemon pairs: only dark text on lemon.
- Focus ring: 3 px blackish gray outline with offset in the white theme, lemon in the dark theme, on every interactive element.
- Touch targets at least 44 px. `prefers-reduced-motion` respected.
- Emoji are product illustrations only (offers have no photos); they carry `aria-hidden="true"`, and the name is in text. No emoji in headings, buttons or navigation.
- Real data first: names, descriptions and prices come from the API. Do not invent offers, prices or claims.
- Effects in CSS only. No UI or animation library unless asked. No real brand names or logos.

## Lessons

- Do not use `-webkit-text-stroke` outlines on headings: glyph contours overlap and look broken.
- Check emoji in a screenshot before keeping them: 🪪 renders as an ID card with a face; 💳 is used for SIM and prepaid.
- Phone-width header: hide secondary text below 520 px so the cart button is not clipped.
- Judge a screenshot for mood, not only bugs. Two earlier directions (a neon dark theme, then a pastel Gen-Z theme) passed every technical check and were still rejected.
