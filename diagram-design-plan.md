# Architecture diagram design plan

Based on the proposed plans/changes in [bulletpoints.md](bulletpoints.md) and the November 12, 2026 discussion in [the meeting transcript](meeting-2026-11-12-090251.md).

Use `bulletpoints.md` as the primary topic list and clarification of proposal intent. Use the transcript for presentation expectations, audience perspectives, and supporting discussion. These are proposals to put in front of the team; inclusion here does not mean the team has approved them or that the changes are already implemented.

## 1. Purpose and scope

Create a consistent set of Miro diagrams that helps reviewers understand each proposal, see how it affects their work, and discuss the decisions needed to move forward.

The meeting explicitly requested:

- Supporting architecture diagrams for each topic, showing current state, problems, future state, and the proposed approach (11:38).
- An overview explaining why each topic matters and where it fits (17:25).
- Views tailored to the CTO, application developers, QA, and DevOps (15:25–17:02).
- Workflow steps, expected outcomes, proposed architecture, and DevOps implementation work (17:33).
- A consistent look and feel, with enough clarity to support review and feedback.
- Presentation-level effort first; detailed Confluence documentation after John's review and approval (12:58).

The layouts, colors, symbols, and workflow conventions below are recommendations for fulfilling those requests. They were not prescribed in the meeting.

### Proposals to put in front of the team

Use this list as the board index and coverage checklist. Each row should have its own identifiable overview, even when related topics share workflow or delivery frames.

| ID | Proposed plan/change | What the diagram should communicate | Team discussion/decision |
|---|---|---|---|
| 01 | Terraform PR review and controlled execution | Build on existing dev-only GitHub Actions planning; preview before PR approval, review the final plan after merge, and control apply per target. Pilot development, then extend to staging and production. | Scope, required checks, PR reviewers, per-target apply policy, identities, and execution ownership. |
| 02 | DevOps monorepo | Terraform, GitOps, Ansible, and DevOps code move into one repository. | Pros, cons, scope, and ownership before proceeding. |
| 03 | Trek Learning (Hub/LMS) monorepo | Evaluate a product repository for the 11 identified application repositories plus agreed adjacent scope; the 16-repo inventory also includes DevOps code. | Pros and cons with application developers; scope, build/test/release boundaries and coordination with Proposal 02. |
| 04 | TrekCAP and TrekFinder repository consolidation | Evaluate consolidation within compatible source-access boundaries; the saved product group has 17 repos including restricted code, CI/tests and DevOps. | Pros/cons with application and IP owners; source visibility, artifact handoffs, final scope and release gates. |
| 05 | QA, sales demo and client pilot environments | Reuse approved code and release manifests for isolated QA, fully working customer demonstrations and production-like multi-student pilots. | Purpose-specific provisioning, acceptance, capacity, data, support and lifecycle. |
| 06 | Documentation / knowledge base | Streamline incomplete and fragmented knowledge around DevOps, cloud architecture, and TrekAI products. | Source of truth, owners, and maintenance process. |
| 07 | Observability and alerting | Improve use of deployed observability and enable alerts for the team. | Current gaps, useful alerts, routing, and response ownership. |
| 08 | Entra ID for Google Cloud | Use Entra as IdP, review and change Google Cloud permissions, and establish meaningful names. | Identity/group mappings, default roles, and permission changes. |
| 09 | Entra ID for GitHub | Use Entra as IdP, review team/group setup and mappings, and establish meaningful names. | Team structure, repository access, and mapping changes. |
| 10 | PAM and role-based access | Define default access from team/role structure and enable just-in-time, temporary elevated access through PAM. | Default access, eligible entitlements, request/approval rules, duration, and target systems. |
| 11 | GitOps / SDLC | Centralize GitOps and simplify current development/release actions. | Which actions change, where automation is added, and required handoffs. |
| 12 | Security coverage and implementation | Explain device and platform controls, known coverage gaps, CrowdStrike capabilities and MOXFIVE/At-Bay roles; propose a verified baseline by environment. | Required controls, accountable owners, partner duties, acceptance, exceptions and staged rollout. |

Proposal 12 was added at the user's request on 2026-11-23 following research in Confluence, GitHub, email, Jira and the 2nd Brain. Its current-state descriptions distinguish reported activity, configured source and verified runtime coverage. The three native Miro frames and presentation topic 08 follow the existing overview, workflow and delivery structure. Detailed source provenance is in `proposals/12/research-notes.md`; it does not appear on presentation slides.

The AI brain was mentioned in the transcript but is absent from the supplied proposal list. Keep it as a supplementary scope item, separate from the eleven proposals above, until its inclusion and content are clarified.

## 2. Organize the diagram set

Use one Miro scratchpad board initially, with a repeatable group of frames for each topic. Split topics into separate boards if navigation becomes difficult; both arrangements were acceptable in the meeting.

Start with a board index using the proposal IDs above, links to their frames, and a short status such as Draft or Ready for review. Add a one-sentence statement of what the team is being asked to consider for each proposal.

For each topic, build these three frames:

| Frame | Main question | Contents |
|---|---|---|
| A. Overview and proposed change | Why are we doing this, and what changes? | Purpose, current state, problems, proposed state, benefits, decisions needed. |
| B. People and workflow | How does this work for the people involved? | Swimlanes for relevant audiences, numbered steps, handoffs, approvals, outputs, and important failure paths. |
| C. DevOps delivery plan | What work makes the proposal real? | Work packages, dependencies, responsible roles, validation, and unresolved implementation decisions. |

For the first team discussion, complete Frame A for all eleven proposals, then develop Frame B where a workflow is central: Terraform, QA, access/PAM, and GitOps/SDLC. Keep Frame C at the work-package level; expand it after feedback. Related proposals may share Frames B and C when their boundaries remain clear.

Keep current and proposed architecture side by side in Frame A when they remain readable. Give them separate frames when either becomes crowded.

Do not create four copies of every diagram automatically. One workflow can serve application developers, QA, and DevOps through clearly separated swimlanes. Add a dedicated audience view when that audience's process needs more explanation.

Keep the same frame order for every topic so readers can navigate without relearning the board.

## 3. Standard frame design

Use a landscape, presentation-shaped frame. A practical starting size is 1600 × 900, with more space for workflow frames when necessary.

### Frame header

Every frame should include:

- **Topic and view:** for example, “QA lab — QA workflow.”
- **Audience:** CTO, application developers, QA, DevOps, or a combination.
- **State:** Current, Proposed, or Mixed comparison.
- **Status:** Draft / Under review / Approved, updated only when accurate.
- **Takeaway:** One sentence explaining the point of the diagram.
- **Proposal / decision needed:** The specific change being put forward and the feedback or decision requested from the team.

### Frame body

Use a predictable reading order:

1. Start at the top left with the actor, request, or trigger.
2. Follow the main flow from left to right.
3. Place exceptions and alternate paths below the main flow.
4. Place supporting systems below the components that use them.
5. Keep decisions and unanswered questions in a side panel.

For an overview frame, use this arrangement:

```text
Topic | Audience | State | Review status
One-sentence takeaway

CURRENT STATE                    PROPOSED STATE
Systems and relationships        Systems and relationships
Numbered problem markers         Matching change markers

Problems addressed | Expected outcomes | Decisions needed
Legend | Evidence and assumptions
```

For a workflow frame, use this arrangement:

```text
Topic — workflow | Audience | State | Review status
Trigger → numbered steps → outcome

Application developer | actions and handoffs
QA                    | actions and handoffs
DevOps                | actions and handoffs
Automation / systems  | automated actions and returned results

Exceptions | Open decisions | Legend | Evidence
```

Omit lanes that do not participate. Keep each step inside the lane of the person or system performing it.

### Readability rules

- Use one font family and a small set of text sizes. Start around 32–40 for titles, 20–24 for section headings, and 18–20 for node labels on a 1600 × 900 frame.
- Use short labels: a component name and, if needed, one line explaining its role.
- Use verb phrases for actions, such as “Select release manifest” or “Approve elevated access.”
- Aim for roughly 6–10 primary elements in an overview. Split the view when labels or connectors become hard to follow.
- Align nodes to a grid and use equal spacing and consistent box sizes.
- Use connectors with right-angle bends where practical; avoid crossing lines or routing them through labels.
- Put supporting explanation beside the diagram rather than inside large text-heavy boxes.
- Use service logos only when they improve recognition. Ordinary labeled boxes are sufficient for early proposals.

## 4. Legend and visual language

Repeat a compact legend in each frame. Use color as reinforcement; shape, labels, and line styles must also explain the meaning.

### Shapes and boundaries

| Symbol | Meaning | Example |
|---|---|---|
| Person icon or labeled actor box | Person or team | QA engineer |
| Rounded rectangle | Action or process step | Run Terraform |
| Rectangle | System, repository, service, or component | GitHub repository |
| Diamond | A real decision with labeled outcomes | Approval granted? |
| Document shape | An artifact passed between steps | Release manifest, plan output, test report |
| Cylinder | A persistent data store, where relevant | Database, artifact store |
| Large labeled container | Ownership, environment, platform, or security boundary | QA lab, Google Cloud project |

Do not use a diamond merely to highlight a problem. Use a numbered callout for problems and questions.

### Lines and labels

| Connector | Meaning |
|---|---|
| Solid arrow | Primary action, handoff, or data movement; label it with the specific action or artifact. |
| Dashed arrow labeled “depends on” | Dependency or prerequisite. |
| Dotted line labeled “maps to” | Association or identity/permission mapping, rather than a sequence of actions. |
| Branch arrows labeled Yes/No or with explicit outcomes | Decision results. |

Use arrowheads only when direction has meaning. Avoid unlabeled arrows between systems when their relationship could be interpreted in several ways.

### Color and evidence status

| Treatment | Meaning |
|---|---|
| Neutral gray fill (`#F3F4F6`) | Existing component or neutral context. |
| Pale blue fill (`#DBEAFE`) | Proposed addition or changed component; also label it “Proposed” or “Changed.” |
| Pale amber callout (`#FEF3C7`) | Open question, assumption, or decision needed. |
| Pale red callout (`#FEE2E2`) | Observed problem, manual bottleneck, or failure path. |
| Pale green callout (`#DCFCE7`) | Expected outcome in a proposal, or verified result when evidence exists; label which one. |

Use dark text such as `#111827`. Keep audience lanes neutral and identify them by name, so color does not have two competing meanings.

Distinguish evidence explicitly:

- **Verified:** Checked against a repository, cloud configuration, or another identified source; include the source and check date.
- **Reported in meeting:** Discussed in the transcript but not independently verified.
- **Reported in proposal notes:** A current-state claim from `bulletpoints.md`, not independently verified.
- **Proposed:** Intended future behavior, not a statement about the current system.
- **TBD:** An unresolved detail or decision.

Show automation separately from manual work with `[Automated]` and `[Manual]` labels. A solid arrow alone must not imply automation.

## 5. Audience perspectives

| Audience | What their view must help them understand | Recommended detail |
|---|---|---|
| CTO | Purpose, architectural fit, current problems, expected benefits, major dependencies, and decisions needed. | A small number of systems and relationships; avoid operational commands. |
| Application developer | Where they enter the flow, what they change or submit, approvals, feedback, and how they know the work succeeded. | Relevant repository, PR, build, deployment, permissions, and troubleshooting handoffs. |
| QA | What they are testing, how they obtain an environment, what they execute, and where results go. | Release manifest, environment selection/provisioning, test execution, results, and cleanup where agreed. |
| DevOps | What must be built or changed, who owns it, dependencies, and how it will be validated and operated. | Configuration, automation, access, environments, integrations, monitoring, and recovery paths where relevant. |

For every workflow, answer five questions: **Who starts it? What do they provide? What happens next? What do they receive? Who handles a failure?**

Do not invent team ownership, approval authority, or service-level commitments. Use role-level placeholders and mark unresolved responsibilities as TBD.

## 6. Content plan by topic

### A. Terraform PR review and controlled execution — proposal 01

Refined on 2026-11-13 after the user supplied the second brain. The original bullet list proposes GitHub Actions, plan → results → approval → apply, and main → dev. The saved code evidence is more specific: existing Actions planning covers changed development roots on PRs into main or preston; it has no apply job. Do not present merge-triggered apply or a fixed main → dev mapping as current fact. Source: [second-brain change-process answer](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-questions/cross-system/2026-11-09-tl-terraform-change-deployment-process.md), answered 2026-11-09 and updated 2026-11-10 against the 2026-11-04 source snapshot; [environment explanation](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-how-it-works/architecture/tl-terraform-environments.md). Current successful workflow runs and effective enforcement remain unverified.

- **Overview:** Build on the existing plan-only workflow. PR → GitHub Actions checks and target-specific plan → visible PR results → review and approve PR → merge → final plan against merged code and latest state → execution authorization → apply approved plan → verify and report.
- **Approval model:** PR approval authorizes merging code. Execution authorization controls applying the final plan. Propose explicit final-plan approval for staging and production; the development policy is a team decision. Check the repository's support for protected approvals before choosing the mechanism.
- **Environment scope:** Pilot development, then extend to staging and production. Each target has its own root, inputs, backend/state, plan and identity scope; main is a source branch, not an environment selector. Shared/common/RD and protected foundation roots require explicit scoping. QA/lab provisioning remains Proposal 05.
- **Developer perspective:** Submit or update a PR, inspect check/plan results, address feedback, and see apply status.
- **Reviewer perspective:** Inspect the proposed infrastructure changes, approve or request changes, and understand what triggers execution.
- **DevOps perspective:** Confirm existing CI, required checks, reviewer enforcement and current apply ownership. Extend root detection to affected shared-module consumers, pilot final-plan/controlled-apply automation, and validate revision/plan identity, per-state concurrency, outcomes and failures before extending coverage.
- **Design:** Keep author, PR automation, PR reviewers/merge, apply automation, execution approver, and results/exception lanes distinct. Show rejected PR approval returning to revision, denied execution stopping apply, failed PR checks returning diagnostics, and failed apply reaching DevOps. Failed or changed final plans must stop apply and require renewed planning/authorization.
- **Decision panel:** Review tool/check scope, non-Terraform PR behavior, affected roots and shared-module consumers, required checks and reviewers, development gate policy, staging/production execution approvers, supported approval mechanism, identities, apply trigger, plan freshness and shared-root rollout scope.

#### Environment promotion and requirement validation

Saved on 2026-11-16 from the user's follow-up discussion. The recommended flow below is a proposal for team review; the existing saved workflow remains development planning only.

**Relationship between the views:** 01B is the core workflow for a single target. 01D explains repeating it across environments, with each process box naming its matching 01B steps. 01E expands the checks before apply (steps 2–8) and the requirement tests in step 10, Verify outcome. The Miro boxes, subtitles and reading cue link these views for presentation navigation.

GitHub Actions can run Terraform to create or update infrastructure after a merge when an apply workflow, authorized cloud identity, target configuration and execution policy are configured. A branch name alone does not select the environment: the Terraform configuration folder (root), environment inputs, backend/state and cloud identity determine the target. [Terraform apply](https://developer.hashicorp.com/terraform/cli/commands/apply).

Two repository strategies can work:

| Strategy | Meaning |
|---|---|
| Environment branches | An explicitly configured workflow can map a merge to `dev` to a development deployment, and a later merge to `main` to a production deployment. These are chosen mappings, not Terraform defaults. |
| Main branch with explicit promotion | Reviewed code merges to `main`; a selected revision or module version is deployed to development, tested, then separately promoted to staging and production. A release/tag may identify the version; it does not inherently mean production. |

**Recommended direction:** use main with explicit environment promotion, building on the existing environment folders. PR → checks, preview plans and code review → merge to main → final development plan → development execution authorization → apply → requirement tests → promote the tested configuration/module version to staging → staging-specific plan, approval, apply and verification → promote to production → production-specific plan, approval, apply and verification. If acceptance tests fail, stop promotion and return to correction and review.

Every target needs its own plan against its inputs and current state. Never reuse a development plan file for production. Apply the exact plan authorized for that target; if the revision, inputs, target or state changes invalidate that plan, plan and authorize again. A GitHub release is optional version identification, not a substitute for planning or approval. [Terraform plan](https://developer.hashicorp.com/terraform/cli/commands/plan), [saved-plan apply](https://developer.hashicorp.com/terraform/cli/commands/apply).

With separate environment folders, a development-only edit does not automatically change production. Promotion must explicitly update the next environment's configuration or its reference to a tested shared-module version. A tag for a whole repository does not copy changes between folders. Keep a record of the configuration revision, module versions, target, plan approval, apply result and verification results for each deployment.

Define measurable acceptance criteria before apply and select the checks needed for the particular change:

| Stage | Verification | Example requirement and evidence |
|---|---|---|
| Before apply | Configuration validity, input constraints, plan review and security/policy checks | Expected resources, agreed region and capacity, private database access, backup settings, and review of replacements/deletions. |
| After apply | Read back actual resource settings and run functional/integration tests | Correct settings exist; the application can reach its database; an unauthorized identity is denied; health checks and key user journeys pass. |
| Where required | Performance, resilience and recovery tests | Meet an agreed load/latency target, demonstrate failover, or restore a backup within the agreed recovery target. |
| Before promotion | Review the acceptance evidence for the exact deployed revision and target | Required tests pass, outstanding issues are resolved or explicitly accepted, and the next target's own plan is approved. |

`terraform validate` checks configuration syntax and consistency; it does not validate remote services or establish that business requirements are satisfied. Successful apply alone is not acceptance. Terraform tests can assert module behavior using plans or test infrastructure; integration tests may create real resources and need an agreed test scope. [Terraform validate](https://developer.hashicorp.com/terraform/cli/commands/validate), [Terraform tests](https://developer.hashicorp.com/terraform/language/tests).

Separate PR approval, target-plan execution authorization and acceptance/promotion decisions. GitHub deployment environments support branch/tag restrictions and approval controls, with availability depending on repository visibility and the GitHub plan. Confirm supported controls before choosing the approval mechanism. [GitHub deployment controls](https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments).

Open decisions: whether development applies run automatically after merge or need approval; who accepts tests and authorizes each promotion; release/tag versus pinned revision/module-version strategy; criteria and owners for each test; supported approval mechanism. QA/lab provisioning remains Proposal 05. These per-change deployment stages are distinct from the earlier phased rollout of the automation capability itself.

### B. DevOps monorepo — proposal 02

Created as three editable Miro frames on 2026-11-16; links and verification are recorded in [progress.md](progress.md#proposal-02--devops-monorepo).

- **Current state:** Saved Nov 3–4 evidence identifies `tl-trekai-terraform`, `tl-trekcap-terraform`, `tl-lms-gitOps` and `cap-gitOps`. Other candidates include `ir-terraform-temporary`, `b-metric-dashboard-terraform` and legacy `trekai-infra`. Ansible/scripts remain scope to inventory. These are dated source observations, not a refreshed live inventory. Evidence: [GitHub inventory](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/reviews/github/reports/01-repo-inventory.md) and [supporting map/assessment](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-questions/cross-system/2026-11-09-gitops-supporting-repositories-and-components.md).
- **Proposed state:** A single DevOps repository with distinct Terraform, GitOps, automation and shared CI/docs areas. Preserve product/environment/state boundaries and ownership. Repository name and final scope remain decisions.
- **Contributor perspective:** Open PR → path/dependency-aware checks → affected-owner review → merge. Failed or unresolved checks block merge; changes requested return to revision and renewed checks/review.
- **Execution boundaries:** Terraform final plan/authorization/apply follows Proposal 01. GitOps changes are consumed by Argo CD under the agreed policy. Other automation needs its own identity and trigger. A shared commit does not establish atomic deployment across these processes.
- **Tradeoffs:** Easier discovery, reusable checks and coordinated review versus CI/dependency complexity, broader shared-change impact and access/integration migration. Compare with separate repositories using common standards/workflows. Folder review rules do not isolate code visibility; retain separate repositories if access requirements demand it.
- **DevOps delivery:** Inventory code, owners and consumers → agree scope and controls → prove a development pilot → cut over one scope at a time. Verify app workflow/GitHub App targets, Argo CD URL/revision/path references, Terraform paths/modules/backends, identity bindings and approval rules. Preserve one writable source per scope and rehearse rollback.
- **Design:** Side-by-side repository organization in 02A; role-based change flow and exceptions in 02B; friendly work-package cards and bullet panels in 02C. Match Proposal 01's native shapes, Noto Sans, and proposed/context/decision palette.
- **Decision panel:** Scope, naming, access, owners, checks/dependencies, cross-area ordering, history strategy, pilot, rollback and acceptance evidence. Consolidation remains a draft for review; no implementation approval or dates are implied.

### C. Platform and product monorepos — proposals 03 and 04

- **Trek Learning (Hub/LMS), Proposal 03:** Three native editable frames created and verified 2026-11-16; [frame links and evidence](progress.md#proposal-03--trek-learning-hublms-monorepo). Hub and LMS refer to the same product grouping in the saved map. The sourced [repository/delivery matrix](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-questions/cross-system/2026-11-10-trek-learning-repositories-and-delivery.md) identifies 16 repositories in the Nov 3 product group: 11 application repositories, 3 adjacent candidates (`tl-lms-db`, `tl-oss-components`, `tl-file-ingestion-pipeline`) and 2 DevOps repositories (`tl-lms-gitOps`, `tl-trekai-terraform`). Agree application/adjacent scope and coordinate the DevOps home with Proposal 02 before migration. Do not present 16 as an approved application-repo consolidation count.
- **03A overview:** Group the 11 app repositories by UI/core, AI/chat/tutor, and content/files/jobs; compare them with illustrative application/service/shared-CI/docs areas. Include benefits, constraints, a separate-repositories/shared-standards alternative and scope accounting. Shared packages are candidates where justified, not an invented current implementation.
- **03B workflow:** Propose change → detect affected services and consumers → tests/owner review → merge/build distinct images → GitOps proposal for selected services/target → Argo CD and QA verification. Include failed-check/revision and failed-deployment/acceptance paths. Preserve independent service release boundaries; coordinate contract changes and database migrations explicitly.
- **03C delivery:** Confirm owners/contracts/dependencies → agree folders/access/tooling/developer experience → pilot a service or service pair in dev → migrate groups with history and one writable source each. Verify build paths, caches, identities, review rules, GitOps writers, local setup and recovery. Completion evidence includes consumer-aware checks and commit/image/GitOps/outcome traceability.
- **03 current versus proposed:** Source snapshots Nov 3–4 describe app develop/staging/main image rebuilds and GitOps delivery; current effective behavior remains unverified. A monorepo does not require a branch-policy change, one shared deployment or automatic Terraform execution. Broader release-policy simplification belongs to Proposal 11; GitOps/DevOps repository consolidation is Proposal 02. Dates, named owners, scope and implementation approval remain team decisions.
- **TrekCAP and TrekFinder, Proposal 04:** Three native editable frames created and verified 2026-11-16; links/evidence in [progress.md](progress.md#proposal-04--trekcap-and-trekfinder-repository-consolidation). TrekCAP is the adaptive engine and TrekFinder the application. The [Nov 12 count clarification](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-questions/github/2026-11-03-which-repos-to-run-trekcap-trekfinder-locally.md#update-2026-11-12-platform-repository-count) establishes 17 repositories in the Nov 3 snapshot: 2 app, 9 engine/module/supporting-service, 4 CI/test and 2 deployment/infra. Exclude legacy `c-trekai-adventure`, which belongs to Trek Adventure. This replaces the original unknown count with dated evidence, not a guessed current count.
- **04A overview:** Compare the saved inventory with a proposed product monorepo for access-compatible code plus separately controlled restricted source/builds. Preserve the existing IP-sensitive `C-CI-GATES` policy ownership. Show approved artifacts flowing to consumers, benefits/tradeoffs and the alternative of separate repositories using common contracts/workflows. All repos are private in the snapshot; open is a source/IP classification, not public visibility. Verify actual grants before choosing consolidation groups.
- **04B workflow:** Restricted owner review → authorized sealing/build/image checks → versioned artifacts; separately, permitted product PR → affected-service build consuming pinned artifacts → proposed required integration/E2E gates → GitOps/RD reconciliation and deployed acceptance. Required-test failures stop the handoff. The saved orchestration workflow dispatches Tier 2 after GitOps merge; current success/effective blocking remain unverified. Pre-handoff gates and complete artifact traceability are proposed improvements, not existing proven controls. Do not invent stage/prod coverage or a universal sealed-image dependency for the UI/backend.
- **04C delivery:** Map actual source grants/classes/owners/consumers → agree access-compatible groups and trusted policy ownership → pilot a permitted UI/backend or similar group in the confirmed RD scope → migrate groups with history, one writable source and tested reference recovery. Verify source visibility, image/module pins, reusable CI, classification manifests, registry consumers, GitOps writers, dispatch targets and local setup. Resolve incomplete build paths before depending on them.
- **04 scope:** 17 is inventory context, not approval to place all source in one broadly readable repository. Folder review rules do not enforce separate read access. Coordinate `cap-gitOps` and `tl-trekcap-terraform` with Proposal 02; preserve separate Hub/LMS scope in 03. Future environments and release/promotion policy need explicit agreement with 11. Owners, scope, gates, dates and implementation approval remain decisions.
- **Proposed state:** Candidate consolidation boundaries, shared components if confirmed, and relationships to build and release workflows.
- **Developer perspective:** Where a change is made, which applications it affects, and how it is tested and released.
- **QA perspective:** How a release or build is identified for testing.
- **DevOps perspective:** CI/CD changes and migration dependencies.
- **Design:** Create a distinct overview frame for each grouping, using the same layout. Do not imply one repository spanning both groupings, or that a monorepo requires every application to deploy together.
- **Decision panel:** Pros and cons with application developers for each grouping, final scope, ownership, and build/test/release implications. Keep candidate benefits and tradeoffs labeled as items to evaluate.

### D. QA, sales demo and client pilot environments — proposal 05

Three native editable Miro frames created and verified 2026-11-16; [links and verification](progress.md#proposal-05--qa-environments-and-lab).

- **Owner clarification, Nov 16:** Separate internal QA, sales demo/POC and client pilot purposes. Customer environments must support complete agreed workflows; pilots must be production-like and accommodate multiple students. Reuse templates with separate configuration, access, data, capacity and lifecycle. These are three purposes, not an agreed instance count.
- **05A overview:** Keep the dated shared Trek Learning dev/staging/production and CAP RD context. The [saved environment explanation](/Users/ron/Documents/trekai/sm-trekai-infrastructure-and-product-review/trekai-how-it-works/architecture/environments.md) uses Nov 2–3 snapshots; an on-demand QA workflow is not established in that scope. Contrast QA functional/load/recovery tests and resets with stable sales demonstrations and supported client pilots.
- **Manifest:** Record artifact/template versions, settings/dependencies, purpose-specific data/account setup, secret references, business/technical owners, capacity, acceptance criteria, change windows, retention, reset and retirement rules. Identify exact deployed versions and instance in evidence.
- **05B workflow:** Owner selects purpose/manifest/profile → validate request/access/limits → review final target plan and authorize execution → scoped Terraform provisioning/verification → separate application deployment, integrations/accounts/data setup → readiness → QA and owner acceptance → accepted testing/demo/pilot use and operating evidence → purpose-specific reset or retirement. Hold invalid requests, failed/partial provisioning, unready instances and failed customer acceptance. Recheck fixes before sign-off.
- **Self-service intent (refined 2026-11-23):** QA requests an approved template, release, size, owner and expiry through a Jira form or permitted workflow. DevOps maintains templates, scoped execution identities and limits; automation runs Terraform and deploys applications. Start with DevOps approval of each final QA plan. After proving isolation, limits, notifications and cleanup, the team may authorize proven routine requests within policy to proceed automatically; custom, larger or sensitive-data requests retain review. QA needs no direct Terraform or cloud administrator access. Preserve separate sales/pilot acceptance, data and lifecycle rules. Reuse 01B controls; each target needs isolated state and scoped ownership. Infrastructure, deployment and acceptance remain separate handoffs.
- **Acceptance:** All agreed end-to-end workflows, accounts and integrations pass before customer use. Rehearse demonstrations; validate the pilot's student/teacher workload against agreed concurrency, response/error and duration thresholds. Verify persistence, monitoring, support and backup/restore as agreed. “Fully functioning” describes measurable product and operating requirements; availability targets remain to agree.
- **Isolation:** Prevent QA resets, load and fault tests from disrupting customer sessions. Separate identities, data, deployment targets and state. Choose shared versus dedicated project/cluster/services by impact and validate shared dependency isolation; a namespace alone may not contain every failure.
- **Lifecycle:** QA completion/expiry can trigger approved reset/cleanup. Demo data refresh/reset happens between agreed sessions. Active pilots retain data/service; the owner approves changes, extensions, retention/export and retirement. Do not apply automatic QA cleanup to active customer use. For retirement, stop deployment desired state before removing only owned resources; exclude shared/protected services, verify residue/cost and assign failure follow-up.
- **05C delivery:** Agree requirements by purpose and infrastructure-code coverage → design reusable profiles and operating policies → prove QA recreation, a full sales rehearsal and a production-like multi-student pilot → launch agreed instances with monitoring, support, change windows, cost review and owner-led retirement. The implementation trial is distinct from the client pilot environment.
- **Data and cost:** Use approved test/demo fixtures and explicitly approved pilot data. Agree access, recovery, resource sizing/quotas/concurrency, budgets and duration per purpose. Numeric limits, instance count, dates and named owners remain open.
- **Relationships:** Consume approved 03/04 artifacts, reuse 01 execution controls and coordinate release policy with 11. Monorepo migration is not a prerequisite. Production promotion and pilot-to-production transition remain separate decisions; provisioning/recreation alone does not prove production disaster recovery.

### E. Documentation and knowledge base — proposal 06

Three editable native Miro frames created 2026-11-16; [frame links and verification](progress.md#proposal-06--documentation-and-knowledge-base).

- **Evidence:** The proposal notes describe incomplete and fragmented documentation; the Nov 12 discussion at 04:45 reports useful but outdated Confluence/product pages. Label these as reported concerns. Inventory actual content and verify freshness during implementation rather than implying a completed audit.
- **06A knowledge map:** Propose a clear task/role/product/environment index linked to an authoritative source per topic. Cover DevOps first (Terraform, CI/CD/GitOps, releases, QA provisioning and runbooks), cloud architecture (environments/components, networking, access and dependencies), then TrekAI products (Hub/LMS, CAP and Finder interactions/user journeys). An entry point does not require moving every document into one tool.
- **Page minimum:** Purpose/audience, product/environment scope, prerequisites, steps, expected outcome, failure handling, content owner/reviewer, status, verification date, applicable version and authoritative references. Link explanations to code/configuration and dated evidence; distinguish current behavior from proposed changes.
- **Concrete starting guide:** Use temporary QA setup to connect release manifest selection, approved infrastructure workflow, readiness, testing, expiry/cost ownership and cleanup failure handling. Link to 05B and 01B. Write the operational guide against the agreed implementation/version.
- **06B maintenance workflow:** Change/incident/reader gap → owner assignment and scope → author draft/update → domain review and instruction validation → publish/index → reader locates guide → uses/checks outcome → feedback task → refresh, reaffirm or retire. Explicitly handle unresolved ownership/conflicting sources, failed review and stale/missing/inaccessible pages. Changes and periodic reviews feed back into assignment/review; retire obsolete guidance with a replacement link.
- **Change coupling:** Infrastructure/application/access/environment changes trigger documentation impact checks. Track updates with the change/release and agree which guides must be ready before handoff. Cadence, overdue escalation, reminders/automation and publishing authority remain team decisions.
- **06C delivery:** Inventory/prioritize → agree structure/canonical sources/ownership/templates → prove one DevOps guide with a second reader → expand cloud and product coverage and maintain it. Proposed roles are DevOps, domain owners/reviewers, QA and team leads; no named assignments or dates are committed.
- **Acceptance:** A reader finds the authoritative guide, another reader completes an agreed task with the stated outcome, scope/version/date are visible, a sample system change triggers the appropriate documentation update, and feedback/stale/retired content reaches an accountable owner.
- **Decisions and boundaries:** Agree entry point, per-topic source of truth, priority gaps, owners/reviewers, access, cadence and delivery checks. Preserve existing source-access boundaries and use secret references. Detailed Confluence/runbook delivery follows review of this proposal. Tool migration, repository consolidation and AI ingestion are not assumed.

### F. Observability and alerting — proposal 07

Three native editable Miro frames created 2026-11-16; [frame links and verification](progress.md#proposal-07--observability-and-alerting).

- **Evidence:** The Nov 12 discussion at 05:56 reports deployed tools but questions effective use/alert visibility; 06:34 explicitly requests enabling alerting. These are reported concerns. Verify actual tools, instrumentation, rules, routes and ownership before making live-state claims or choosing implementation changes.
- **07A overview:** Workload/dependencies → relevant telemetry → ingest/store/query → useful alert rules → scoped notification → accountable response and verified recovery. Cover availability, errors, latency, capacity and critical journeys. Actual tool names, channels, recipients, numeric targets and response arrangements remain decisions.
- **Developer/QA perspective:** Directly inspect dashboards, logs and traces where useful. Correlate symptoms with product, environment, release and instance/manifest context. QA records behavior and evidence during tests; developers investigate service/version issues.
- **Environment purposes:** Coordinate temporary QA test/expiry/cleanup handling with 05B. Agree stable-service monitoring/support for sales demos, client pilots and production. Test/maintenance silences have explicit scope and expiry; missing/stale collection has its own policy.
- **07B response flow:** Emit → collect/check freshness → evaluate condition/window/severity → deliver contextual notification → acknowledge/assign incident ownership → investigate → scoped authorized mitigation → verify the affected service/journey and fresh signals → close/communicate/improve. Keep no-condition cases observing. Explicitly handle no data, delivery failure, missing acknowledgement and failed mitigation; unresolved recovery returns to investigation.
- **Alert content and response:** Include symptom, impact/scope, environment/service identity, evidence and runbook. Agree primary/backup roles, coverage, destinations, acknowledgement timing, escalation and incident tracking. A configured/sent event does not by itself establish receipt, response or recovery.
- **07C delivery:** Inventory existing setup and critical-impact gaps → agree alerts/response coverage → configure a focused first scope with instrumentation, labels, dashboards, routes and runbooks → exercise controlled failures, absent data, failed delivery, escalation, recovery and QA expiry → tune and expand. No vendor migration, numeric service promise, 24/7 commitment, dates or named assignments are implied.
- **Acceptance:** A controlled failure generates the expected scoped alert; the real primary receives it and ownership is recorded; alternate/escalation paths work; fresh signals and the affected journey confirm recovery. Exercise absent data, duplicate noise and silence expiry. Retain evidence and repeat validation after rule/route/ownership changes.
- **Operating controls:** Review/version rule and routing changes, own runbooks through 06, monitor telemetry and notification paths, tune noise/coverage regularly, and agree data minimization/redaction, access, retention and collection cost. No live rules, notification messages or operational mitigations are executed while creating these proposal diagrams.

### G. Microsoft Entra ID, permissions, and PAM — proposals 08–10

Create a connected set with three identifiable proposal overviews. Keep sign-in/federation, group/permission mapping, and elevation visually distinct so each relationship is understandable.

#### G1. Entra ID as IdP for Google Cloud — proposal 08

Three native editable Miro frames created 2026-11-16; [frame links and verification](progress.md#proposal-08--entra-id-for-google-cloud).

- **Evidence and scope:** Proposal notes and Nov 12 discussion (06:54–10:37) request Entra as Google Cloud IdP, permission changes, meaningful roles/groups/naming and a baseline model that informs PAM. This proposal addresses staff cloud access; current tenant setup, effective grants and required clients/services remain to inventory. Track service-account/CI/workload identities separately.
- **08A architecture:** Separate Entra and Google Cloud boundaries. Solid sign-in trust arrow: person authenticates in Entra → selected Google identity/session integration. Dashed access-mapping arrow: approved Entra team/group membership → mapped identity/group and scoped Google IAM baseline role. A separate IAM evaluation step determines resource permissions; successful sign-in alone does not define allowed actions.
- **Integration decision:** Official Google documentation checked Nov 16 describes [Workforce Identity Federation](https://docs.cloud.google.com/iam/docs/workforce-identity-federation) and [Entra SSO/provisioning with Cloud Identity or Workspace](https://docs.cloud.google.com/architecture/identity/federating-gcp-with-azure-ad-configuring-provisioning-and-single-sign-on). Show these as alternatives to evaluate, not selected architecture. Confirm required services, console/CLI, identity/group handling and lifecycle for the chosen model. [Google IAM overview](https://docs.cloud.google.com/iam/docs/overview) supports the authentication/authorization distinction.
- **Permission and naming work:** Plan, review and change direct/group/inherited access at the relevant resource scope. Agree task-based baseline roles, group owners and membership approvals. Names communicate team, product/environment and purpose; `qa-learning-nonprod-observe` is explicitly illustrative. Record stable group identifiers, target roles and resource scope rather than relying on display names alone.
- **08B workflow:** Staff task/scope → approved membership → Entra authentication → accepted cloud identity → IAM permission evaluation → confirmed allowed scope → scoped task → relevant outcome/audit evidence → access maintenance. Include blocked sign-in, identity/mapping mismatch, denied/more-access-needed and unexpected allow/deny behavior. Baseline changes require the agreed approval; eligible temporary elevation follows Proposal 10's separate design.
- **Lifecycle:** Joiner/mover/leaver changes trigger membership/mapping/IAM reconciliation. Test additions, changes, removals, remaining direct grants and active-session/propagation behavior in the selected model. Do not assume immediate revocation or that group removal removes every alternative grant.
- **08C delivery:** Inventory identities/current paths/effective permissions and administrative recovery → agree baseline tasks/roles/scope/names/mappings and integration → limited representative developer/QA pilot → controlled cohort migration and recurring maintenance. Validate before retiring replaced paths/grants. Proposed role owners are identity/Cloud administrators, team/security leads and pilot users; no named assignments or dates are committed.
- **Acceptance:** Supported console/CLI and required service access work; intended actions succeed while out-of-scope actions remain denied. Multiple memberships/direct/inherited grants match the model. Membership changes/departures remove access as designed; propagation/session behavior, audit evidence, support and administrative recovery are exercised.
- **Boundaries and decisions:** Proposal 09 covers GitHub; 10 defines target-specific temporary elevation. No universal read/write roles, automatic Entra-to-all-resource access, strict finalized migration sequence, workload-identity change or live permission grant is implied. Agree integration, service/client scope, mapping/role owners, membership/cutover approvals, lifecycle/support and PAM handoffs. Maintain the access catalog through 06B.

#### G2. Entra ID as IdP for GitHub — proposal 09

Three native editable Miro frames created 2026-11-16; [frame links and verification](progress.md#proposal-09--entra-id-for-github).

- **Evidence and scope:** Proposal notes and Nov 12 discussion (06:54–10:37) request Entra for GitHub, clearer group/team mappings and meaningful names/access. Inventory current GitHub deployment, plan, account model, members, teams and effective permissions before choosing the integration. Scope is staff GitHub access, with automation/App/deploy-key identities tracked separately.
- **09A overview:** Separate Entra and GitHub boundaries. Solid arrows show identity/SSO context and access evaluation; a dashed arrow shows approved group-to-team membership. GitHub teams receive explicit repository roles. Review organization base permissions, direct/collaborator access and team-derived grants. Preserve restricted-source boundaries from 04A.
- **Account-model decision:** Official [GitHub SAML guidance](https://docs.github.com/en/enterprise-cloud@latest/admin/managing-iam/understanding-iam-for-enterprises/about-saml-for-enterprise-iam) checked Nov 16 distinguishes personal accounts with SAML SSO from Enterprise Managed Users. Personal accounts keep their normal GitHub login. Select the supported model/integration after validating deployment/plan, migration, provisioning and collaboration requirements; do not assume an enterprise-type migration is an ordinary setting change.
- **Membership versus provisioning:** [Team synchronization guidance](https://docs.github.com/en/enterprise-cloud@latest/organizations/managing-saml-single-sign-on-for-your-organization/managing-team-synchronization-for-your-organization) distinguishes the mechanisms for personal-account/team-sync and managed-user models. Establish organization membership and GitHub teams as required; group mapping does not itself define repository roles or replace organization provisioning. Exact scope/mechanism remains open.
- **Names and roles:** Agree understandable group/team names, stable Entra group IDs, GitHub organization/team identity, owners, target repositories and roles. `dev-learning-source-write` is explicitly illustrative. Use [repository-role guidance](https://docs.github.com/en/organizations/managing-user-access-to-your-organizations-repositories/managing-repository-roles/repository-roles-for-an-organization) to validate required actions; branch/review rules remain separate constraints.
- **09B workflow:** Staff task/repository scope → approved organization/group membership → model-specific GitHub/Entra identity checks → accepted membership/mapping context → repository permission evaluation → confirmed allowed scope → task → relevant evidence → lifecycle maintenance. Include blocked login/SSO, incomplete mapping/provisioning, denied/additional access and unexpected visibility/actions. Access changes use the agreed GitHub approval route.
- **Lifecycle:** Reconcile joiner/mover/leaver events across Entra assignment, organization membership, teams, direct/collaborator roles and relevant human credentials. Verify sync/session/removal behavior and remaining paths rather than assuming one group removal revokes everything. Keep automation identity review separately scoped.
- **09C delivery:** Inventory → select identity/team/role model and naming → representative pilot covering web/Git/CLI/API credential paths, allowed/denied actions and restricted sources → controlled cohort migration and recurring maintenance. Verify access before retiring replaced grants/paths; test audit, support and administrative recovery. Owners are proposed roles, not named assignments.
- **Acceptance and boundaries:** Required actions work; restricted repositories/actions remain denied; base/direct/team/inherited grants match policy; membership and credential lifecycle behavior is verified. Coordinate source-access boundaries with 02–04 and documentation with 06. Proposal 10 must define any supported GitHub elevation mechanism; no automatic Google Cloud PAM-to-GitHub grant, current feature availability, live configuration change or implementation date is assumed.

#### G3. Role-based default access and PAM — proposal 10

Three native editable Miro frames created 2026-11-16; [frame links and verification](progress.md#proposal-10--role-based-default-access-and-pam).

- **Evidence and scope:** Proposal notes and Nov 12 discussion (07:43–10:37) call for team/job-based default access and temporary elevation through meaningful entitlements. Read versus write is an illustrative distinction, not a universal policy. Current standing access, target coverage and elevation configuration remain to inventory.
- **10A overview:** Team/job → approved membership/mapping → separately authorized baseline access. A distinct path uses an entitlement catalog → eligible request and configured policy/approval → time-bound grant at the selected target → expiry/revocation and removal verification. An entitlement is a predefined requestable access definition; a grant is one activation, not permanent membership.
- **Catalog:** Define name/purpose, target platform, resource/repository scope, roles, eligible requester identities/groups, approval/justification policy, maximum duration, accountable owner, audit, early-ending capability and verification requirements. No specific roles, duration, approvers or assignments are committed.
- **Target-specific implementation:** Official [Google Cloud PAM overview](https://docs.cloud.google.com/iam/docs/pam-overview) and [grant lifecycle guidance](https://docs.cloud.google.com/iam/docs/pam-request-temporary-elevated-access) checked Nov 16 support the Google IAM elevation path. Validate identity compatibility and effective scope against 08. GitHub needs an independently supported mechanism matching 09; [Entra PIM for Groups](https://learn.microsoft.com/en-us/entra/id-governance/privileged-identity-management/concept-pim-for-groups) is a candidate to evaluate, not a verified GitHub integration. Prove downstream activation/removal timing and group synchronization. Google Cloud PAM does not directly grant GitHub repository permissions.
- **10B lifecycle:** Identify task/entitlement/duration → validate eligibility/scope → satisfy configured approval/control requirements → issue grant → apply target access → verify effective elevated action → perform scoped task → expiry or supported early ending → verify removal and retain evidence. If baseline is sufficient, use the normal task workflow.
- **Exceptions:** Ineligible/declined/expired requests do not activate access. Hold tasks on failed/partial activation or mismatched scope. If a grant ends, stop privileged work; a new window needs a new request. If the elevated action still works after expected end, keep follow-up open, reconcile target bindings/membership/sessions/other grants, assign an owner and repeat the denial check.
- **Timing and baseline:** Test propagation and session behavior for each target; early task completion follows an agreed early-ending policy. Verify the elevated action becomes denied after the grant ends. Baseline remains only while its separate membership/role authorization is still valid; remaining standing grants must not mask a failed removal test.
- **10C delivery:** Agree normal/elevated tasks and review standing/overlapping grants → design per-target catalog/policies/owners → prove a limited entitlement across rejection, activation, use, expiry/revocation and removal failure → expand and remove replaced standing grants only after validation. Publish runbooks through 06 and coordinate audit/exception response with 07.
- **Acceptance and decisions:** Baseline works while elevated actions are denied before activation; ineligible/pending/declined requests add no privilege; an active grant permits only agreed scope; expiry/revocation removes elevation while valid baseline remains. Exercise delays, remaining access, audit and exception escalation. Agree roles/scopes, target mechanisms, eligibility/approvals, duration/reason, emergency/recovery access, owners and recurring review. Elevation does not replace normal change/execution controls from 01, and the final 08/09 migration sequence remains open.

#### G4. Team structure before access mapping — proposal 10D (added Nov 24, 2026)

- **Proposed structure:** Application developers build product/platform application code; DevOps builds and operates environments, infrastructure and delivery tooling; QA tests releases and requests approved environments; management/leadership includes leads, managers and directors with agreed coordination, reporting and oversight duties. Reporting lines, memberships and named assignments remain unresolved.
- **Access design:** Define team + task + product + environment, then approved Entra groups, Google IAM roles/GitHub repository permissions, baseline access and separate elevation eligibility. Record group/access owners, membership rules, meaningful names, target scope and mappings. Titles grant no automatic administration or approval authority; hands-on leads need explicitly assigned technical roles.
- **Illustrative baselines:** Developers get scoped source/development access; DevOps gets agreed non-production operational/delivery access; QA gets test accounts, allowed diagnostics and controlled requests; management gets agreed reports/dashboards. Production, sensitive-data and administrative tasks need separately scoped authorization. Provider role IDs and exact permissions remain to design.
- **Boundaries:** Preserve Trek Learning (Hub/LMS), TrekCAP/TrekFinder restricted-source boundaries, environment scopes and separate automation identities. QA self-service from 05 needs no default Terraform/cloud administration. Validate Google PAM and any GitHub elevation mechanism separately; test allowed/denied actions, role changes, overlapping grants and removal.
- **Artifacts and basis:** Native editable 10D matrix beside 10A–10C; revised 10A inputs and 10C delivery/decisions in place. Presentation topic 06 adds team-structure and mapping slides and expands its baseline matrix. Basis: original proposal intent, Nov 12 discussion (07:43–10:37), user clarification Nov 24, 2026. No organization or access configuration is implemented.

**Shared decision panel:** Team structure, default roles, naming rules, identity/group mappings, permission changes, PAM target systems, eligible entitlements, request/approval rules, and temporary access duration. Show role/group design as an input to meaningful entitlements without presenting a strict migration sequence as finalized.

### H. GitOps centralization and SDLC simplification — proposal 11

Three native editable Miro frames created 2026-11-16; [frame links and verification](progress.md#proposal-11--gitops-and-sdlc).

- **Evidence:** The proposal notes and Nov 12 discussion at 11:11 request centralizing GitOps work and simplifying SDLC. At 23:05, the reviewed workflow was reported to automate development, with manual work after PR comments/approvals for staging/production. Label this as reported context; inventory the actual product/repository/step coverage before changing it.
- **11A overview:** Show dev/staging/production separately beside reported gaps. Propose a shared GitOps area/conventions and authoritative, owned desired state per product/target. Choose repository placement with 02 while preserving access boundaries; repository consolidation is not a prerequisite.
- **Release contract:** Build/test and publish pinned immutable application artifacts plus a service-version manifest. Promote the accepted artifact set through dev → staging → production without rebuilding it for each environment. Each target has its own reviewed configuration, dependencies, secret references, acceptance evidence and release authorization. Branch/reference mappings and automated promotion policy remain decisions.
- **GitOps model:** [OpenGitOps principles](https://opengitops.dev/), checked Nov 16, support versioned declarative desired state pulled and continuously reconciled by agents. Propose target-scoped reconciliation with actual revision/version/health/drift reporting; verify the current engine and ownership before selecting implementation changes.
- **11B workflow:** Source PR → CI/owner checks and source review → merge/build/publish candidate → explicit target desired-state PR → render/policy/artifact/prerequisite checks and target authorization → merge reviewed target revision → pull/reconcile → readiness/journey/health acceptance → record promotion decision → operate/recover. Repeat the target steps for staging and production using the same artifacts. Include failed source checks/review, failed candidate build/publication and sync/readiness/acceptance failure.
- **Ownership and evidence:** Developers own application changes, CI publishes candidates, release/service owners authorize target changes, QA supplies agreed acceptance evidence and DevOps owns the delivery platform with service owners. Trace source commit, artifact manifest, GitOps revision, environment and test/health outcomes. QA acceptance authority and exact release gate ownership remain to agree.
- **Failures and recovery:** Hold the next promotion when source/build/target checks fail. Keep diagnostic/version evidence and assign an owner; return fixes/reverts through the appropriate review path and reverify. Continuously report drift/failed reconciliation. Recovery must account for dependencies and data/schema compatibility; Git reversion alone does not restore database contents or prove disaster recovery.
- **11C delivery:** Inventory real CI/deployment paths/manual gaps → agree shared manifest/state layout/engine/target mapping/owners/gates → prove one scoped development release including failure/drift/recovery → extend staging and production after equivalent evidence and replace manual steps deliberately. Retain runbooks, release records and recurring review.
- **Relationships and decisions:** Infrastructure changes use 01 controls; artifacts follow 03/04, and source/state placement is coordinated with 02. QA, sales demo and client pilot manifests/lifecycle follow 05 separately from promotion. Use 06/07 for runbooks/observability and 08–10 for access/execution identity decisions. No Terraform-to-app deployment, automatic main-to-production behavior, current engine, universal branch strategy or live release is implied.

### I. AI brain — supplementary scope item

The meeting explicitly included the AI brain in the initial conversation material, but did not define its architecture or required diagram details. It is not listed in `bulletpoints.md`, so keep it visibly separate from the confirmed proposal topic list.

- Reserve a placeholder marked **Supplementary — inclusion and scope to confirm**.
- Establish its purpose, users, inputs, outputs, source systems, and boundaries before drawing a proposed architecture.
- Add audience workflows only after those requirements are clear.
- Do not assume ingestion, indexing, access controls, or connections to documentation from the name alone.

## 7. How to build the diagrams

1. **Create the visual template.** Build one overview frame, one workflow frame, one delivery-plan frame, and a reusable legend. Duplicate these for each topic.
2. **Map proposal coverage.** Use the eleven-item index to confirm every change from `bulletpoints.md` has an overview and a clear team discussion/decision. Keep AI brain supplementary.
3. **Inventory the evidence.** List known components and relationships, proposal-note claims, transcript timestamps, repository/cloud evidence, and unresolved details.
4. **Draw the current state.** Capture the main systems and important manual steps. Mark reported findings and unknowns honestly.
5. **Add problem markers.** Use P1, P2, and so on, with a short explanation of each problem.
6. **Draw the proposed state.** Use matching problem references to explain what each proposed change addresses. Keep unchanged context visually neutral.
7. **Draw the human workflow.** Walk through one concrete scenario with the relevant audience lanes, numbered steps, handoffs, outputs, and one important failure path.
8. **Add the delivery plan.** Group work into logical packages such as inventory → design/review → implementation → validation → rollout. Label role ownership and prerequisites; avoid invented dates or commitments.
9. **Simplify the CTO view.** Keep the purpose, major change, benefits, dependencies, and decisions visible at presentation scale.
10. **Review the set for consistency.** Reuse the same names, shapes, colors, state labels, and environment terminology across all topics.
11. **Prepare for feedback.** Add a clearly labeled questions area beside each topic. The meeting anticipated reviewers interacting with diagrams and making suggestions.

## 8. Review sequence and completion criteria

Use the review path discussed in the meeting: initial material for Preston, then John, followed by discussion. Keep the content at presentation level until the direction is approved.

A topic is ready for initial review when:

- Its purpose and architectural fit are clear without a spoken explanation.
- The proposal is traceable to `bulletpoints.md`, or explicitly marked as supplementary, and the team's requested decision/feedback is visible.
- Current state, proposed state, problems, and expected outcomes are distinguishable.
- Relevant audiences can find their actions, handoffs, and results.
- The implementation work and important dependencies are visible.
- Every arrow has a clear meaning, and symbols follow the shared legend.
- Reported findings, verified facts, proposals, and unknowns are labeled accurately.
- A reviewer can see which decisions are needed and leave feedback in context.
- The frame remains readable at presentation size without zooming into small text.

After direction is approved, expand the material into detailed architecture documentation, operational procedures, and runbooks as appropriate.
