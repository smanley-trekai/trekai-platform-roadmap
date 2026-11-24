# TrekAI Platform Roadmap

Proposals, architecture diagrams and presentations for improving TrekAI's DevOps, infrastructure, security and operations across Trek Learning (Hub/LMS) and TrekCAP/TrekFinder.

These materials support team review and planning. A diagram or completed presentation does not establish approval or implementation of a proposal. Current-state evidence and open decisions are recorded in the supporting notes.

## Start here

- Open [the combined presentation](presentation/index.html) in a browser. It contains 100 slides across eight platform topics and works offline without installation. Topic 09 in its menu opens the separate [AI guide roadmap presentation](ai-guide-roadmap/visuals/ai-agents-team-presentation.html).
- Read [presentation instructions](presentation/README.md) for individual topic decks and keyboard controls. Use **T** to open the topic menu, **Space** or **Right Arrow** to reveal points, and **F** for fullscreen.
- View [the Miro diagrams](https://miro.com/welcomeonboard/ZUkwd3ZSaXRHa2NnYlE5ZGlWUXdPdHNMa01hNE1NSjRLSm5ON0ZLRFo4TnlicDNLcytGejErTkEyYkNubnhkdCtOc3dzeStGSDB3Q3dBQ1prODhJMU8vYjQ2OVlTT3ZCSTB6SDJobDBVYXNvTVpPSEk3OHMvSkViTHd4RUczQ2lBd044SHFHaVlWYWk0d3NxeHNmeG9BPT0hdjE=?share_link_id=794227503994) using the supplied sharing link. The [direct board link](https://miro.com/app/board/uXjVEOGaQYU=/) and individual frame links in [progress.md](progress.md) provide navigation for accounts with access.
- Review [the diagram design plan](diagram-design-plan.md) for proposal scope and visual conventions, and [the progress log](progress.md) for dated changes, verification and open questions. Later entries may supersede earlier status notes.

## Repository contents

| Path | Contents |
| --- | --- |
| `presentation/index.html` | Combined, self-contained HTML presentation. |
| `presentation/01.html` through `08.html` | Editable topic copies of the presentation. |
| `presentation/archive/` | Preserved earlier presentation versions. |
| `ai-guide-roadmap/` | AI-agent learning material and the separately linked team presentation. |
| `proposals/01/` through `12/` | Native Miro diagram sources, Python builders, live snapshots, verification exports and operation records. |
| [diagram-design-plan.md](diagram-design-plan.md) | Diagram structure, audience needs, workflow conventions and proposal scope. |
| [progress.md](progress.md) | Historical progress, frame links, evidence, verification and follow-up work. |
| [bulletpoints.md](bulletpoints.md) | Original proposal list and intent. |
| [meeting-2026-11-12-090251.md](meeting-2026-11-12-090251.md) | Supporting meeting discussion and presentation expectations. |
| [AGENTS.md](AGENTS.md) | Instructions for agents maintaining this repository. |

## Topics and proposal mapping

The combined presentation groups twelve proposals into eight platform topics. Its menu also includes topic 09, a link to supplementary AI-agent learning material. Presentation topic numbers and proposal folder numbers use different mappings.

| presentation topic | Proposal folders |
| --- | --- |
| 01 Monorepo | `02` DevOps, `03` Hub/LMS, `04` TrekCAP/TrekFinder |
| 02 QA environments | `05` QA, sales demo and client pilot environments |
| 03 Terraform deployment automation | `01` Terraform review and controlled execution |
| 04 GitOps standardization | `11` GitOps / SDLC |
| 05 Observability and alerting | `07` Observability and alerting |
| 06 Microsoft Entra ID and privileged access | `08` Google Cloud identity, `09` GitHub identity, `10` team structure, PAM and role-based access |
| 07 Documentation | `06` Documentation / knowledge base |
| 08 Security | `12` Security coverage and implementation |
| 09 AI guide roadmap | Supplementary learning presentation in `ai-guide-roadmap/`; separate from the twelve platform proposals |

## Working with the materials

Update the combined presentation and the corresponding topic file together, preserving the existing slide style, navigation and point-by-point animation. Keep prior versions in `presentation/archive/` when retaining a reviewed baseline matters.

The diagram files use Miro Canvas Composer SVG conventions. Some labels and connectors depend on Miro's native interpretation and may not display fully in an ordinary SVG viewer. Treat `*.miro.svg` as saved live-ID snapshots and `*.verified.svg` as verification records. `*.canvas.svg` compositions are for fresh creation; importing them onto the existing board can duplicate diagrams. Builders and revision scripts write artifacts, so inspect them before running them.

Record meaningful revisions and verification in [progress.md](progress.md), and update the design plan when scope or conventions change. Keep proposed responsibilities, approvals and future behavior distinct from verified current behavior. Security source provenance is preserved in [proposal 12 research notes](proposals/12/research-notes.md).
