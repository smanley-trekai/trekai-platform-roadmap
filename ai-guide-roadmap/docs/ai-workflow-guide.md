# Using AI Agents for Software Development and DevOps

The most useful change is to give AI a clear task, the relevant evidence, and a way to check its work. Let it perform the routine execution while you retain responsibility for intent, architecture, and consequential decisions. The recurring pattern across these videos is **understand → plan → execute → verify → review**. The benefit comes from making that whole workflow easier to repeat. [Vibe and agentic coding](https://www.youtube.com/watch?v=h4tHDFCPmQE&t=214s), [prompt to production](https://www.youtube.com/watch?v=bs1qPy_CWkM&t=151s).

This guide combines the knowledge in your 14 videos. The workflows, examples, and practice plan below are proposed applications of that knowledge. They are not productivity results measured by the presenters. For the individual sources, see the [video reference](video-reference.md); for disagreements and simplifications, see the [advice comparison](advice-comparison.md).

## Understand the pieces

A coding assistant can answer a question or generate a patch. An **agent** can also use tools, inspect the result, and choose another action. Its loop is: receive a goal, act, observe, adjust, and check whether it should stop. That makes a reliable stopping condition as important as the initial prompt. [Agent loops](https://www.youtube.com/watch?v=4LINhsEZEDI&t=16s).

Several other terms describe different parts of the same system:

| Piece | What it contributes | Example in your work |
| --- | --- | --- |
| Specification | The intended behavior, constraints, and definition of done | A reset token expires after 15 minutes and can be used once |
| Context | The information available to the model during the task | Relevant code, dependency versions, test failures, and your intent |
| Skill | A reusable procedure for a particular kind of job | Your team's process for investigating a failed deployment |
| Tool connection such as MCP | Access to an external capability or source | Reading a CI job, querying telemetry, or fetching an issue |
| RAG | Retrieving relevant material to inform an answer | Finding the applicable runbook instead of loading every runbook |
| Memory | Retaining useful information between tasks or sessions | A verified lesson about a recurring failure |
| Observability | Evidence about current system behavior | Metrics, logs, traces, deployment events, and service relationships |

These pieces can work together. A skill can tell the agent which telemetry to inspect; a tool connection can retrieve it; RAG can supply the runbook; memory can suggest a previous incident to compare. A stored lesson still needs checking against today's evidence. [Skills, MCP, RAG, and memory](https://www.youtube.com/watch?v=X4FVEEegCbk&t=132s).

Two terminology details matter. MCP connects an AI **application** to servers that expose capabilities; the model itself is not the entire host. RAG describes retrieving information to support generation, and can use more than a vector database. These are useful corrections to the video's simplified explanation. [MCP architecture](https://modelcontextprotocol.io/docs/learn/architecture), [retrieval options](https://docs.aws.amazon.com/bedrock/latest/userguide/knowledge-base.html).

## Follow one repeatable development workflow

### 1 Define a small outcome

Describe the behavior you want, why it matters, what must stay compatible, and how you will know it works. For a small bug, a reproduction and expected result may be enough. For a feature spanning services, write a short specification beside the code.

For example: “A user can request a reset link. It expires after 15 minutes, works once, and requesting another invalidates the earlier link.” That is a more useful target than “add password reset.” Keep refining the specification as you learn; freezing the entire project upfront recreates the weakness the spec-driven video warns about. [Specification loop](https://www.youtube.com/watch?v=GpZ5T51jE4U&t=175s).

### 2 Have the agent inspect before editing

Ask it to identify the relevant entry points, an existing implementation to follow, the tests, and any assumptions. Check that the change belongs in the intended layer. An endpoint that bypasses the service responsible for authorization can return the expected data while weakening the application. [Codebase and architectural context](https://www.youtube.com/watch?v=zAe-sau06io&t=66s).

Supply the relevant modules, interfaces, dependency and lock files, build instructions, and constraints. Your intention is especially important: the agent can discover a function, but cannot discover an unstated business requirement. [Agent inputs](https://www.youtube.com/watch?v=EkdIZXDnRK8&t=91s).

### 3 Agree on the plan and boundaries

For a meaningful change, ask for the files likely to change, the checks to run, and the main risks. For a tiny correction, this can be a few sentences.

My suggested default is to let the agent edit and test in an isolated branch or workspace. Treat adding dependencies, changing authentication, modifying infrastructure, migrating data, and deploying as explicit scope decisions. Give it access appropriate to the task. Broader reach makes both useful actions and mistakes more consequential. [Boundaries](https://www.youtube.com/watch?v=zAe-sau06io&t=332s), [agent security](https://www.youtube.com/watch?v=h4tHDFCPmQE&t=337s).

### 4 Implement a reviewable change

Ask the agent to reuse existing utilities and conventions. Keep unrelated refactoring and dependency upgrades separate from behavior changes unless the task requires them. Smaller changes make both human review and automated checks more informative. [Small changes](https://www.youtube.com/watch?v=iv32wI3MBpw&t=419s).

Subagents can help with independent investigation, testing, or a focused review. Use them when the separation has a clear purpose, and give each a bounded question and limited permissions. Their summaries can save context, but you should still be able to follow the evidence behind a claim. They are an option, not a requirement for every task. [Focused subagents](https://www.youtube.com/watch?v=h4tHDFCPmQE&t=286s).

### 5 Verify behavior and architectural fit

Run the checks appropriate to the change: a regression test, unit or integration tests, type checks, linting, and a build where relevant. Then compare the actual behavior and diff with the acceptance criteria. Check that the agent did not obtain a passing result by weakening the test or changing the requirement.

A successful build is useful evidence, but it does not establish that authorization, compatibility, and architecture are correct. Ask for what changed, the results of the checks, and what remains uncertain. [Verification beyond passing tests](https://www.youtube.com/watch?v=zAe-sau06io&t=278s), [evidence for outcomes](https://www.youtube.com/watch?v=bs1qPy_CWkM&t=243s).

### 6 Review with fresh evidence

Review the patch against the intended behavior. A separate AI session or model can provide another perspective because the implementation session may repeat its own assumptions. That second perspective supplements tests and human judgment; it is not a guarantee of independence or correctness. [Independent review](https://www.youtube.com/watch?v=iv32wI3MBpw&t=432s).

My suggested stopping rule is: the acceptance criteria are met, relevant checks pass, the change stays within scope, and remaining risks are visible to the reviewer. If the agent is repeating unsuccessful edits, stop and revisit its assumptions rather than letting the loop continue indefinitely.

### 7 Carry the task through delivery

When the task includes delivery, check configuration, infrastructure, documentation, monitoring, and downstream effects as well as application code. Preserve the intent and results when moving between the editor, terminal, CI, and deployment environment. The IDE versus CLI video describes this handoff problem; it does not require choosing one interface for everything. [Workflow handoffs](https://www.youtube.com/watch?v=5RtmQSKKQo8&t=319s).

For consequential changes, my suggested release record contains the artifact or commit, relevant check results, expected operational behavior, and a recovery plan. Check the observed outcome after deployment. A completed code edit and a successful production outcome are different milestones. [Coordinating the complete workflow](https://www.youtube.com/watch?v=bs1qPy_CWkM&t=145s).

## Keep context useful as a task grows

Give the agent enough context to find the right information without loading everything at once. A compact repository map and pointers to relevant code are often more useful than an entire repository dump. Retrieve details when they become relevant. [Focused context](https://www.youtube.com/watch?v=EkdIZXDnRK8&t=297s).

The context engineering video describes four ways a long session can go wrong:

| Failure | What it looks like | What to do |
| --- | --- | --- |
| Poisoning | An unverified assumption becomes a remembered fact | Validate it against code, documentation, or an experiment before retaining it |
| Distraction | The agent keeps repeating earlier work | Replace the long history with a concise current state and pointers to evidence |
| Confusion | Too many tools or irrelevant instructions obscure the right action | Make the task's tools and instructions easier to select |
| Clash | Old and corrected information coexist as if both are current | Mark the old claim as superseded and retain the correction |

These are diagnostic patterns, not a promise that every mistake comes from context length. The video also warns that repeated summaries can lose detail. Store important evidence in files that can be reread. [Failure modes and remedies](https://www.youtube.com/watch?v=BwXremQ-i6I&t=271s).

My recommended handoff contains the goal, current state, decisions and reasons, verified findings with references, checks already run, open questions, and the next action. Start a fresh session when the task changes or the history becomes misleading. Preserve this handoff so that a fresh session does not mean starting from zero. Use the [handoff template](workflow-templates.md).

## Choose autonomy deliberately

The loop video presents four patterns. Use them to ask who starts the work, who checks completion, and who reviews the result. These are separate decisions; an event can start a workflow that still requires human review. [Four loop patterns](https://www.youtube.com/watch?v=4LINhsEZEDI&t=90s).

| Pattern | Useful situation | Suggested initial use |
| --- | --- | --- |
| Interactive | Requirements are unclear or the change requires judgment | Explore the problem together and inspect intermediate results |
| Delegated | A bounded task has measurable acceptance criteria | Let the agent prepare a tested patch for your review |
| Scheduled | A recurring check becomes stale over time | Produce dependency or maintenance proposals on a schedule |
| Event triggered | A specific event provides the task context | Investigate a failed CI job or prepare a PR review when triggered |

Before automating a loop, define allowed actions, its success condition, and when it must stop unsuccessfully. My suggested controls include attempt and time limits, cancellation, visible failures, and escalation when evidence is missing. For repeated events, also prevent duplicate actions. These operational controls extend the video's loop model; they are not demonstrated as a complete implementation in the videos.

## Apply the same ideas to DevOps

Development asks what the system should do. Operations also asks what it is doing **now**. A runbook can explain the intended architecture, but it cannot establish today's cause of a slowdown. Combine it with relevant, recent telemetry and change history. [System knowledge and live context](https://www.youtube.com/watch?v=hvnPWgfmvyI&t=34s).

Consider this fictional incident: checkout latency increases shortly after a configuration update. The agent retrieves the checkout runbook, a trace showing extra time in a downstream call, queue metrics, and timeout logs for the same interval. Together these justify investigating the change; they do not prove it caused the incident. [Evidence and causation](https://www.youtube.com/watch?v=hvnPWgfmvyI&t=252s).

My suggested investigation output is:

1. **Observed facts:** the symptom, affected service, time window, and links to evidence.
2. **Possible explanations:** ranked hypotheses and what supports or challenges each one.
3. **Impact:** affected requests and dependencies, with uncertainty made explicit.
4. **Next check:** the smallest useful read-only query or comparison.
5. **Action proposal:** expected benefit, risk, and recovery steps for an operator to assess.

Start by using the agent to gather and organize evidence. Keep the choice of a production intervention with the responsible operator until you have explicitly established a suitable automation policy. That follows the operations video's emphasis on an operator who validates evidence and decides the action. [Operator control](https://www.youtube.com/watch?v=hvnPWgfmvyI&t=450s).

## Make repeatable work into skills

When a procedure repeatedly works, capture your actual process, including the corrections and unusual environment details. Good candidates include preparing a change for review, investigating a recurring CI failure, or producing a release checklist. A skill is most useful when it teaches the agent something specific it would otherwise have to guess. [Expertise and gotchas](https://www.youtube.com/watch?v=qYNs80FKIVc&t=245s).

Describe when to use the skill clearly. Keep its main instructions short and put details in referenced files. Use scripts for fragile, exact operations such as reconciling totals or validating a fixed schema. Inspect scripts before running them, and test their logic: predictable execution does not make a program bug-free. [Skill design](https://www.youtube.com/watch?v=qYNs80FKIVc&t=371s), [Agent Skills specification](https://agentskills.io/specification).

A practical distinction is to keep durable project conventions in the repository's instruction file, reusable task procedures in skills, and temporary investigation details in a task handoff. Review lessons before promoting them to durable instructions. This is my proposed organization for combining the context and skills advice.

## Treat security as part of the workflow

The sensitive-data video identifies five capabilities: visibility, classification, control over location and movement, access control, and audit evidence. Applied to daily work, know what data the agent can see, which approved services it can send data to, and what records its actions leave. Keep logs useful while limiting exposure of sensitive content. [Sensitive-data controls](https://www.youtube.com/watch?v=jnP9AgtX0qo&t=62s).

The agent-concepts video highlights a dangerous combination: access to sensitive information, untrusted external content, and the ability to send data out. Treat content from issues, web pages, and tool results as material to evaluate, rather than instructions that expand the task's authority. Use constrained execution environments and permissions appropriate to the work. [Prompt injection and sandboxes](https://www.youtube.com/watch?v=hTAWHgQI4xg&t=440s).

Supply-chain controls also apply to packages, container images, CI configuration, and installed skills. Track components with a software bill of materials, scan dependencies and secrets early, and retain evidence of how artifacts were built. A signature helps establish origin and integrity; it does not by itself establish that the contents are safe. [Supply-chain controls](https://www.youtube.com/watch?v=iv32wI3MBpw&t=374s).

## Build the habit gradually

Use this suggested four-week practice plan at a pace that fits your workload:

| Stage | Practice | What to learn |
| --- | --- | --- |
| Week 1 | Use one bounded bug or small feature to practice inspecting, planning, and checking | Which information and instructions prevent repeated corrections |
| Week 2 | Use a short, versioned spec and a session handoff | Whether acceptance criteria and continuity reduce rework |
| Week 3 | Capture one proven procedure and try a read-only operations investigation | Whether reusable expertise and live evidence improve the result |
| Week 4 | Try one scheduled or event-triggered task that produces a reviewable proposal | Whether the automation saves effort without creating hidden failures |

For comparable tasks, record total time including review and rework, the correctness of the result, repeated corrections, and tool cost. For investigations, record time to a useful evidence-backed hypothesis and false leads. Expand autonomy only when the observed results justify it. The videos' dramatic speed examples are anecdotes, so use your own results to judge improvement. [Capability claims in context](https://www.youtube.com/watch?v=hTAWHgQI4xg&t=56s).

For your next task, fill in the [task brief](workflow-templates.md), have the agent inspect the relevant code, agree on a small plan, and ask it to return the patch together with check results and open risks. That gives you one complete cycle to improve.
