# Proposal diagram progress

## Working context

- Source proposals: [bulletpoints.md](bulletpoints.md).
- Design guide: [diagram-design-plan.md](diagram-design-plan.md).
- Supporting discussion: [meeting transcript](meeting-2026-11-12-090251.md).
- Destination board: https://miro.com/app/board/uXjVEOGaQYU=/
- Use editable native Miro shapes, text, and connectors. Do not flatten diagrams into images.
- Proposals are drafts for team discussion; creating a diagram does not approve implementation.
- After each proposal, update its status and record frames, links, design choices, verification, open questions, and the next step here.

## Proposal tracker

| ID | Proposal | Diagram status |
|---|---|---|
| 01 | Terraform PR review and controlled execution | Original diagrams accepted; promotion/validation companions added 2026-11-16, ready for review |
| 02 | DevOps monorepo | Created in Miro; editable draft verified and ready for review |
| 03 | Trek Learning (Hub/LMS) monorepo | Created in Miro; editable draft verified and ready for review |
| 04 | TrekCAP and TrekFinder repository consolidation | Created in Miro; editable draft verified and ready for review |
| 05 | QA, sales demo and client pilot environments | Updated in Miro with separate purposes, acceptance and lifecycle; ready for review |
| 06 | Documentation / knowledge base | Created in Miro; editable draft verified and ready for review |
| 07 | Observability and alerting | Created in Miro; editable draft verified and ready for review |
| 08 | Entra ID for Google Cloud | Created in Miro; editable draft verified and ready for review |
| 09 | Entra ID for GitHub | Created in Miro; editable draft verified and ready for review |
| 10 | PAM and role-based access | Created in Miro; editable draft verified and ready for review |
| 11 | GitOps / SDLC | Created in Miro; editable draft verified and ready for review |

## Proposal 01 — Terraform PR review and controlled execution

### Session: 2026-11-13

- Request: Build the first proposal on the supplied board as an editable example for the user to review.
- Intended views: overview/proposed change; developer/reviewer/automation workflow; DevOps delivery plan.
- Proposal intent: Terraform review on every PR using a GitHub Actions runner; plan → view results → approval → apply; main → dev.
- Draft workflow choice: PR checks and plan → human review/approval → merge to main → apply to dev → results. Approval/merge placement remains a team decision.
- Current-state evidence: the transcript reports merge triggering apply; a complete current pipeline has not been independently verified.
- Open questions: review tool; checks for PRs without Terraform changes; approval authority; PR approval versus a separate apply gate; runner/execution identity; handling changed plans and apply failures.
- Execution status: Miro plugin denied access to the destination board. No board items were created or changed.

### Prepared content

- [Native Canvas Composer source](proposals/01/proposal-01.canvas.svg): three frames with editable shape, text, and attached-connector definitions; no images, HTML embeds, or flattened diagram widgets.
- [Source builder](proposals/01/build_source.py): generates the composition and checks its structure.
- **01A — Overview:** partial reported current flow, proposed plan/review/approval/apply flow, main → dev mapping, expected outcome, and team decisions.
- **01B — People and workflow:** application developer, runner, reviewer, merge/environment, and feedback/exception lanes; rejected approval, failed checks/plan, and apply failure paths. QA is identified as a possible consumer of the dev outcome, not an invented approval gate.
- **01C — Delivery plan:** inventory → design agreement → implementation → validation/pilot, with proposed role ownership and completion evidence.
- Visual convention: blue proposed nodes, gray reported/context nodes, yellow decisions/exceptions; embedded labels, consistent typography, and attached arrow definitions. All editable when created through Canvas Composer; viewing the source as an ordinary SVG does not reproduce Miro's embedded node labels.
- Local verification: builder checks XML output, unique local IDs, connector references, three frames, and absence of image/embed elements. No rendered Miro layout or live editability has been verified yet.

### Access issue and resume instructions

- The board-specific composer request and canvas overview both returned **Board access denied** for `https://miro.com/app/board/uXjVEOGaQYU=/`.
- The plugin identity request succeeded, so the plugin is connected; the available evidence does not establish why this board is inaccessible.
- Asked the user to check edit access for the Miro account connected to the plugin or provide an accessible board URL.
- Native flowchart format guidance returned unavailable; basic shape/connector DSL and free-form shape guidance were available. The saved composition honors the user's explicit editable-shape request.
- Resume by checking access with `canvas_search` overview, reading the intended placement area if the board contains content, and positioning the saved composition clear of existing items.
- Then create with `canvas_create_from_svg`, save the returned `result_svg` with actual Miro IDs, resolve any changed dimensions, and read back the created frames to verify the layout and native items.
- Record frame deep links here after successful creation. Call `board_show` once after all content is verified.

### Invitation-link retry: 2026-11-13

- User supplied a Miro `welcomeonboard` invitation link to try for access.
- The Miro canvas plugin rejected that URL format: it requires a normal `https://miro.com/app/board/...` URL and cannot directly redeem the invitation through this tool.
- Retried the original board URL: still **Board access denied**.
- BrowserOS neo MCP tools were unavailable. Computer Use inventory found BrowserOS neo, but opening it was rejected with **Computer Use was not approved to use BrowserOS neo**. No invitation was opened or accepted.
- No changes were made to the board. The local three-frame source remains ready.
- Next action needed: open/accept the invitation with the same Miro account connected to the plugin, or reconnect the plugin to an account that already has edit access; then retry the standard board URL.

## Next step

### Miro desktop fallback: 2026-11-13

- User explicitly selected both the Miro plugin and the Miro desktop app.
- Plugin board search still returned **Board access denied**; plugin identity remained unchanged.
- The selected Miro desktop app successfully opened the requested board, named **Proposed Tech Changes**. Its accessibility state reported no objects on the board.
- Submitted a Miro Sidekick request to create three frames with native editable shapes, text, attached arrows, draft/audience labels, decisions, and failure paths. Requested no images or flattened embeds.
- Generation is pending verification. The local Canvas Composer source was not uploaded; this attempt uses the authorized desktop UI.

### Latest plugin retry: 2026-11-13

- User requested another retry after the invitation-link attempt.
- Retried `canvas_search` overview against the original board URL through the Miro plugin.
- Result: **Board access denied**. No items were created or modified; Proposal 01 remains prepared locally and pending upload.

Current next step (2026-11-16): review Proposal 11, GitOps / SDLC, then consolidate feedback and decisions across 01–11. All eleven proposal diagram sets are now created. The original Proposal 01 diagrams were accepted; the remaining drafts and companions are available for review, not approved implementation.

### MCP diagnosis: 2026-11-13

- Both the newly configured `mcp__miro` server and the existing Miro app connection report user `3458764684425343129`, organization `3458764558053565357`, and active team `3074457346817538340`.
- `content_item_list_roles` confirms that this same user is the **owner** of the proposal board. Missing ordinary board permission is therefore ruled out.
- The desktop UI observed earlier identifies the proposal board's team as **Architecture**, ID `3458764688959218790`, which differs from the MCP active team.
- The configured direct endpoint is the official `https://mcp.miro.com/`; no custom auth overrides are configured in that server section.
- Search and role listing succeed for the proposal board, while canvas overview, comments, board-space lookup, and board-scoped composer requests return **Board access denied**.
- Control test: the MCP lists the Arch: Current State space and its Adventure - Current State board, then successfully reads that board's canvas overview (52 items) and its space. This confirms the canvas tools work within the currently authorized team.
- Miro's official troubleshooting documentation states that MCP authorizes one team at a time, the latest client/team authorization supersedes prior authorization, and duplicate plugin/manual connections can cause auth confusion: https://developers.miro.com/docs/miro-mcp-server-faq-and-troubleshooting .
- Required correction: reauthorize the intended Miro connection while viewing the proposal board and select **Architecture**. Keep one active Miro connection to avoid competing authorization sessions. Verified CLI commands for the manually configured server are `codex mcp logout miro` and `codex mcp login miro`; the user must select the intended team in OAuth.
- No credentials, sharing permissions, board ownership, team location, or board contents were changed during diagnosis. Reauthorization has not been performed or verified.
- Next: confirm `user_who_am_i` reports team `3458764688959218790`, then retry the proposal board's canvas overview before creating Proposal 01.

### Retry after diagnosis: 2026-11-13

- At the user's request, retried both the direct Miro MCP and the existing Miro app connection.
- Both still report active team `3074457346817538340`; both proposal-board canvas overviews return **Board access denied**.
- The Architecture-team authorization is not reflected in either live connection. No board content was created or modified during this retry.

### Successful creation and verification: 2026-11-13

- The direct Miro MCP now reports Architecture team `3458764688959218790`. Canvas overview succeeded and confirmed an empty board before creation.
- Created Proposal 01 as three frames containing native editable shapes, text, and attached connectors. Initial creation: 85 items, zero failed or skipped; final read-back: 86 managed items, zero foreign or skipped items, including the added PR revision loop.
- [01A: Overview](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690359619682)
- [01B: People and workflow](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690359619683)
- [01C: Delivery plan](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690359619684)
- Preserved draft status, main to dev mapping, reported versus proposed distinctions, role ownership placeholders, and unresolved tool/approval/trigger decisions.
- Final refinements: named GitHub Actions explicitly in the overview runner; connected rejected approval through PR revision back to the PR event; labeled delivery progression arrows “Next”.
- Measured text bounds were smaller than authored text boxes and remained clear of other items. Visually inspected the overview, workflow, and delivery content in the Miro desktop app; node labels fit, connectors attach, and the workflow rejection/failure routes are visible without crossing nodes.
- [Latest Miro update source with actual IDs](proposals/01/proposal-01.miro.svg); [final board read-back](proposals/01/proposal-01.verified.svg); [initial creation response](proposals/01/proposal-01.created.json). Do not rerun create with the local source on this board; use the saved Miro IDs for future edits.
- Next step: user review of Proposal 01; Proposal 02 remains not started.
- Preview delivery: the separate Miro app connector's `board_show` returned Board access denied. This does not affect the successful direct-MCP creation, read-back, or desktop visual verification. Provide the standard frame link for review.

### Proposal refinement after second-brain review: 2026-11-13

- User requested refinement after discussing planning versus applying, PR versus execution approval, and environment scope. Updated the same three frames in place; their deep links above remain valid.
- Revised goal: standardize Terraform change review and controlled execution, building on existing development planning, then extending to staging and production.
- Corrected the current-state row using the second-brain answer `trekai-questions/cross-system/2026-11-09-tl-terraform-change-deployment-process.md` (updated Nov 10 against Nov 4 source evidence): existing development-root PR checks/plan and PR comments; no apply job or merge-to-apply trigger in that workflow. Current enforcement, successful runs, and apply ownership remain unverified.
- Replaced fixed `main → dev` framing with target selection by Terraform root, inputs and backend/state. Proposed merge destination is main; it does not select an environment. Each target requires its own plan, scoped identity and execution policy.
- Proposed flow: PR → checks/target plan → PR results → PR approval → merge → final plan from merged code/current state → execution authorization → apply approved plan → verify/report.
- Separated approval to merge code from authorization to execute the final plan. Explicit final-plan approval is proposed for staging/production; the dev gate policy remains a team decision. Failed/changed final plans block execution and require renewed planning/authorization.
- Added development pilot, staging extension, production extension; shared/common/RD and protected foundation scope remains to agree. QA/lab remains Proposal 05. No new branch mappings, named owners, dates, live controls, or implementation approval are implied.
- Delivery work now covers existing workflow/rules/apply inventory, shared-module consumer detection, per-target controls and identities, development pilot, final-plan consistency, concurrency and execution evidence, followed by coverage expansion.
- Verification: update preserved all 86 existing widget identities, added 18 items, and deleted none. Final read-back returned **104 managed items, zero skipped**. Visually checked all three frames in the Miro desktop app; shortened clipped labels and made the execution-lane background transparent so connector paths remain visible. Final approval and failure routes are legible.
- Updated `diagram-design-plan.md`, canonical [live source](proposals/01/proposal-01.miro.svg), [verified read-back](proposals/01/proposal-01.verified.svg) and [fresh-board export](proposals/01/proposal-01.canvas.svg). `build_source.py` now exports and validates the canonical reviewed snapshot, stripping live IDs only for fresh-board creation. Do not create that export on this existing board.
- Preserved the pre-refinement board snapshot in `proposals/01/proposal-01.before-refinement.svg`. The original bullet list and second brain were not edited. No Terraform commands, cloud changes, workflow triggers, or repository changes were executed.
- Next: user review of the refined Proposal 01. Proposal 02 remains not started.

### Audience readability and bullet formatting: 2026-11-13

- Converted 01C's pilot readiness and environment coverage content into left-aligned bullets, including the accompanying team-decision and plan-freshness panels.
- Added short reading cues below both headings. Pilot readiness now uses the leads “See the changes”, “Review current code”, “Check the final plan” and “Control execution”. Coverage explains Terraform root as an infrastructure component, module as reusable configuration, and state as Terraform's record of managed resources.
- Preserved proposal status and existing requirements. Added no new control commitments. Retained the user's current frame position, size and work-package layout; adjusted only the edited panels for readable spacing.
- Verified the bullet text, reading cues and panel fit in the desktop app; synchronized the canonical live snapshot, verified SVG and fresh-board export. The board now has 106 managed items, including two new reading cues.

### Friendlier work-package descriptions: 2026-11-13

- Rewrote the four 01C work-package cards as: “Understand today’s setup”, “Agree how changes should work”, “Try it in development”, and “Roll it out step by step”.
- Used short, full-sentence explanations of the existing phases, preserving the intended sequence, role ownership, frame layout and draft status. Four items updated; no items created or deleted.
- Visually verified all four cards fit without clipping. Synchronized the saved Miro source, verified SVG and fresh-board export.

### User review complete: 2026-11-16

- User confirmed “we're good with 01” and asked about Proposal 02.
- Proposal 01's diagram review is complete. This does not establish team approval to implement the proposed infrastructure changes.
- Next proposal: 02 — DevOps monorepo. Its diagrams remain not started.

### Environment promotion and requirement validation: 2026-11-16

- User asked to save the explanation of Terraform deployment/promotion and validation, then add it to Miro.
- Saved the detailed explanation, comparison of branch strategies, recommended flow, requirement checks, limitations and primary documentation references in [the design plan](diagram-design-plan.md#environment-promotion-and-requirement-validation).
- Added two editable companion frames to the right of the original Proposal 01 frames. Original 01A–01C and all Proposal 02 items were not changed.
- [01D: Branches and promotion](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690575950778): branch/commit versus environment target versus release/tag; proposed main → dev apply → dev verification → staging → production flow; alternative environment-branch strategy; failed-test stop; each target's own plan and explicit configuration/module-version promotion.
- [01E: Verify the requirements](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690575950779): before/after-apply examples for database settings, network/access, recovery and capacity; configuration validity versus acceptance; test evidence and promotion authority.
- Main-plus-promotion is a recommendation for discussion, not a newly approved deployment policy. The existing evidence remains development-only planning, with no apply job. Release/tagging is optional identification of a version; it does not select production or copy dev-only changes into production folders.
- Each environment needs its own root/inputs/state/identity, plan, authorization and verification. Development auto-apply policy, acceptance criteria, test owners, release strategy and supported approval mechanism remain team decisions. Per-change promotion is distinct from the phased rollout of the automation capability in 01A–01C.
- Creation returned **50 items, zero failed or skipped**: 2 frames, 31 shapes, 11 text items and 6 attached connectors. Scoped read-back returned all 50 managed items and all 6 connectors. The 35 excluded connectors belong to earlier frames outside the selection.
- Checked measured text bounds; all fit inside authored allocations with clear spacing. Visually inspected 01D and 01E in the Miro desktop app: labels fit, the promotion path and failed-test branch attach, and requirement rows are legible.
- Saved [canonical live companion source](proposals/01/proposal-01-promotion.miro.svg), [verified read-back](proposals/01/proposal-01-promotion.verified.svg), [creation response](proposals/01/proposal-01-promotion.created.json), [initial source](proposals/01/proposal-01-promotion.canvas.svg) and [builder](proposals/01/build_promotion_source.py). These companion files are separate from the original three-frame snapshot. Use live IDs for edits; do not recreate the initial source on this existing board.
- No Terraform execution, deployment trigger, repository migration or cloud change was performed.
- The separate Miro app preview connector returned **Board access denied**; direct-MCP creation/read-back and desktop inspection succeeded. Use the standard 01D/01E links above.

### Explain the relationship between 01B, 01D and 01E: 2026-11-16

- User asked to add the relationship information inside the boxes to make the diagrams easier to explain.
- Updated 01D's six process boxes with mappings to 01B: PR review = steps 1–5; merge = step 6; development apply = steps 7–9; verification = step 10; staging and production repeat steps 7–10 for their own targets. The failed-test panel explains that step 10 supplies acceptance evidence before further promotion.
- Labeled 01E's planned-configuration column as 01B steps 2–8 and its deployed-behavior column as step 10. Updated the acceptance and configuration panels to explain their role in that workflow.
- Added clickable links back to 01B from both companion subtitles. Added links in 01B's merge and verification boxes to 01D/01E, plus a short two-line navigation cue below the workflow. 01D's dev-verification box and 01E's acceptance panel link to each other.
- Preserved the user's current frame locations and two curved connectors from 01B to the detail views. Updated 19 existing items, created one navigation text item, and deleted none; Miro returned success with zero failed/skipped items.
- Visually inspected the updated 01D and 01E: step references, links and validation headings fit. Existing 01B node dimensions accommodate the added short references, and its new reading cue fits between existing footer panels.
- A subsequent fresh read-back failed twice because the direct Miro server could not discover OAuth metadata at `https://mcp.miro.com/`. The successful mutation response and desktop visual checks precede this connection error; do not replay the update or recreate items.
- Saved the [pre-edit live read](proposals/01/proposal-01.relationship.before.svg), [sparse update](proposals/01/proposal-01.relationship.update.svg), [successful update response](proposals/01/proposal-01.relationship.result.json), and [confirmed composition](proposals/01/proposal-01.relationship.confirmed.svg). The confirmed composition merges the held content with the server-returned identities; it is not a fresh post-update server read-back.
- Synced the original and companion `.miro.svg` canonical sources and fresh-board exports. The older `.verified.svg` files remain historical server read-backs; use the canonical sources or confirmed composition for these latest edits.

## Proposal 02 — DevOps monorepo

### Created and verified: 2026-11-16

- User authorized proceeding with Proposal 02 after accepting Proposal 01's diagrams.
- Created three frames below Proposal 01 on the same board, following its editable-shape format, typography and blue/gray/yellow conventions. Proposal 01 was not edited.
- [02A: Overview and tradeoffs](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690571914544): dated current repository examples alongside a proposed DevOps repository, folder areas, benefits, constraints, a separate-repositories/shared-standards alternative and team decisions.
- [02B: Change workflow](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690571914545): contributor → scope/dependency checks → affected-owner review → merge; failed checks and requested revisions; separate Terraform, GitOps and other automation execution expectations.
- [02C: Delivery plan](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690571914546): inventory → boundary agreement → development pilot → staged migration, with proposed role ownership, acceptance evidence, consumer updates, cutover and rollback.

### Evidence and design choices

- Used existing local evidence only; no GitHub refresh, repository migration or cloud operation was performed.
- [Saved GitHub inventory, 2026-11-03](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/reviews/github/reports/01-repo-inventory.md).
- [Identified GitOps repositories](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-questions/github/2026-11-09-how-many-gitops-repositories.md): two identified repositories in the Nov 3 snapshot, `tl-lms-gitOps` and `cap-gitOps`; environment folders indicate saved declarations, not verified runtime.
- [Infrastructure/GitOps supporting map and assessment](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-questions/cross-system/2026-11-09-gitops-supporting-repositories-and-components.md), including Nov 10 update: Terraform counterparts, adjacent infrastructure candidates, app workflow writers, Argo CD consumers and separate change processes. Sources are dated Nov 3–4 with static assessment Nov 6.
- Current examples: `tl-trekai-terraform`, `tl-trekcap-terraform`, `tl-lms-gitOps`, `cap-gitOps`. Adjacent candidates: `ir-terraform-temporary`, `b-metric-dashboard-terraform`, legacy `trekai-infra`.
- Ansible and other DevOps scripts remain scope to inventory; their current repositories were not invented. `devops/` is an illustrative repository name, not a decision.
- Consolidation is a proposal. Folder review rules are not read-access isolation; retain separate repositories where visibility requirements demand it. Shared commits do not make deployments atomic or unify Terraform state.
- Migration dependencies include app workflow destinations, GitHub App access, Argo CD URLs/revisions/paths, Terraform paths/module references/backends, identity bindings and review rules. Keep one writable source per migrated scope and rehearse consumer rollback.
- Proposal boundaries: Terraform execution in 01, application monorepos in 03/04, broader GitOps/SDLC policy redesign in 11.

### Verification and saved artifacts

- Creation succeeded: **77 items, zero failed or skipped**, consisting of 3 frames, 34 shapes, 30 text items and 10 attached connectors.
- Checked every changed text measurement: rendered boxes were smaller than authored allocations, remained clear of neighboring items and required no repositioning.
- Visually inspected all three frames in the Miro desktop app. Labels fit, panel spacing is consistent, progression arrows attach and exception/execution branches do not cross nodes.
- Scoped read-back returned all **77 managed items**, no foreign items, and all 10 Proposal 02 connectors. It also reported 25 unrelated Proposal 01 connectors excluded because their endpoints were outside this selection; these were not modified or missing from Proposal 02.
- [Canonical live source with Miro IDs](proposals/02/proposal-02.miro.svg), [verified read-back](proposals/02/proposal-02.verified.svg), [creation response](proposals/02/proposal-02.created.json), [initial creation source](proposals/02/proposal-02.canvas.svg), [source builder](proposals/02/build_source.py).
- Use live Miro IDs for edits. Do not rerun creation or upload the fresh composition again on this existing board.
- Open decisions: final scope and repository name; area ownership and access; shared dependency checks; cross-area execution ordering; history strategy; pilot and rollback acceptance. No implementation approval, dates or named owners are implied.
- Next: user review of Proposal 02. Proposal 03 remains not started.
- Preview delivery: the separate Miro app connector's `board_show` returned **Board access denied**. Direct-MCP creation/read-back and desktop inspection succeeded; use the standard frame links above for review.

## Proposal 03 — Trek Learning (Hub/LMS) monorepo

### Created and verified: 2026-11-16

- User confirmed the product grouping and authorized proceeding with the diagrams. Hub/LMS is the Trek Learning product group; TrekCAP/TrekFinder is separate Proposal 04.
- Created three native editable frames below the user's current Proposal 02 row. Checked the placement area was empty before creation; did not move or edit existing frames.
- [03A: Overview, scope and tradeoffs](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690578070331): saved application repository groups, illustrative product-repo folders, benefits, constraints, separate-repository/shared-standards alternative, and scope accounting.
- [03B: Developer and release workflow](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690578070332): propose change → identify affected services → test/review → merge/build images → propose GitOps deployment → deploy/verify. Failed tests/review and failed deployment/acceptance paths are explicit.
- [03C: Delivery plan](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690578070333): confirm product code/scope → agree developer experience and controls → small development pilot → staged migration. Proposed owners, acceptance evidence, reference updates, cutover/recovery and team decisions are included.

### Scope and evidence

- [Trek Learning product map](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-product-map/01-trek-learning.md), saved 2026-11-03.
- [Repository and delivery matrix](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-questions/cross-system/2026-11-10-trek-learning-repositories-and-delivery.md), answered Nov 10 from Nov 3 GitHub / Nov 4 Terraform snapshots, incorporating the Nov 6 static GitOps assessment. Used its detailed qualifications over broader historical wording in the generated product map.
- The reported **16 repositories** are a product-group inventory, not 16 application repositories to merge unconditionally. Accounting: **11 application repositories + 3 adjacent candidates + 2 DevOps repositories**.
- The 11 application examples are `tl-lms-ui`, `tl-lms-service`, `tl-auth-service`, `tl-ai-service`, `tl-chat-service`, `tl-lms-agent`, `tl-grading-service`, `tl-rag-ingestion-service`, `tl-rag-retrieval-service`, `tl-file-handling-service`, `tl-batch-job-service`.
- Adjacent candidates to discuss with application developers: `tl-lms-db`, `tl-oss-components`, `tl-file-ingestion-pipeline`. Their inclusion, owners and operating paths need agreement; absence of Actions for DB/ingestion does not rule out external automation.
- `tl-lms-gitOps` and `tl-trekai-terraform` need a coordinated home decision with Proposal 02. The proposed product repository does not silently absorb DevOps scope. Trek Adventure and TrekCAP/TrekFinder are outside the drawn application scope.
- Current delivery is shown as dated configured behavior: service image builds → GitOps proposals → Argo CD; application develop/staging/main paths rebuild per environment. Current successful execution, effective gates and exact deployed identity remain unverified. Application branch mappings do not define Terraform targets.
- Proposed improvements preserve independently identifiable service images and release boundaries; shared commits do not require all services to deploy together. Shared code/configuration changes need consumer-aware checks, contracts/schema checks and selected QA user-journey evidence.
- Branch/version strategy and release-policy changes are team decisions coordinated with Proposal 11. No new tooling, version scheme, dates or named owners are committed.

### Verification and artifacts

- Creation succeeded: **75 items, zero failed or skipped**, including 3 frames and 10 attached connectors.
- Scoped live read-back returned all **75 managed items**, zero foreign items, and all 10 Proposal 03 connectors. Its 43 excluded connectors belong to earlier content outside this selection.
- Inspected measured text bounds; text remained within allocated space with clear margins. Visually checked all three frames in Miro desktop: labels fit, comparisons and bullet panels are readable, and progression/failure connectors attach without crossing nodes.
- Saved [canonical live source](proposals/03/proposal-03.miro.svg), [verified read-back](proposals/03/proposal-03.verified.svg), [creation response](proposals/03/proposal-03.created.json), [initial creation source](proposals/03/proposal-03.canvas.svg), and [builder](proposals/03/build_source.py).
- Use live Miro IDs for edits; do not recreate the source on this board. No repositories, workflows, access permissions or cloud environments were changed.
- Next: user review of Proposal 03. Proposal 04 remains not started.
- Preview delivery: the separate Miro app connector returned **Board access denied**. Direct-MCP creation/read-back and desktop visual verification succeeded; use the standard 03A–03C links above.

## Proposal 04 — TrekCAP and TrekFinder repository consolidation

### Created and verified: 2026-11-16

- User authorized proceeding to Proposal 04. Created three native editable frames in an empty area below Proposal 03; existing frames were not moved or edited.
- [04A: Overview, scope and tradeoffs](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690579560265): 17-repository inventory, application/engine/CI/DevOps categories, compatible-access product monorepo option, retained restricted sources and policy ownership, artifact handoff, benefits, constraints and separate-repository alternative.
- [04B: Controlled builds and RD delivery](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690579560266): restricted review/build/artifact supply; permitted product changes consuming pinned artifacts; proposed release tests; GitOps/RD deployment and verification; failed-test stop.
- [04C: Delivery plan](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690579560267): map source/access → agree boundaries → permitted pilot → phased migration, with role-level owners, evidence, reference updates, cutover/recovery and team decisions.

### Evidence and scope decisions

- [Product map](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-product-map/03-trekcap.md) and [repository count clarification](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-questions/github/2026-11-03-which-repos-to-run-trekcap-trekfinder-locally.md#update-2026-11-12-platform-repository-count): **17** repositories in the Nov 3 inventory, clarified Nov 12. Categories: 2 UI/backend + 9 engine/module/supporting services + 4 CI/tests + 2 deployment/infra. The older 18-row related list includes unrelated legacy `c-trekai-adventure`; it is excluded from this product group.
- [CAP delivery explanation](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-how-it-works/path-to-production/03-trekcap.md), snapshots Nov 2–3, and [Nov 6 control assessment](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/reviews/gitops/reports/controls.md) qualify runtime and effective-gate claims. Saved configuration identifies RD; no stage/prod path is established. Tier 2 dispatch is post-GitOps-merge; current success and blocking policy are unverified.
- [Restricted orchestration source report](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/reviews/github/reports/repos/C-IP-ORCH.md) describes the open shell and kernel meeting through image layers. [CI policy report](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/reviews/github/reports/repos/C-CI-GATES.md) records sensitive classification-policy ownership. Only repository/policy metadata was used; no sensitive keyword lists or restricted implementation were copied into diagrams.
- All 17 repos are private in the snapshot. Open/sealed/employee-only classes do not by themselves establish current grants. Actual permitted readers, source owners, workflow consumers and registry access require confirmation before consolidation.
- Proposed direction is consolidation inside compatible source-access boundaries, retaining separately controlled kernel/employee-only source and trusted CI policy. A single broadly readable monorepo would expose all included source to its readers; folder review rules do not preserve separate visibility. Final group boundaries and migration count remain decisions.
- UI/backend do not universally require a sealed base image; the workflow shows pinned-artifact consumption where applicable to the affected service/module. The team must confirm build readiness, current core-engine path and exact consumers.
- Pre-GitOps integration/E2E gates and complete source/artifact/deployment traceability are proposals. Do not describe them as already enforced, or promise that static IP checks prove absence of all IP leakage.
- Coordinate GitOps/infra home decisions with Proposal 02. Hub/LMS remains Proposal 03; stage/prod and wider release-policy design require agreement with Proposal 11.

### Verification and saved artifacts

- Creation succeeded: **72 items, zero failed or skipped**: 3 frames, 30 shapes, 28 text items and 11 attached connectors.
- Visual QA caught a failed-test connector crossing a build node. Updated that connector in place and refined the facing sides so the failure path runs below the test row; no items were created or deleted during routing fixes.
- Visually verified all three frames in Miro desktop: labels and panels fit, artifact handoffs and progression arrows attach, and the final failure path stays clear of node content.
- Final scoped read-back returned **72 managed items, zero foreign items**, including all 11 Proposal 04 connectors. The 53 excluded connectors belong to earlier content outside this read.
- Saved [canonical live source](proposals/04/proposal-04.miro.svg), [verified read-back](proposals/04/proposal-04.verified.svg), [creation response](proposals/04/proposal-04.created.json), [current fresh-board source](proposals/04/proposal-04.canvas.svg), [builder](proposals/04/build_source.py) and routing responses in the same folder. Rebuilt the fresh-board source to include final routing.
- Use live IDs for later edits; do not recreate this composition on the existing board. No repositories, permissions, workflows, images or cloud resources were changed.
- Next: user review of Proposal 04. Proposal 05 remains not started.
- Preview delivery: the separate Miro app connector returned **Board access denied**. Direct-MCP creation/read-back and desktop visual verification succeeded; use the standard 04A–04C links above.

## Proposal 05 — QA environments and lab

**Current scope:** QA, Sales Demo and Client Pilot Environments. The initial creation record below is historical; the Nov 16 scope revision at the end supersedes its QA-only profile and cleanup descriptions.

### Created and verified: 2026-11-16

- User authorized proceeding with Proposal 05. Created three editable native frames below Proposal 04 after checking the placement area was empty. Existing board content was not moved or edited.
- [05A: Overview, manifest and lab profiles](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690584503904): saved environment context; QA selects a manifest/profile; illustrative functional, load/resilience and rapid-POC instances; isolation options, expected outcomes, proposed manifest fields and lifecycle controls.
- [05B: Request, provision, test and clean up](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690584503905): role-based request → validation/approval → final plan → infrastructure apply/verification → separate release deployment/data setup → readiness → QA tests → evidence → cleanup. Includes incomplete/unauthorized requests, failed/partial provisioning, unready instances and cleanup follow-up.
- [05C: Delivery plan and operating controls](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690584503906): agree scenarios/code coverage → design the lab contract → pilot recreation, test and cleanup → expand agreed profiles, with role ownership, dependencies, controls and open decisions.

### Evidence and design choices

- Proposal intent comes from [bulletpoints.md](bulletpoints.md) and the Nov 12 [meeting](meeting-2026-11-12-090251.md): identify testing targets via a release manifest, enable QA to provision from code, and support different or multiple environments including rapid POCs.
- Used the existing [environment explanation](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-how-it-works/architecture/environments.md), [Terraform environment scope](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-how-it-works/architecture/tl-terraform-environments.md) and saved delivery explanations as dated context. Nov 2–3 snapshots describe running shared Trek Learning dev/stage/prod and CAP RD environments; an on-demand lab workflow is not established in the reviewed scope. No current runtime refresh was performed.
- Manifest fields and the three lab illustrations are proposed, not an existing schema or an approved quantity. Record artifact/template versions, dependencies/settings, schema/data profile, owner/purpose, sizing/expiry and acceptance checks; use secret references rather than values.
- Show QA initiating an approved-code workflow while keeping the interface and authorization mechanism open. Workflow/button versus direct CLI, actual identity, state boundaries and approval policy require team agreement. Proposal 01 execution controls are linked inside the final-plan box and overview.
- Separate Terraform infrastructure provisioning from application deployment and schema/data setup. Verify readiness before handing a lab to QA. Record failures as well as passes and distinguish product defects from environment failures.
- Compare logical isolation in shared infrastructure with dedicated project/cluster/data services. Choose based on security, load/fault testing and dependencies; the proposal does not assume a namespace meets every need or a full cluster is needed for every test.
- Completion or expiry follows an agreed lifecycle policy, with approved extensions and evidence retention. Remove/stop lab deployment desired state before resource cleanup; scope cleanup to owned resources, exclude shared/protected dependencies and verify residual resources/cost. Failed/partial provisioning does not imply automatic rollback.
- Propose synthetic or explicitly approved sanitized test data, bounded resource profiles/quotas/concurrency/duration, scoped execution and clear failure owners. No numeric limits, dates, lab quantity or named owners are committed.
- Pilot evidence covers reproducible configuration/artifact versions, readiness and QA journeys, overlapping requests, partial operations, removal/recreation and cleanup residue. Infrastructure-code exercise alone does not prove production disaster recovery.
- Consume approved artifacts from 03/04 and coordinate release policy with 11; repository consolidation is not a prerequisite. Production promotion and implementation approval remain separate decisions.

### Verification and saved artifacts

- Creation succeeded: **88 items, zero failed or skipped**: 3 frames, 39 shapes, 32 text items and 14 attached connectors.
- Checked measured text bounds: all remained inside their allocations with clear margins. Visually inspected all three frames in Miro desktop; labels fit, role lanes and exception branches are readable, and connectors remain clear of node content.
- Final scoped read-back returned **88 managed items, zero foreign items**, including all 14 Proposal 05 connectors. The 64 excluded connectors belong to earlier content outside the selected frames.
- Saved [canonical live source](proposals/05/proposal-05.miro.svg), [verified read-back](proposals/05/proposal-05.verified.svg), [creation response](proposals/05/proposal-05.created.json), [initial creation source](proposals/05/proposal-05.canvas.svg) and [builder](proposals/05/build_source.py).
- Use live IDs for later edits; do not recreate the initial source on the existing board. No Terraform commands, app deployments, test-data operations, access changes or cleanup actions were executed.
- Next: user review of Proposal 05. Proposal 06 remains not started.
- Preview delivery: the separate Miro app connector returned **Board access denied**. Direct-MCP creation/read-back and desktop visual verification succeeded; use the standard 05A–05C links above.

### Scope revision: QA, sales demo and client pilot — 2026-11-16

- User clarified and authorized separate internal QA, sales demo/POC and production-like client pilot purposes. Customer-facing workflows must function end to end, and pilots must accommodate multiple students. Updated all three existing frames in place, preserving their positions and identities.
- [05A: Purpose and environment requirements](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690584503904) now contrasts disruptive/resettable QA, rehearsed stable sales demonstrations and persistent supported client pilots. Templates are reusable; configuration, access, data, capacity and lifecycle are separate. Three purposes do not imply exactly three instances.
- [05B: Provision, accept, operate and retire](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690584503905) includes QA/sales/pilot request ownership, infrastructure versus application handoffs, readiness, purpose-specific acceptance, a failed-acceptance hold, owner sign-off, use/support evidence and separate reset/retirement rules. Active pilots are excluded from automatic QA cleanup; retirement includes approved retention/export and verification of owned-resource removal.
- [05C: Delivery and operating controls](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690584503906) covers complete workflows/accounts/integrations, agreed student concurrency and response/error thresholds, persistence, monitoring/support, backup/restore, isolation from QA disruption, controlled changes and business/technical ownership. Capacity, dates, service targets and named owners remain decisions. “Fully functioning” is expressed as measurable acceptance requirements.
- Miro update succeeded: **56 updated, 2 created, zero deleted, failed or skipped**. Added one native failed-acceptance card and its attached connector. Scoped read-back returned **90 managed items, zero foreign items**: 3 frames, 40 shapes, 32 text items and 15 connectors. All original 88 identities were preserved; 64 out-of-scope connectors belong to earlier content.
- Compared all 53 changed content bodies with read-back; checked frame bounds and connector references. Visually verified all three revised frames in Miro desktop: labels fit, panels remain separated and connector routes are readable.
- Saved the [pre-revision snapshot](proposals/05/proposal-05.before-sales-pilot.svg), [applied patch](proposals/05/proposal-05.sales-pilot.patch.svg), [update response](proposals/05/proposal-05.sales-pilot.updated.json) and [read-back](proposals/05/proposal-05.sales-pilot.readback.svg). Refreshed canonical/verified SVGs, the fresh-board export and its builder. Original creation builder/export are archived with `.before-sales-pilot` suffixes. Do not replay the revision patch; it includes two additions without live IDs.
- Updated the design plan and tracker. No infrastructure, application deployments, account/data operations or cleanup commands were executed. Next: review revised Proposal 05; Proposal 06 remains not started.
- Revision preview: the separate Miro app connector again returned **Board access denied**; direct-MCP update/read-back and desktop verification succeeded. Use the standard frame links above.

## Proposal 06 — Documentation and knowledge base

### Created and verified: 2026-11-16

- User authorized proceeding with the three documentation diagrams. Created native editable frames below Proposal 05 after a scoped read confirmed the placement area was empty. Existing board items were not moved or edited.
- [06A: Knowledge map](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690590495740): reported fragmentation/freshness concerns, a proposed knowledge index and authoritative sources, DevOps/cloud/product content areas, page minimum, outcomes and open decisions. Includes a temporary QA setup guide example linked to 05B and 01B.
- [06B: Change, review, publish and maintain](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690590495741): change/reader gap → owner assignment → draft → domain review/validation → publish/index → discover/use → feedback → refresh/reaffirm/retire. Includes unresolved ownership/conflicting sources, failed review and missing/stale/inaccessible pages. Change impact checks and periodic reviews return work to the owner.
- [06C: Delivery and ownership](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690590495742): inventory/prioritize → agree structure and responsibilities → prove one DevOps guide → expand to cloud/product knowledge and maintain it. Includes proposed roles, validation evidence, inputs, operating rules and team decisions.

### Evidence and design choices

- Based on [proposal notes](bulletpoints.md), the [Nov 12 discussion](meeting-2026-11-12-090251.md) at 04:45 and the presentation-first direction at 12:58. Incomplete/fragmented documentation and outdated Confluence/product pages are reported concerns, not a new audit finding.
- The entry point links to an authoritative page or repository per topic; it does not assume all content moves to one tool. Show owner, status, scope, verification date and implementation version. Link maintained explanations to code/configuration and dated evidence.
- Start with DevOps and an agreed operational task such as temporary QA provisioning. Include manifest/launch/readiness/testing/expiry/cleanup instructions and failure ownership. Actual instructions must describe the agreed implementation/version.
- Tie documentation impact checks to infrastructure, application, access and environment changes. Track updates with the change/release and agree required handoff timing, review cadence, overdue escalation and ownership transfer. Reminders/automation are options, not existing verified services.
- Acceptance includes another reader locating and completing an agreed task, clear version/scope/date, a sample change causing the right update, and feedback/stale/retired guidance reaching an owner. Obsolete pages get retirement/replacement links.
- Tool choice, actual content inventory, named owners/reviewers, priorities, cadence and publishing authority remain open. Detailed Confluence/runbook delivery follows review. No tool migration, AI ingestion, live publishing or access changes were performed.

### Verification and saved artifacts

- Creation succeeded: **89 items, zero failed or skipped**: 3 frames, 40 shapes, 32 text items and 14 attached connectors. Refined two workflow role labels in place; **2 updated, zero created/deleted/failed/skipped** in that follow-up.
- Compared 81 content bodies with scoped read-back; verified the two revised labels after their update. Checked measured text bounds, frame containment and connector references. Final scoped read-back returned **89 managed items, zero foreign items**; 79 excluded connectors belong to earlier content outside these frames.
- Visually verified all three frames in Miro desktop, including updated role labels. Text fits, panels remain separated, and workflow/exception routes are readable.
- Saved [creation source](proposals/06/proposal-06.canvas.svg), [builder](proposals/06/build_source.py), [creation response](proposals/06/proposal-06.created.json), [label update response](proposals/06/proposal-06.labels.updated.json), [canonical live source](proposals/06/proposal-06.miro.svg) and [verified read-back](proposals/06/proposal-06.verified.svg). Use live identities for edits; do not recreate this source on the existing board.
- Updated the design plan and tracker. Next: review Proposal 06; Proposal 07, Observability and Alerting, remains not started.
- Preview delivery: the separate Miro app connector returned **Board access denied**. Direct-MCP creation/update/read-back and desktop visual verification succeeded; use the standard 06A–06C links above.

## Proposal 07 — Observability and alerting

### Created and verified: 2026-11-16

- User authorized proceeding with Proposal 07 and reiterated continuation after an interruption. The initial interrupted turn performed only read-only checks; resumed work confirmed the new placement area was empty before creating three native editable frames below Proposal 06. No previous proposal content was changed.
- [07A: Signals to response](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690608642585): reported current concerns versus workload/dependencies → relevant telemetry → ingest/store/query → rule evaluation → useful notification → accountable response/recovery. Includes direct developer/QA investigation, expected outcomes, coverage, team decisions and environment-purpose policies linked to 05B and 06B.
- [07B: Detect, notify, respond and verify recovery](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690608642586): emit → collect/check → evaluate → notify → acknowledge/assign incident ownership → investigate → mitigate → verify recovery → close/improve. Includes missing/stale telemetry, failed delivery, acknowledgement timeout/escalation and failed mitigation. Unconfirmed recovery returns to investigation while retaining incident ownership.
- [07C: Delivery and controls](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690608642587): verify existing setup → agree alerts/response coverage → configure a focused first scope → exercise/tune/expand. Shows proposed roles, acceptance evidence, dependencies, operating rules and open decisions.

### Evidence and design choices

- Based on [proposal notes](bulletpoints.md) and the [Nov 12 discussion](meeting-2026-11-12-090251.md) at 05:56–06:42, including the explicit request to enable alerting. Deployed tools and questioned effectiveness/alert visibility are reported concerns; no new runtime/configuration audit was performed.
- Keep actual tool names, signal coverage, thresholds/windows, severity, destinations, recipients, response hours and escalation timings open until verified/agreed. This proposal validates and extends the existing setup before choosing replacements.
- Relevant coverage includes critical journeys/dependencies, availability, errors, latency, capacity, collection freshness and notification-path health. Developers and QA can query signals directly and correlate evidence with product/environment/release/manifest/instance context.
- Temporary QA test windows, expiry and cleanup need purpose-specific rules. Stable sales demos, client pilots and production need agreed monitoring/support coverage. Test/maintenance silences have an explicit scope and end; missing telemetry follows an agreed no-data policy.
- Notifications include scope, symptom/impact, severity, evidence and runbook links. Assign primary/backup coverage, acknowledgement, escalation and incident ownership. Actual receipt, response and fresh service/journey recovery evidence are distinct from a configured rule or a sent event.
- Mitigation uses existing change/access controls. Retain incident evidence and unresolved follow-up; tune noise/coverage, maintain runbooks through 06 and repeat validation when rules/routes/owners change. Agree access, minimization/redaction, retention and collection cost.
- Acceptance exercises controlled impact, real notification receipt and acknowledgement, failed delivery, escalation, recovery, missing data, duplicates, silence expiry and temporary QA lifecycle. No live alerts, messages, incidents, mitigations or infrastructure changes were executed. Numeric targets, 24/7 coverage, dates and named assignments remain decisions.

### Verification and saved artifacts

- Creation succeeded: **96 items, zero failed or skipped**: 3 frames, 42 shapes, 31 text items and 20 attached connectors.
- Compared **88 content bodies** with read-back; checked measured text/frame bounds, unique IDs and connector references. Final scoped read-back returned **96 managed items, zero foreign items**; 93 excluded connectors belong to earlier content outside these frames. Board count matched the prior 562 items plus these 96 additions.
- Visually verified all three frames in Miro desktop after bringing its rendering up to date. Text fits, panels remain separated and the overview/response routes avoid node content, including the two routed handoffs between detection, acknowledgement, investigation and mitigation.
- Saved [creation source](proposals/07/proposal-07.canvas.svg), [builder](proposals/07/build_source.py), [creation response](proposals/07/proposal-07.created.json), [canonical live source](proposals/07/proposal-07.miro.svg) and [verified read-back](proposals/07/proposal-07.verified.svg). Use live identities for later edits; do not recreate this composition on the existing board.
- Updated the design plan and tracker. Next: review Proposal 07; Proposal 08, Entra ID for Google Cloud, remains not started.
- Preview delivery: the separate Miro app connector returned **Board access denied**. Direct-MCP creation/read-back and desktop visual verification succeeded; use the standard 07A–07C links above.

## Proposal 08 — Entra ID for Google Cloud

### Created and verified: 2026-11-16

- User authorized proceeding with Proposal 08. Created three native editable frames below Proposal 07 after confirming the placement area was empty. Earlier proposal content was not changed.
- [08A: Sign-in and access model](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690610675776): separate Entra/Google Cloud boundaries, solid identity-trust/evaluation arrows and a dashed group/attribute-to-role mapping. Covers permission review/change, meaningful group naming, mapping ownership, integration alternatives and the separate baseline/elevation boundary.
- [08B: Staff access and lifecycle](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690610675777): staff task/scope → approved membership → Entra authentication → accepted cloud identity → scoped IAM evaluation → allowed task → evidence → access maintenance. Includes blocked sign-in, identity/mapping mismatch, denied/additional-access requests and unexpected allow/deny behavior.
- [08C: Delivery and validation](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690610675778): inventory identities/effective permissions → design roles/naming/mappings/integration → representative pilot → controlled cohort migration and maintenance. Includes roles, acceptance, dependencies, lifecycle/recovery controls and open decisions.

### Evidence and design choices

- Based on [proposal notes](bulletpoints.md) and the [Nov 12 discussion](meeting-2026-11-12-090251.md), 06:54–10:37. Explicitly include planning, reviewing and changing Google Cloud permissions, understandable group/role names, team-based baseline access and the handoff to PAM design. No current tenant/grant audit was performed.
- Checked official Google references on Nov 16: [Workforce Identity Federation](https://docs.cloud.google.com/iam/docs/workforce-identity-federation), [Entra SSO/provisioning with Cloud Identity or Workspace](https://docs.cloud.google.com/architecture/identity/federating-gcp-with-azure-ad-configuring-provisioning-and-single-sign-on) and [IAM overview](https://docs.cloud.google.com/iam/docs/overview). Linked these references inside the diagrams. Integration choice remains open; verify required services, console/CLI, group/identity handling and lifecycle before selecting it.
- Authentication establishes staff identity; Google IAM evaluates resource actions. Review group/direct/inherited access and applicable policy. Define baseline tasks, roles and scope rather than treating sign-in as an access grant or assuming every role receives the same read/write permissions.
- Group naming includes team/product/environment/purpose; `qa-learning-nonprod-observe` is an explicitly illustrative label. Record stable identifiers, target roles/scopes and accountable owners. Approve membership/permission changes through an agreed process.
- Test intended allowed actions and out-of-scope denials, multiple memberships, remaining direct grants, joiner/mover/leaver changes, removal propagation and active-session behavior. Include audit evidence, support and administrative recovery. Do not assume instant revocation.
- Scope is staff Google Cloud access; track service-account/CI/workload identities separately. Proposal 09 covers GitHub; 10 defines temporary elevation for agreed targets, including eligibility, approval, scope and expiry. No strict final migration sequence or universal PAM mechanism is asserted. Maintain the access catalog/user guidance through 06B.
- Tool choice, tenant configuration, required clients/services, baseline roles, membership/cutover approvals, ownership and lifecycle/support remain decisions. No identities, memberships, IAM permissions, authentication settings or live access paths were changed.

### Verification and saved artifacts

- Creation succeeded: **97 items, zero failed or skipped**: 3 frames, 41 shapes, 35 text items and 18 attached connectors.
- Compared **87 content bodies** with read-back; checked measured text/frame bounds, unique IDs and connector references. Final scoped read-back returned **97 managed items, zero foreign items**; 113 excluded connectors belong to earlier content outside these frames.
- Visually verified all three frames in Miro desktop. Labels fit, boundaries and arrow meanings are clear, and workflow/exception routes avoid node content.
- Saved [creation source](proposals/08/proposal-08.canvas.svg), [builder](proposals/08/build_source.py), [creation response](proposals/08/proposal-08.created.json), [canonical live source](proposals/08/proposal-08.miro.svg) and [verified read-back](proposals/08/proposal-08.verified.svg). Use live identities for edits; do not recreate this composition on the existing board.
- Updated the design plan and tracker. Next: review Proposal 08; Proposal 09, Entra ID for GitHub, remains not started.
- Preview delivery: the separate Miro app connector returned **Board access denied**. Direct-MCP creation/read-back and desktop visual verification succeeded; use the standard 08A–08C links above.

## Proposal 09 — Entra ID for GitHub

### Created and verified: 2026-11-16

- User authorized proceeding with Proposal 09. Created three native editable frames below Proposal 08 after confirming the placement area was empty. Earlier proposal content was not changed.
- [09A: Sign-in, teams and repository access](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690640001435): separate Entra/GitHub boundaries, solid identity/access arrows and dashed group-to-team membership mapping. Includes repository roles, base/direct/team access review, meaningful names, integration choices and restricted-source boundaries linked to 04A.
- [09B: Staff access and membership lifecycle](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690640001436): scoped task → approved organization/group membership → identity/SSO checks → model-supported membership/mapping → repository authorization → task → evidence → lifecycle maintenance. Includes blocked identity checks, incomplete membership/mapping, denied/additional access and unexpected repository visibility/actions.
- [09C: Delivery and access validation](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690640001437): inventory → identity/team/role design → representative pilot → controlled cohort migration and maintenance. Includes proposed roles, acceptance, inputs, membership/repository controls and open decisions.

### Evidence and design choices

- Based on [proposal notes](bulletpoints.md) and the [Nov 12 discussion](meeting-2026-11-12-090251.md), 06:54–10:37: Entra for GitHub, clearer teams/group mappings, meaningful naming and job-based default access. Current hosting/plan, account type, memberships and effective grants remain to inventory.
- Checked and linked official [GitHub SAML/account-model guidance](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/understanding-iam-for-enterprises/about-saml-for-enterprise-iam), [team synchronization guidance](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-saml-single-sign-on-for-your-organization/managing-team-synchronization-for-your-organization) and [repository roles](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization) on Nov 16. Keep personal-account SAML SSO versus Enterprise Managed Users and the supported provisioning/team mechanism open for evaluation.
- Separate GitHub account/SSO checks, organization membership, group/team mapping and repository authorization. Review organization base access, team-derived/inherited access, direct/collaborator grants and branch/review constraints. Source visibility remains consistent with 04A and compatible repository boundaries from 02–04.
- Names communicate team/product and purpose; `dev-learning-source-write` is explicitly illustrative. Record stable Entra group IDs, GitHub organization/team identity, owners, repositories and roles. Membership/permission changes follow an agreed approval path.
- Test representative web/Git/CLI/API journeys, required actions, restricted repository/action denials and multiple access paths. Reconcile joiner/mover/leaver events and verify synchronization, session/removal and relevant human-credential behavior. Inventory GitHub Apps, deploy keys and workflow identities separately.
- Verify access before retiring replaced grants/paths; include audit, support and administrative recovery. Maintain the access catalog through 06B. Proposal 10 must define any supported GitHub temporary-elevation mechanism; no Google Cloud PAM-to-GitHub integration is assumed.
- Account model, feature/license compatibility, integration scope, roles, owners, approvals and lifecycle/support remain decisions. No SSO settings, identities, organization/team memberships, repository permissions or live credentials were changed.

### Verification and saved artifacts

- Creation succeeded: **97 items, zero failed or skipped**: 3 frames, 41 shapes, 35 text items and 18 attached connectors.
- Compared **87 content bodies** with read-back; checked measured text/frame bounds, unique IDs and connector references. Final scoped read-back returned **97 managed items, zero foreign items**; 131 excluded connectors belong to earlier content outside these frames.
- Visually verified all three frames in Miro desktop. Labels fit, boundaries and arrow meanings are clear, and workflow/exception routes avoid node content.
- Saved [creation source](proposals/09/proposal-09.canvas.svg), [builder](proposals/09/build_source.py), [creation response](proposals/09/proposal-09.created.json), [canonical live source](proposals/09/proposal-09.miro.svg) and [verified read-back](proposals/09/proposal-09.verified.svg). Use live identities for edits; do not recreate this composition on the existing board.
- Updated the design plan and tracker. Next: review Proposal 09; Proposal 10, Role-based Default Access and PAM, remains not started.
- Preview delivery: the separate Miro app connector returned **Board access denied**. Direct-MCP creation/read-back and desktop visual verification succeeded; use the standard 09A–09C links above.

## Proposal 10 — Role-based default access and PAM

### Created and verified: 2026-11-16

- User authorized proceeding with Proposal 10. Created three native editable frames below Proposal 09 after confirming the placement area was empty. Earlier proposal content was not changed.
- [10A: Baseline plus temporary elevation](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690641387257): team/job → approved membership/mapping → baseline; separate entitlement → eligible request/policy → temporary grant → ending/removal verification. Defines entitlement versus grant, catalog fields, expected outcomes, decisions and separate target mechanisms linked to 08A/09A.
- [10B: Request, authorize, use and verify removal](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690641387258): need → eligibility/scope → configured authorization → grant → target activation → effective-access check → task → expiry/supported early ending → removal check/evidence. Includes ineligible/declined/expired requests, failed/partial activation, scope mismatch, task failure/overrun and access remaining after expected end.
- [10C: Delivery and validation](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690641387259): agree normal/elevated tasks → target-specific catalog/policies → limited entitlement pilot → controlled expansion and standing-access review. Includes proposed owners, acceptance, dependencies, operating controls and open decisions.

### Evidence and design choices

- Based on [proposal notes](bulletpoints.md) and the [Nov 12 discussion](meeting-2026-11-12-090251.md), 07:43–10:37. Default access follows the agreed team/job model; extra privilege is temporary and scoped. The read/write discussion is an example rather than a blanket rule for all teams. Current entitlements, standing grants and elevation tools remain to inventory.
- Checked and linked official [Google Cloud PAM overview](https://docs.cloud.google.com/iam/docs/pam-overview), [grant lifecycle guidance](https://docs.cloud.google.com/iam/docs/pam-request-temporary-elevated-access) and [Entra PIM for Groups](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/concept-pim-for-groups) on Nov 16. Google Cloud PAM is the cloud-specific implementation to evaluate. Entra PIM for Groups is a candidate for a separately validated downstream group-based path; it is not presented as a proven GitHub integration.
- An entitlement defines requestable target access and its policy; a grant is one time-bound activation. Catalog fields include meaningful purpose/name, target platform/scope, roles, eligible identities/groups, approval/justification rules, maximum duration, owner, audit and ending/verification requirements.
- Approval behavior is configured per entitlement: no invented fixed stages, mandatory universal approval, durations or named approvers. A pending/declined/ineligible request adds no privilege. Verify actual target permissions before privileged use and follow normal change/execution controls during the task.
- Test expiry and supported revocation/early ending, including propagation/session behavior. Baseline remains only while separately authorized. If elevated actions still work, reconcile bindings/membership/sessions/other grants, keep exception follow-up open and repeat the denial check. New access windows require new requests rather than assumed extension.
- Prove before/during/after permissions, rejection/pending behavior, target scope, audit completeness and failed-removal escalation. Expand only after validation and review replaced standing privilege. Coordinate identity decisions with 08/09, execution controls with 01 and runbooks/audit response with 06/07; the final migration sequence remains open.
- Targets, exact roles, entitlement mechanisms, eligibility, policy, duration, emergency access and owners remain decisions. No live entitlements, grants, permissions, memberships or authentication settings were changed.

### Verification and saved artifacts

- Creation succeeded: **98 items, zero failed or skipped**: 3 frames, 42 shapes, 31 text items and 22 attached connectors.
- Compared **90 content bodies** with read-back; checked measured text/frame bounds, unique IDs and connector references. Final scoped read-back returned **98 managed items, zero foreign items**; 149 excluded connectors belong to earlier content outside these frames.
- Visually verified all three frames in Miro desktop. Text fits, baseline/elevation paths are distinct and workflow/exception routes avoid node content, including the removal-mismatch branch.
- Saved [creation source](proposals/10/proposal-10.canvas.svg), [builder](proposals/10/build_source.py), [creation response](proposals/10/proposal-10.created.json), [canonical live source](proposals/10/proposal-10.miro.svg) and [verified read-back](proposals/10/proposal-10.verified.svg). Use live identities for edits; do not recreate this composition on the existing board.
- Updated the design plan and tracker. Next: review Proposal 10; Proposal 11, GitOps / SDLC, remains not started.
- Preview delivery: the separate Miro app connector returned **Board access denied**. Direct-MCP creation/read-back and desktop visual verification succeeded; use the standard 10A–10C links above.

## Proposal 11 — GitOps and SDLC

### Created and verified: 2026-11-16

- User authorized proceeding with Proposal 11. Created three native editable frames below Proposal 10 after confirming the placement area was empty. Earlier proposal content was not changed.
- [11A: Shared desired state and promotion](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690643240926): reported delivery gaps, shared GitOps contract, dev → staging → production using the same accepted artifacts, target reconciliation, expected outcomes, decisions and the separate infrastructure/application/acceptance handoffs.
- [11B: Code change to verified environment promotion](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690643240927): source PR → checks/review → merge/build/publish candidate → target desired-state PR → target authorization → merge reviewed revision → pull/reconcile → verify → record acceptance/promotion decision → operate/recover. Includes source-review failure, candidate-publication failure and sync/readiness/acceptance failure.
- [11C: Delivery and validation](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764690643240928): inventory real delivery paths → agree release contract → prove one development release → extend staging/production after evidence. Includes proposed owners, acceptance, dependencies, operating controls and open decisions.

### Evidence and design choices

- Based on [proposal notes](bulletpoints.md) and the [Nov 12 discussion](meeting-2026-11-12-090251.md), 11:11 and 23:05. Centralizing GitOps and simplifying SDLC are the request; automated development versus manual staging/production handoffs are reported concerns, not a fresh pipeline audit.
- Checked and linked [OpenGitOps principles](https://opengitops.dev/) and their [v1.0 explanation](https://opengitops.dev/blog/1.0-announcement/) on Nov 16: versioned declarative desired state, pulled and continuously reconciled by agents. Current engine, authoritative state layout, branch/reference mapping and automation policy remain to verify/agree.
- Build immutable service artifacts and record exact versions in a candidate manifest. Promote the same accepted artifact set without rebuilding. Each target has its own reviewed configuration, dependencies, secret references, prerequisites, acceptance evidence and release authorization. A branch merge alone does not prove target health or authorize production promotion.
- Trace source commit, artifact manifest, GitOps revision, target environment and test/health outcomes. Developers, CI, release/service owners, QA and DevOps have proposed responsibilities; exact gate ownership and QA acceptance authority remain decisions.
- Failures hold the next promotion, retain diagnostics and return fixes/reverts through the appropriate review path. Report drift/failed reconciliation to an owner. Recovery includes dependency and data/schema compatibility; a Git revert alone does not restore database contents or prove disaster recovery.
- Infrastructure uses 01 controls; artifacts follow 03/04. Coordinate state/repository placement with 02 while preserving source-access boundaries; consolidation is not a prerequisite. QA/demo/pilot instances follow 05 manifest and lifecycle rules separately from normal promotion. Use 06/07 for runbooks/monitoring and 08–10 for access/execution identities.
- Engine, layout, target mapping, automated versus human gates, checks, migrations, recovery, retention and support remain decisions. No live pipelines, deployments, branch protections, resources or reconciliation settings were changed.

### Verification and saved artifacts

- Creation succeeded: **92 items, zero failed or skipped**: 3 frames, 40 shapes, 32 text items and 17 attached connectors.
- Compared **84 content bodies** with read-back; checked measured text/frame bounds, unique IDs and connector references. Final scoped read-back returned **92 managed items, zero foreign items**; 171 excluded connectors belong to earlier content outside these frames.
- Visually verified all three frames in Miro desktop. Text fits, panels remain separated and workflow/exception routes avoid node content, including the routed reconciliation-status handoff to target verification.
- Saved [creation source](proposals/11/proposal-11.canvas.svg), [builder](proposals/11/build_source.py), [creation response](proposals/11/proposal-11.created.json), [canonical live source](proposals/11/proposal-11.miro.svg) and [verified read-back](proposals/11/proposal-11.verified.svg). Use live identities for later edits; do not recreate this composition on the existing board.
- Updated the design plan and tracker. All eleven confirmed proposal diagram sets are created. Next: review Proposal 11 and consolidate team feedback/decisions across the full set. Supplementary AI-brain scope remains unconfirmed.
- Preview delivery: the separate Miro app connector returned **Board access denied**. Direct-MCP creation/read-back and desktop visual verification succeeded; use the standard 11A–11C links above.


### QA controlled self-service clarification — 2026-11-23

- User approved the model and explicitly requested matching updates in the presentation and Miro. Updated topic 02 in the combined HTML and its editable topic copy: QA requests approved options, DevOps owns templates/limits and initially approves each final plan, and scoped automation runs Terraform, deploys applications, reports URL/status and performs approved expiry cleanup. Added ownership and staged approval-policy slides.
- Updated existing 05A–05C Miro shapes in place: **12 updated, 0 created/deleted, 0 failed/skipped**. The request method is a Jira form or permitted workflow; QA needs no direct Terraform/cloud admin access. Later routine automation requires an agreed policy and a proven pilot. Exceptions retain review. Sales/demo/client pilot rules remain separate.
- Scoped Miro read-back: **90 managed items**. Compared all 12 changed content bodies exactly after normalizing line-break markup. Canonical/verified snapshots, fresh-board export and design plan synchronized. Sources: `proposals/05/proposal-05.self-service.patch.svg`, `.self-service.updated.json`, `.self-service.readback.svg`; prior live state preserved in `.before-self-service.svg`.
- This edits planning material only; no workflows, permissions, Terraform executions or infrastructure operations were performed.
- Visual QA completed for all changed HTML slides and Miro 05A–05C; text fits the existing shapes/canvas. HTML structure, script syntax, menu targets and preservation of other topics passed. Combined deck now has 86 slides.

## Security coverage and implementation — 2026-11-23

- User requested adding the researched security information and improvement plan to both Miro and the combined presentation.
- Added presentation topic **08 Security**, slides **87–98**. Current setup, open coverage gaps, responsibilities, proposed baseline, environment records, control rollout, acceptance, incident response, QA template checks, delivery and team decisions use the existing animated 16:9 style. Updated the Topics menu and editable `Presentation/08.html`; combined deck now has **98 slides**. Earlier topic slides remain unchanged. Prior combined file is preserved in `Presentation/archive/combined-before-security.html`.
- Created three native editable Miro frames on the existing board, in a checked empty area below Proposal 11:
  - [12A Current coverage and proposed baseline](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764691334212141)
  - [12B Rollout, verification and response](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764691334212142)
  - [12C Delivery plan and environment coverage](https://miro.com/app/board/uXjVEOGaQYU=/?moveToWidget=3458764691334212143)
- Creation succeeded: **67 items**, zero failed/skipped. Scoped read-back returned **67 managed items, zero foreign items**. All **56 content bodies** matched the authored source after markup/whitespace normalization. Rendered bounds remain inside the frames; workflow connectors attach to actual nodes. Existing content was not changed.
- Saved the builder, fresh-composition source, creation response, canonical live-ID snapshot and verified snapshot in `proposals/12/`. Use the live identities for subsequent edits; do not recreate the source on the existing board.
- Current-state sources are preserved in `proposals/12/research-notes.md`. Active CSPM reporting does not establish runtime coverage; open LMS GKE and Cloud Workstations tasks remain open; registry access source does not establish working scans. Partner engagement and operating ownership require confirmation. November 2 audit findings remain dated and require remediation-state checks.
- Validation passed: all eight menu links, unique slide IDs, 98-slide count, matching topic/master content, script syntax, offline assets, preserved earlier topic content, point reveals/reset and topic navigation. Checked rendered bounds for every new slide and visually inspected all new slides, the menu and the Miro frames. Shortened one baseline note to clear the footer. Browser screenshot capture stalled once; native BrowserOS/Miro visual inspection completed the review.
- These are planning updates only. No cloud resources, access, Falcon sensors, connectors, subscriptions or delivery workflows were changed.
