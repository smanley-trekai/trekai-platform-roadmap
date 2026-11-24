# Agent instructions

## Purpose and sources

This repository holds TrekAI platform improvement proposals, presentation files and native Miro diagram artifacts. Work here concerns planning and review material unless the user's task explicitly includes implementation.

Read `README.md` for navigation and the mapping between eight presentation topics and twelve proposal folders. Consult `diagram-design-plan.md` and the relevant dated entries in `progress.md` before changing content. Use `bulletpoints.md` for original proposal intent and `meeting-2026-11-12-090251.md` for supporting discussion. Later progress entries can supersede earlier notes; historical completion does not mean implementation approval.

Use Trek Learning and Hub/LMS consistently. TrekCAP is the adaptive engine used with TrekFinder. Preserve source-access, environment and product boundaries described in the proposals.

## Content changes

- Distinguish verified current behavior, reported information, proposals and unresolved decisions. Keep source dates and provenance when describing current-state evidence.
- Do not invent owners, approval authority, response targets or implementation status. Mark unresolved details explicitly.
- Keep the relevant proposal artifacts, design plan, progress log and presentation content consistent when the requested change affects them.
- Preserve historical evidence and archived baselines. Record material changes, checks, open questions and next steps in `progress.md`.
- Keep credentials and secret values out of documents and generated files. Use secret references where necessary.

## Presentation maintenance

- `Presentation/index.html` is the combined deck; `Presentation/01.html` through `08.html` are editable topic copies. Keep corresponding slides synchronized.
- Preserve the established 16:9 style, offline operation, keyboard controls, topic menu and progressive point reveals.
- Update slide counts, menu targets and documentation if the structure changes. Keep IDs unique and links valid.
- After presentation changes, inspect affected slides in a browser and verify navigation, animation and text fit. Check the relevant topic copy as well as the combined deck.
- There is no package installation or application build required to open the HTML presentation.

## Diagram maintenance

- Preserve native editable Miro shapes, text and attached connectors. Follow `diagram-design-plan.md` for layout, labels, evidence and audience needs.
- Read each builder or revision script before running it. These scripts can overwrite source artifacts, and some snapshots reflect later live edits.
- `*.miro.svg` contains saved live Miro identities. Use the live board and existing identities for edits; confirm current state before applying changes.
- `*.canvas.svg` is a fresh-composition source. Do not recreate it on the existing board when updating diagrams, as that duplicates content.
- Preserve `*.verified.svg`, operation responses and prior snapshots as records of their original operations. Save fresh read-back evidence for new edits.
- For changed diagrams, check XML validity, unique IDs, connector references, content and frame bounds. For live changes, also read back and visually inspect the affected frames.
- Treat the Miro link in `README.md` as a navigation reference; use the standard board URL for tools that require it.

## Scope and validation

Use checks appropriate to the actual change. Copying files requires file-integrity and link checks; it does not require running diagram generators or editing the live board. Local presentation and documentation edits do not require changing infrastructure, access permissions or delivery workflows. Follow the user's requested scope.
