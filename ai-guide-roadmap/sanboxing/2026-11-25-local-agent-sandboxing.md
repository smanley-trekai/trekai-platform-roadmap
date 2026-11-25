# Local AI agent sandboxing

November 25, 2026

For installation, read-only 2nd Brain context, a first task, and branch handoff, follow the [ThinkRail and Docker setup guide](README.md).

## Default sandboxing in local coding agents

**User**

question, by default does codex, claude code and other popular ai agent use some kind of sandboxing to run code safely ?

**Codex**

**For local shell commands, Codex enables sandboxing by default. Claude Code and Gemini CLI make it opt-in.** An approval prompt controls whether a command can start. A sandbox limits what that command and the processes it launches can do once they’re running.

| Local agent | Default behavior |
|---|---|
| **Codex** | Uses an OS-enforced sandbox. In a trusted repository, commands can typically write to the workspace and temporary directories. Shell network access is off by default. Codex can also start in read-only mode. [OpenAI docs](https://developers.openai.com/codex/agent-approvals-security) |
| **Claude Code** | The shell sandbox is **off by default**. Permission prompts still govern actions that need approval. Run `/sandbox` to inspect or enable filesystem and network restrictions for shell commands. [Anthropic docs](https://code.claude.com/docs/en/sandboxing) |
| **Gemini CLI** | Sandboxing is **opt-in**. Start it with `gemini --sandbox` or enable it in settings. The restrictions depend on the selected profile. [Google docs](https://geminicli.com/docs/cli/sandbox/) |

**In this Codex session, `workspace-write` is active.** A script I run can modify ordinary files in this repository and write to designated temporary directories. Reads can extend outside the repository, and shell network access is restricted. So if a script accidentally overwrites a project file, the sandbox permits that write.

## What Docker Sandboxes adds on a local machine

**User**

okay then, what would be the benefit of adding actual sandboxing ? like this in local machine? https://www.docker.com/products/docker-sandboxes/

**Codex**

**The benefit is that you can give the agent more freedom while exposing less of your Mac.** Codex already uses an OS-enforced sandbox. In this session, it limits where commands can write and restricts network access, but commands can still read files outside the repository. Docker Sandboxes adds a separate Linux microVM on your Mac, with its own filesystem and Docker Engine. You choose which host directories to share. [Codex security model](https://developers.openai.com/codex/agent-approvals-security) · [Docker isolation model](https://docs.docker.com/ai/sandboxes/security/isolation/)

Imagine asking an agent to **install dependencies and run the tests in an unfamiliar repo**. A dependency’s install script runs with the permissions of the process that launched it. Inside Docker’s sandbox, that script can install Linux packages or start containers using the VM’s private Docker Engine. Your other checkouts, personal documents, and host Docker daemon stay outside its reach unless you explicitly share access to those files. You can discard the VM and its installed tools afterward. [Docker security defaults](https://docs.docker.com/ai/sandboxes/security/defaults/)

**Protecting your working copy is a separate choice.** By default, Docker shares the current project read-write. If the agent overwrites a presentation, the change appears on your Mac immediately. Docker’s `--clone` mode gives the agent a separate Git checkout inside the VM, so you can review its commits before bringing them back. [Docker workspace modes](https://docs.docker.com/ai/sandboxes/usage/#git-workspace-modes)

For **this roadmap repo**, I’d use the existing Codex sandbox for routine Markdown and slide edits. I’d choose Docker when running unfamiliar scripts, installing toolchains, or letting an agent build and test unattended. If your main concern is an agent overwriting local work, **clone mode** is the feature that directly addresses it.

## Trying new skills and DevOps tools

**User**

the work is related to software development and devops, trying new skills, and maybe tools so main concern is security and safety plus not overwriting local work

**Codex**

For a first run of an unfamiliar skill or DevOps tool, I’d use a fresh local Docker Sandbox with a small sample repository. Install the skill inside the VM and use `--skills=off` when creating it to keep the experiment out of the shared skills store. Allow outbound access only to the services the test needs. [Docker sandbox defaults](https://docs.docker.com/ai/sandboxes/security/defaults/)

When the test needs your project, use `--clone` from the main Git checkout. The agent edits a private clone, and your original working tree, including uncommitted work, is mounted read-only. Review the diff and bring back the commits you want. Files such as a local `.env` in the original checkout can still be read. Use a sanitized sample if those files are sensitive. [Docker Git workspace modes](https://docs.docker.com/ai/sandboxes/usage/#git-workspace-modes)

For DevOps, scope the account as well as the machine. A sandboxed tool with a production Kubernetes credential can still change production if it can reach the API. Use a disposable cluster or test account. Check which SSH identities and connected tools the sandbox can use, since a forwarded SSH agent or host-side integration can authorize actions outside the VM. [Docker security model](https://docs.docker.com/ai/sandboxes/security/)

## Docker clone mode and ThinkRail worktrees

**User**

about overwriting local work, does it use git worktree? if it does is there a benefit in using thinkrail from jetbrains ide?

**Codex**

Docker Sandboxes’ `--clone` creates an independent Git clone inside the VM. Your original checkout is mounted read-only. ThinkRail, a standalone agent IDE from JetBrains, uses a linked Git worktree when you create a side workspace. Each task gets its own branch and directory, so you can leave unfinished edits open in IntelliJ, inspect the agent’s changes, and merge them when ready. [Docker Git workflows](https://docs.docker.com/ai/sandboxes/workflows/git/) · [ThinkRail workspaces](https://thinkrail.ai/blog/thinkrail-workspaces/)

A worktree keeps routine edits separate. A command that explicitly targets your original checkout can still write there if its process has permission. For unfamiliar skills or DevOps tools, I’d use Docker clone mode. For trusted parallel tasks, ThinkRail adds convenient worktree creation, diff review, and pull request tracking. If you want both VM isolation and parallel branches, create a worktree per task inside the sandbox’s clone. [Git worktrees](https://git-scm.com/docs/git-worktree) · [ThinkRail features](https://github.com/JetBrains/thinkrail) · [Docker parallel tasks](https://docs.docker.com/ai/sandboxes/workflows/git/#parallel-tasks)

## Running ThinkRail inside Docker Sandboxes

**User**

okay is it possible to make thinkrail and docker sandbox work together?

**Codex**

Yes. The documented pieces support a manual setup: run the Linux ThinkRail CLI and its Pi agent inside a Docker shell sandbox, and open ThinkRail’s browser UI on your Mac. ThinkRail creates its worktrees inside the VM. This combination was checked against the documentation but was not run end to end here. [ThinkRail CLI](https://github.com/JetBrains/thinkrail/blob/main/apps/cli/SPEC.md) · [Docker shell sandbox](https://docs.docker.com/ai/sandboxes/agents/shell/)

For a first test, create a sandbox with no host workspace mounted. Run these on your Mac:

```sh
sbx create --name thinkrail-lab --skills=off --publish 127.0.0.1:24242:24242 shell
sbx run --name thinkrail-lab
```

Inside the sandbox, install ThinkRail’s Linux CLI, configure access to your model provider, and enter a sample Git repository. Start `thinkrail --host 0.0.0.0 --port 24242 --no-open .` there, then open `http://127.0.0.1:24242` on your Mac. Docker publishes the UI only on the Mac’s loopback address. Keep production credentials and host tools out of the trial. [ThinkRail installation](https://github.com/JetBrains/thinkrail) · [Docker port publishing](https://docs.docker.com/ai/sandboxes/usage/#publish-ports) · [Pi sandbox authentication](https://docs.pi.dev/latest/containerization)

For work that needs the local project, create a separate shell sandbox with `--clone` from the main checkout and open its private clone in ThinkRail. Docker mounts the original checkout read-only. Fetch the agent’s commits to review them before merging. [Docker Git workflows](https://docs.docker.com/ai/sandboxes/workflows/git/)

## Using the setup for development and DevOps

**User**

for this type of setup, how would it help software development and devops work? where you deal with terraform, ansible, scripts, google cloud commands, github actions etc

**Codex**

The benefit is that an agent can take a change from an idea to a tested commit while you keep working in your original checkout. ThinkRail gives each task its own branch and diff. Docker gives the tools a disposable Linux environment. Remote permissions are a separate decision: a cloud command inside the VM can still change any resource its credentials authorize. [Docker Git workflows](https://docs.docker.com/ai/sandboxes/workflows/git/) · [Google Cloud IAM](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control)

| Work | What I’d use the sandbox for | Where the real effect happens |
|---|---|---|
| Terraform | Change a module, run `terraform init -backend=false` and `terraform validate`, then test module logic with mocked providers. | A live plan reads real state and provider APIs. Use separate test state and a test project for integration runs. [Validation](https://developer.hashicorp.com/terraform/cli/commands/validate) · [Provider mocking](https://developer.hashicorp.com/terraform/language/tests/mocking) |
| Ansible | Point a test inventory at a disposable Linux target. Apply the role twice and check whether the second run reports unexpected changes. | The inventory and SSH identity determine which machines a playbook can change. A task can override `--check` with `check_mode: false`. [Ansible check mode](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_checkmode.html) |
| Scripts and application code | Install an unfamiliar dependency, run the test suite, or run a cleanup script against seeded files and inspect exactly what it removed. | In clone mode, file edits land in the private checkout. Separate worktrees still share the VM’s tools and services. Use a fresh sandbox for an unfamiliar skill. [Docker Git workflows](https://docs.docker.com/ai/sandboxes/workflows/git/) |
| Google Cloud CLI | Exercise an inventory script against a test project using an identity with only the required read permissions. | `--project` selects a target. IAM determines what the identity can actually do, including permissions inherited from folders or the organization. [gcloud configurations](https://docs.cloud.google.com/sdk/gcloud/reference/topic/configurations) · [IAM inheritance](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control) |
| GitHub Actions | Run `actionlint` and execute the workflow’s build or test scripts locally before pushing. | A push or pull request can start a real workflow. Its runner, token permissions, secrets, and cloud identity govern that run. Test deployment behavior in a test repo or environment with scoped credentials. [actionlint](https://github.com/rhysd/actionlint) · [GitHub Actions security](https://docs.github.com/en/actions/reference/security/secure-use) |

For example, to try a skill that upgrades a Terraform provider, give it a fresh sandbox with a sample module and no cloud credentials. Have it update the version constraint and lock file, run validation and mocked tests, and show you the diff. If the change looks right, run a real plan against test state in a test project. You get a reviewable commit and a plan before deciding whether to take the change through your normal release process.

## Claude Code and Codex in Docker Sandboxes

**User**

question - how will claude code or codex work with docker sandbox?

**Codex**

Both have built-in Docker launchers. You interact with the CLI in your Mac terminal while commands, edits, dependency installs, and tests run in the VM. The [direct launch instructions](README.md#run-claude-code-or-codex-directly) use separate named sandboxes, a private clone per agent, and selected 2nd Brain notes mounted read-only. ThinkRail provides an optional browser-based workflow with Pi.

Claude supports subscription sign-in or an Anthropic API key. Codex supports host-side OpenAI OAuth or an API key. By default, Docker launches Claude with its permission prompts skipped and Codex with its inner sandbox and approvals bypassed. Docker enforces the outer boundary. A DevOps command can still affect any external resource its credentials authorize. [Claude in Docker](https://docs.docker.com/ai/sandboxes/agents/claude-code/) · [Codex in Docker](https://docs.docker.com/ai/sandboxes/agents/codex/)
