---
name: Serene Reflections
colors:
  surface: '#fbf9f4'
  surface-dim: '#dbdad5'
  surface-bright: '#fbf9f4'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f5f3ee'
  surface-container: '#f0eee9'
  surface-container-high: '#eae8e3'
  surface-container-highest: '#e4e2dd'
  on-surface: '#1b1c19'
  on-surface-variant: '#424843'
  inverse-surface: '#30312e'
  inverse-on-surface: '#f2f1ec'
  outline: '#727972'
  outline-variant: '#c2c8c1'
  surface-tint: '#476550'
  primary: '#476550'
  on-primary: '#ffffff'
  primary-container: '#7d9d85'
  on-primary-container: '#173422'
  inverse-primary: '#adcfb5'
  secondary: '#4f6167'
  on-secondary: '#ffffff'
  secondary-container: '#d2e6ec'
  on-secondary-container: '#55676d'
  tertiary: '#725a41'
  on-tertiary: '#ffffff'
  tertiary-container: '#ad9074'
  on-tertiary-container: '#3d2a15'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c9ebd0'
  primary-fixed-dim: '#adcfb5'
  on-primary-fixed: '#032110'
  on-primary-fixed-variant: '#304d39'
  secondary-fixed: '#d2e6ec'
  secondary-fixed-dim: '#b7cad0'
  on-secondary-fixed: '#0c1e23'
  on-secondary-fixed-variant: '#384a4f'
  tertiary-fixed: '#ffdcbd'
  tertiary-fixed-dim: '#e1c1a2'
  on-tertiary-fixed: '#291805'
  on-tertiary-fixed-variant: '#59422b'
  background: '#fbf9f4'
  on-background: '#1b1c19'
  surface-variant: '#e4e2dd'
typography:
  headline-xl:
    fontFamily: Manrope
    fontSize: 40px
    fontWeight: '700'
    lineHeight: 48px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Manrope
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
  headline-lg-mobile:
    fontFamily: Manrope
    fontSize: 28px
    fontWeight: '600'
    lineHeight: 36px
  body-lg:
    fontFamily: Literata
    fontSize: 18px
    fontWeight: '400'
    lineHeight: 32px
  body-md:
    fontFamily: Literata
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 28px
  label-md:
    fontFamily: Manrope
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.05em
  label-sm:
    fontFamily: Manrope
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  unit: 8px
  container-margin: 24px
  gutter: 16px
  section-gap: 48px
  element-gap: 12px
---

## Brand & Style

The design system is centered on the concept of "Digital Sanctuary." It aims to evoke a sense of calm, safety, and deep introspection, transforming the smartphone into a private space for emotional processing. The target audience includes individuals seeking mental clarity, mindfulness practitioners, and those managing emotional well-being through journaling.

The visual style is a blend of **Minimalism** and **Tactile Modernism**. It avoids the sterility of pure minimalism by introducing soft, organic textures and a "paper-like" digital canvas. The interface is intentionally quiet, using generous whitespace to reduce cognitive load and allow the user's thoughts to take center stage. Every interaction is designed to feel deliberate and gentle, mirroring the slow pace of physical journaling.

## Colors

The palette is derived from natural, desaturated tones that promote physiological relaxation. 

- **Primary (Sage Green):** Used for growth-oriented actions and primary navigation. It represents balance and tranquility.
- **Secondary (Soft Blue):** Used for mood tracking and secondary information. It evokes a sense of peace and security.
- **Tertiary (Warm Sand):** Used for accents and highlights, providing a grounded, human warmth to the interface.
- **Neutral (Parchment):** The foundation of the UI. Rather than pure white, this warm off-white reduces eye strain and mimics the feel of high-quality notebook paper.

The color mode is primarily light to maintain an airy feel, though a "Twilight" (dark) mode should utilize deep charcoal-greens rather than pure blacks to maintain softness.

## Typography

This design system employs a dual-font strategy to balance modern utility with personal expression.

- **Manrope** is used for the interface "chrome"—navigation, buttons, and labels. Its clean, geometric sans-serif nature provides a sense of reliability and professional security.
- **Literata** is used exclusively for the content the user creates. As a refined serif font specifically designed for long-form reading, it gives journal entries a literary, intimate quality.

Line heights are intentionally generous (1.6x to 1.8x for body text) to create an open, breathable reading experience. Headlines should use tighter tracking for a more sophisticated, editorial appearance.

## Layout & Spacing

The layout philosophy follows a **Fluid Grid with Safe Margins**. 

On mobile, a single-column layout is mandatory to maintain focus, with a minimum horizontal margin of 24px. On tablet and desktop, the content container is capped at 720px width for journal entries to ensure optimal line lengths for reading and writing.

Spacing follows an 8px base unit. To reinforce the "airy" feel, vertical spacing between disparate sections (e.g., between the mood tracker and the recent entries list) should be aggressive, often exceeding 40px, to prevent the UI from feeling cluttered or "busy."

## Elevation & Depth

Hierarchy is established through **Tonal Layers** and **Soft Ambient Shadows**. 

Instead of traditional elevation, this design system uses subtle shifts in background color (e.g., a slightly darker "Paper" tint for the background and a pure "Neutral" for cards). 

Where shadows are necessary for interactivity (like floating action buttons), they must be highly diffused (30px+ blur) and low opacity (8-10%), using a slight tint of the primary Sage Green rather than black. This "glow-shadow" approach makes elements feel like they are gently resting on a surface rather than hovering high above it.

## Shapes

The shape language is organic and approachable. Sharp corners are avoided to minimize visual "tension." 

Standard components (cards, inputs) use a 16px radius (`rounded-lg`). Interactive elements like buttons and chips utilize a fully rounded (pill) shape to invite touch. Decorative elements, such as mood icons or background blobs, should favor imperfect, organic circles to reinforce the human, non-mechanical nature of the product.

## Components

### Buttons
Primary buttons are pill-shaped with a solid Sage Green fill and white text. Secondary buttons use a tonal ghost style—a subtle Sage border with no fill—to minimize visual competition.

### Journal Cards
Journal entry previews are cards with a soft background tint and no border. They display the date in `label-sm` (Manrope) and a snippet of the entry in `body-md` (Literata).

### Mood Chips
Small, circular or pill-shaped indicators using the palette's soft blues and greens. When selected, they should exhibit a soft "pulse" animation or a slight scale increase rather than a heavy border.

### Input Fields
Journaling inputs are "borderless" by default, appearing as a simple lined or blank page to encourage free-form writing. For structured data (like settings), use fields with a subtle `Neutral` fill and a very soft 1px border.

### Security/Privacy Indicators
Privacy is conveyed through subtle "Shield" or "Lock" icons in the status bar and during authentication, rendered in the Secondary blue to feel protective rather than alarming.