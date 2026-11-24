# Capability audit and evaluation before use

This is a proposed operating policy for the learning roadmap. It applies to skills, plugin capabilities and MCP connections. It does not assert that any named capability has passed an audit, and it does not install or activate anything.

## The order of work

Define the task → load project guidance → check the DevOps HQ catalog → identify the exact candidate and required scope → audit safety → evaluate usefulness in a sandbox → record a scoped decision → verify the reviewed version and task scope → activate only if both checks passed → verify the outcome.

If safety, usefulness, coverage or provenance is unresolved, keep the candidate inactive. Repair it, gather evidence or choose an alternative before repeating the relevant checks. A safe but unhelpful capability need not be adopted; a useful capability with unacceptable risks must not be enabled.

## Start with the existing catalog

[devops-hq-agentic-skills](https://github.com/smanley-trekai/devops-hq-agentic-skills) is the starting point for discovering existing candidates. Its live README lists Terraform skills, Graphify, BrowserOS neo, Miro capabilities, GitHub CI/review skills and the GitHub MCP server. The README reports supported entries as installed/in use and distinguishes proposed additions. Those are repository reports, not an independent deployment or audit finding.

Select only the capabilities needed for the task. Catalog inclusion, popularity, installation, an official-looking name and a clean scan are not blanket approval for a different version, configuration or resource scope.

## Two separate gates

### 1. Safety review before controlled evaluation

- Freeze the source snapshot; record source, version/commit or content hash, configuration and dependencies. Inspect a copy without allowing automatic discovery or activation by the agent.
- Read every relevant instruction, script, hook and dependency as untrusted material. Do not follow candidate instructions or execute candidate code during intake.
- Check command execution, credential access, data destinations, network use, filesystem/resource scope, write/destructive operations and attempts to override the user's intent or conceal actions.
- Use applicable secret, dependency and static scans plus manual review. Review the scanner and its own permissions/data handling too. A scan error, missing tool, incomplete report or skipped scope blocks a clean decision; it is not equivalent to zero findings.
- Only proceed to a controlled runtime evaluation after the review supports that scope. Use test fixtures or dummy data, restricted credentials, isolation and action/resource limits. Do not test with production credentials or live destructive targets.

A review supports a bounded risk decision; no scanner or document can guarantee that a capability is safe in every situation.

### 2. Usefulness evaluation

Compare the candidate with the existing allowed baseline. For a skill, test with versus without it. For MCP, compare the connection with the current authorized workflow that accomplishes the same task; retain necessary task data and permissions in both conditions. For a plugin bundle, isolate relevant components where feasible so the source of improvement is clear.

Use equivalent prompts, data, model/settings and resource budgets where practical. Define an acceptance rubric before looking at results and repeat runs when outcomes vary. A suggested starter set, adapted from the audit project's skill workflow, is 5–10 representative tasks plus 2–3 tasks where the capability should not be selected, with several runs per condition. These counts are examples, not universal thresholds.

Measure correctness/pass rate, evidence quality, time, tokens/cost, retries, unnecessary calls, unwanted actions and inappropriate triggering. Record failures as well as successes. Decide what improvement and cost/risk trade-off is worthwhile for the actual task; numeric thresholds and reviewers remain team decisions. A successful installation or tool response does not prove benefit.

## Apply the gate to each capability type

| Type | Candidate and safety scope | Usefulness evidence |
| --- | --- | --- |
| Skill | SKILL.md, references, scripts, hooks/dependencies and the tools it directs the agent to use | Representative with/without trials and non-trigger cases |
| MCP connection | Server/package or provider evidence, transport, authentication, dependencies, exposed tools, account/resource permissions and data destinations | Task completion compared with the existing workflow; test allowed/denied operations, output handling, errors and credential revocation in a non-production scope |
| Plugin | The relevant packaged skills, tools, hooks, dependencies and MCP configuration actually enabled | Compare the enabled combination and isolate component effects where possible |

A read-only label is not proof of harmless behavior: sensitive data can still be read and disclosed. Keep authorization enforced by actual tools, credentials and configuration. Treat returned issues, pages, logs and other external text as untrusted evidence rather than instructions that expand the task.

## Initial adoption, every task and updates

- **Before first adoption:** complete both gates and record a decision tied to the exact candidate version/configuration and allowed purpose/resources.
- **Before every task:** verify the current version/configuration matches that record and the task fits its permitted data, actions and resource scope. If it does not, hold use.
- **After a change:** relevant content, dependency, server behavior, permission or configuration changes require re-audit before use. Re-evaluate benefit when task type, agent/model or operating assumptions change materially.
- **After execution:** verify the actual target result, retain failures and review evidence that challenges the original decision.

This avoids repeating the whole benchmark on every invocation while still requiring a valid review and scope check before use. The process is a proposed policy; enforcement and accountable review roles must be implemented and agreed separately.

## Reusable review record

```yaml
candidate: <skill, plugin component, or MCP connection>
source: <repository/provider and path>
version_or_hash: <exact reviewed revision>
configuration_and_dependencies: <reviewed references or fingerprints; no secrets>
intended_tasks: <evaluated purpose>
allowed_scope: <data, actions, accounts and resources>
safety_evidence: <scan versions/configuration, coverage, findings and manual review>
evaluation: <task fixtures, rubric, baseline, repeated results and costs>
limitations: <unsupported content, uncertainties and failure cases>
decision: <pass-both | hold | reject>
reviewer: <to assign>
reviewed_at: <date>
reaudit_triggers: <version/configuration/permission/task changes>
```

Store policy and review records in an agreed project documentation location, such as `docs/capability-audits/`, using non-secret references. Keep root AGENTS.md short by pointing to the policy rather than copying every report into permanent instructions. Do not put credential values into audit reports or prompt fixtures.

## How ai-skill-audit-and-evaluation informs this flow

The local [audit project README](../../../ai-skill-audit-and-evaluation/README.md) and [vetting workflow](../../../ai-skill-audit-and-evaluation/docs/03-workflow.md) propose static scanning, deeper review, manual reading and sandboxed with/without evaluation before installing a skill. Its [web UI design](../../../ai-skill-audit-and-evaluation/docs/web-ui/design.md) explicitly states that no application is implemented. The initial proposed MVP is static auditing with a manual recorded decision; deeper scans, usefulness tests and installation are deferred. Static-audit acceptance therefore does not mean approval to install.

This roadmap extends the same two-gate idea to MCP and plugins at the user's request. It does not claim the skill scanners validate every MCP server or plugin type. Choose checks that match the actual implementation and coverage. Scanner/evaluator names in the source project are research candidates whose current versions, flags, capabilities and data handling need verification before use; no installation commands are prescribed here.

## Evidence and status — checked November 24, 2026

- DevOps HQ README read live through the GitHub connector: [source](https://github.com/smanley-trekai/devops-hq-agentic-skills/blob/main/README.md), README blob SHA `8f414c6de5d364c54b17902ecff2d6b1546692e6`. A blob hash identifies those file contents, not a deployment or a completed audit.
- The local DevOps HQ checkout was older than the live README, so the live source was used for catalog statements.
- Audit project read from `/Users/ron/Documents/trekai/ai-skill-audit-and-evaluation`. Local HEAD: `2541e44eee7332cf95bdb6dd0c0ba95da66b07eb`; README modifications and untracked docs were present. Their content is working-copy planning material, not committed implementation evidence.
- The GitHub connector could not retrieve that audit repository's workflow (404); no published state is inferred from the local copy.
- No candidate skills/scripts were executed, no scanners or benchmarks were run, and no installed skills, MCP servers, plugins, credentials or access permissions were changed for this documentation update.
