# Local development and DevOps with Docker Sandboxes

Choose a terminal session with Claude Code or Codex, or use ThinkRail’s browser UI with its Pi agent. All three setups use a private clone for edits and a read-only mount for selected TrekAI 2nd Brain notes. You can fetch the agent’s finished branch while your current checkout stays open in your IDE. [Docker Git workflows](https://docs.docker.com/ai/sandboxes/workflows/git/) · [ThinkRail workspaces](https://thinkrail.ai/blog/thinkrail-workspaces/)

| Location | What belongs there |
| --- | --- |
| Mac | Your original checkout and unfinished edits, the private 2nd Brain, Docker’s credential store, and the browser. |
| Sandbox VM | Your chosen agent, its shell commands, the editable Git clone, task worktrees, dependencies, and test services. Worktrees in the same VM share tools, credentials, and services. |
| Read-only context | The agent reads selected 2nd Brain notes at `/context/second-brain`. Include only material suitable for the task and the model provider. |
| External systems | GCP IAM, SSH access, and GitHub workflow permissions still govern live operations. A command inside the VM can change a remote system when its identity has access. |

**Verification status, November 25, 2026.** The local project, 2nd Brain paths, and example source files were checked. This is a manual integration assembled from the vendors’ documented interfaces. The combined runtime still needs the smoke test below on a Mac with `sbx` installed. The [saved discussion](2026-11-25-local-agent-sandboxing.md) explains how this compares with agent-native sandboxing.

## Which sandbox fits the work?

For routine changes to a trusted project, native Codex or Claude Code with its Bash sandbox enabled is the simpler starting point. Put the task in a separate Git worktree if you have unfinished edits. For a first run of a new skill, installer, or agent extension, use a fresh Docker Sandbox with a sample repo and synthetic notes. Once it earns access to project data, use the private-clone and selected-context setup below. These are recommendations for this workflow based on the documented boundaries as of November 25, 2026.

| Approach | Benefit | Tradeoff |
| --- | --- | --- |
| **Codex CLI on the Mac** | Its usual trusted-repo setup applies OS-enforced workspace write restrictions and disables shell network access by default. You keep your local tools and avoid VM setup. | The active workspace is writable, and file reads can extend beyond it. Running in a separate worktree reduces accidental overwrites. Approving an out-of-sandbox command expands what it can reach. [Codex approvals and security](https://developers.openai.com/codex/agent-approvals-security) |
| **Claude Code on the Mac** | The default permission flow lets you review actions. Enable the optional Bash sandbox with `/sandbox` for OS-enforced filesystem and network limits on shell commands and their children. | The Bash sandbox is off by default. Even when enabled, file tools, hooks, and MCP servers have separate controls, and settings can permit unsandboxed retries. This matters when the thing you are evaluating is an extension or integration. [Claude Code sandbox scope](https://code.claude.com/docs/en/sandboxing) |
| **Local Docker Sandbox with a private clone** | The agent process and its in-VM tools run under a separate Linux kernel with a private Docker Engine. Try installers, services, and competing changes while your Mac checkout stays read-only. | You maintain a second toolchain, allocate local compute and disk, configure credentials and network rules, and fetch commits back. Linux may differ from your Mac or CI runner. Docker’s built-in Claude and Codex launchers skip native approval prompts by default. [Docker isolation](https://docs.docker.com/ai/sandboxes/security/isolation/) · [Git modes](https://docs.docker.com/ai/sandboxes/workflows/git/) · [Claude launcher](https://docs.docker.com/ai/sandboxes/agents/claude-code/) · [Codex launcher](https://docs.docker.com/ai/sandboxes/agents/codex/) |
| **A conventional dev container** | A versioned dev container can reproduce the team’s compiler, linters, and dependencies. A fresh clone in a container volume also keeps edits away from the Mac checkout. | Containers share the kernel of their Docker host, which is typically a Linux VM on macOS. You configure mounts, credentials, and egress. A writable project bind mount writes through immediately. Mounting the host Docker socket can give commands control of that Docker Engine. [Docker container model](https://docs.docker.com/engine/containers/run/) · [Docker daemon access](https://docs.docker.com/engine/security/) · [Claude dev container](https://code.claude.com/docs/en/devcontainer) |
| **Disposable remote VM or GitHub Codespace** | A fresh remote checkout keeps local drafts off the agent’s filesystem. A Codespace has its own VM and network. This works well when local compute is scarce or the team needs a repeatable remote Linux environment. | Source and selected notes move to another environment. Decide what the provider may receive and what repository token, cloud role, and forwarded ports the agent gets. Remote compute and storage can incur charges. [Codespaces security](https://docs.github.com/en/codespaces/reference/security-in-github-codespaces) · [Codespaces billing](https://docs.github.com/en/billing/concepts/product-billing/github-codespaces) |

**Three checks for a TrekAI ticket**

- **Could this overwrite my draft?** A ThinkRail or Git worktree gives normal edits a separate directory, but a process with host permission can still target the original path. Docker direct mode writes to the host checkout. Docker clone mode mounts that checkout read-only, including uncommitted files, and gives the agent a separate writable clone. For sensitive drafts that must also stay unreadable, use a mountless sandbox with a fresh clone of the required commits. [Git worktrees](https://git-scm.com/docs/git-worktree) · [Docker checkout options](https://docs.docker.com/ai/sandboxes/workflows/git/)
- **Could this disclose private notes?** A read-only mount protects integrity. The agent can still read the mounted notes and include them in a model request. Export only the material appropriate for the task and provider. Choose the same way for a local sandbox and a cloud VM. [Docker isolation boundaries](https://docs.docker.com/ai/sandboxes/security/)
- **Could this change a live service?** A Terraform apply, an Ansible run over SSH, or a workflow triggered by a Git push takes effect wherever its credentials work. Docker also supports forwarded SSH agents and host-side MCP services. For first trials, use fixtures. For integration tests, scope credentials to test state, a disposable target, or a test project, and check which workflow a push will trigger. [Docker security model](https://docs.docker.com/ai/sandboxes/security/) · [Google Cloud IAM](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control) · [GitHub Actions security](https://docs.github.com/en/actions/reference/security/secure-use)

## Claude Code, Codex, VS Code, or ThinkRail?

Pick the interface based on how you want to work. Claude Code and Codex are coding agents you can launch directly in Docker. VS Code is an editor you can attach to either sandbox. ThinkRail pairs its own interface with the Pi agent and organizes tasks into Git worktrees. Keep the private clone, read-only 2nd Brain mount, and scoped credentials the same when comparing them. [Docker editor integration](https://docs.docker.com/ai/sandboxes/integrations/vscode/) · [ThinkRail project](https://github.com/JetBrains/thinkrail)

| Interface | Pros for development and DevOps | Cons and tradeoffs |
| --- | --- | --- |
| **Claude Code CLI** | Docker has a built-in launcher. For an unfamiliar Ansible role, ask Claude to trace the inventory, handlers, and affected hosts. Select Plan Mode when you want a proposed edit sequence before it changes files. | A terminal session gives you less of a visual overview of several task branches. Parallel sessions need separate worktrees or clones to avoid editing the same files. Docker’s default Claude launch skips native permission prompts, so choose the interaction mode deliberately. [Claude workflows](https://code.claude.com/docs/en/common-workflows) · [Docker’s Claude launcher](https://docs.docker.com/ai/sandboxes/agents/claude-code/) |
| **Codex CLI** | Docker also has a built-in Codex launcher. Use `/review` on a Terraform or GitHub Actions diff before handing it back. Use `codex exec` for a repeatable task such as reviewing changes against the same instructions. | Review findings still need verification against actual plan output or a test workflow. For hands-on debugging and cross-file navigation, you may want an editor attached. Docker’s default Codex launch bypasses its inner approvals and sandbox. [Codex CLI](https://developers.openai.com/codex/cli/features/) · [Docker’s Codex launcher](https://docs.docker.com/ai/sandboxes/agents/codex/) |
| **VS Code over Remote – SSH** | Keep the editor on your Mac and open the sandbox clone. Inspect a YAML diff, set a breakpoint in a script, or run tests in the remote terminal while Claude Code or Codex works in that same VM. This suits tickets where you expect to edit alongside the agent. | Requires SSH setup, the Remote – SSH extension, and any needed remote debugging tools. A local VS Code window still targets the Mac. Check the remote hostname and folder before editing. You and the agent can overwrite each other’s edits if you share a worktree. [Docker’s VS Code guide](https://docs.docker.com/ai/sandboxes/integrations/vscode/) · [VS Code Remote – SSH](https://code.visualstudio.com/docs/remote/ssh) |
| **ThinkRail with Pi inside Docker** | Each side workspace brings together a task branch, chat, terminal, and diff. You can keep a Terraform provider upgrade separate from an Ansible role change, compare the results, and merge each independently. | This guide’s setup requires installing ThinkRail inside the VM, configuring Pi’s provider, and publishing the browser UI. Worktrees separate files, but agents in one VM share tools, services, and available credentials. An unfamiliar skill warrants its own sandbox. [ThinkRail features](https://github.com/JetBrains/thinkrail) · [Docker parallel tasks](https://docs.docker.com/ai/sandboxes/workflows/git/#parallel-tasks) |

**For a single ticket**, start with the CLI you already use. Attach VS Code to the named sandbox when you want breakpoints, file navigation, or manual edits. **For several concurrent tickets**, ThinkRail earns its extra setup when switching among chats, branches, and diffs becomes the time-consuming part. In either workflow, Docker’s mounts and the credentials available to the agent determine which files and systems it can affect. [Docker security model](https://docs.docker.com/ai/sandboxes/security/)

### Worktree defaults and how closely VS Code matches ThinkRail

All four tools can work in a linked Git worktree. Each worktree has its own checked-out files and staging area while sharing repository history. Opening a repository already gives you its primary working tree. The choice below is whether a task gets an **additional** one. [Git worktrees](https://git-scm.com/docs/git-worktree)

| Where you start | Does a task get a new worktree? | Setup effort |
| --- | --- | --- |
| ThinkRail | Creating a side workspace gives it a worktree, branch, and chat. ThinkRail also lets you work directly in the project folder. | One workspace action per task once ThinkRail is installed. Review its diff and PR from that workspace. [ThinkRail workspaces](https://github.com/JetBrains/thinkrail) |
| Claude Code CLI | A plain launch works in the current checkout. Use `claude --worktree tf-check` to request a separate checkout for that session. | One flag per task. The installed Claude Code 2.1.329 also accepts `-w`. [Claude Code workflows](https://code.claude.com/docs/en/common-workflows) |
| Codex CLI or desktop | The CLI supports `codex --worktree` for a new local managed worktree. In the desktop app, choose **Worktree** when starting the chat. | One flag or one UI choice. The installed Codex CLI 0.172.0 advertises the flag. Confirm the version inside the VM if using Docker’s launcher. [Codex CLI reference](https://learn.chatgpt.com/docs/cli/reference) · [Codex environments](https://learn.chatgpt.com/docs/environments/modes) |
| VS Code editor | Opening a folder uses that checkout. In **Source Control Repositories → … → Worktrees → Create Worktree**, choose a branch and folder, then open the worktree in a window. | Built-in Git support handles this without an extra worktree extension or settings file. Launch your chosen CLI from that window’s terminal. [VS Code Git worktrees](https://code.visualstudio.com/docs/sourcecontrol/branches-worktrees) |
| VS Code Agents window | For a supported Git session with at least one commit, **New Worktree** is initially selected by default (`sessions.useWorktree` is `true`). VS Code remembers a previous isolation choice, so check the selector. **Branch** edits the selected checkout. | Open **Chat: Open Agents window**, select the project and an available signed-in agent, and start one **New Worktree** session per task. The sessions list and diff review give you much of ThinkRail’s parallel-task workflow. Codex in this window requires enabling the experimental Codex Agent Host integration and permitted account access. [Agents window](https://code.visualstudio.com/docs/agents/run/agents-window) · [Settings defaults](https://code.visualstudio.com/docs/agents/reference/ai-settings) · [Agent integrations](https://code.visualstudio.com/docs/agents/run/agent-harnesses) |

**For the Docker setup in this guide**, connect VS Code to the sandbox with Remote – SSH and open the private clone. Create worktrees there using the remote window’s Git controls or terminal, then run Claude Code or Codex in the chosen worktree. If VS Code already created it, launch the CLI normally to use that directory. Docker’s `--clone` creates one independent clone per sandbox. A worktree per concurrent task is a separate choice. VS Code’s dedicated Dev Container agent-session mode currently works directly in its container workspace and omits the **New Worktree** selector. [Docker VS Code integration](https://docs.docker.com/ai/sandboxes/integrations/vscode/) · [Docker Git workflows](https://docs.docker.com/ai/sandboxes/workflows/git/) · [VS Code session isolation](https://code.visualstudio.com/docs/agents/run/agents-window)

## 1. Prepare Docker and choose the project on your Mac

Docker’s local macOS runtime requires Apple silicon and macOS 14 or later. It uses the `sbx` CLI. Install it once with Homebrew, sign in to Docker, and confirm the version. [Docker installation](https://docs.docker.com/ai/sandboxes/install/)

```sh
brew trust docker/tap
brew install docker/tap/sbx
sbx login
sbx version
```

Run the remaining **Mac** commands in the same terminal. The primary project below is the roadmap repo, useful for a documentation trial. For application or infrastructure changes, set `PROJECT_REPO` to the main checkout of the repo that owns the code. Choose a new sandbox name for each independent experiment. Clone mode starts from the checked-out commit. Uncommitted edits stay in the original checkout, which Docker also exposes read-only inside the VM. For an unfamiliar skill’s first run, choose a sample project with synthetic context. [Workspace modes](https://docs.docker.com/ai/sandboxes/usage/#git-workspace-modes)

```sh
PROJECT_REPO="$HOME/Documents/trekai/trekai-platform-roadmap"
BRAIN_REPO="$HOME/Documents/trekai/sm-trekai-infrastructure-and-product-review"
LAB_NAME=thinkrail-trekai-lab
git -C "$PROJECT_REPO" status --short --branch
git -C "$BRAIN_REPO" rev-parse --show-toplevel
```

## 2. Select the 2nd Brain context on your Mac

The 2nd Brain contains private security findings, IAM inventories, and internal documentation. For a Terraform-process ticket, the two paths below supply a dated change-process answer and an environment explanation. Read the files locally first. Exporting specific committed files keeps working drafts, Git history, and unrelated audit data outside the context mount. Keep the temporary directory available for the life of this sandbox.

```sh
BRAIN_CONTEXT="$(mktemp -d)"
BRAIN_REV="$(git -C "$BRAIN_REPO" rev-parse HEAD)"
PROCESS_NOTE=trekai-questions/cross-system/2026-11-09-tl-terraform-change-deployment-process.md
ENV_NOTE=trekai-how-it-works/architecture/tl-terraform-environments.md
git -C "$BRAIN_REPO" archive -o "$BRAIN_CONTEXT/notes.tar" "$BRAIN_REV" -- "$PROCESS_NOTE" "$ENV_NOTE" &&
  tar -xf "$BRAIN_CONTEXT/notes.tar" -C "$BRAIN_CONTEXT" &&
  rm "$BRAIN_CONTEXT/notes.tar" &&
  printf '%s\n' "$BRAIN_REV" > "$BRAIN_CONTEXT/SOURCE_COMMIT"
```

For other tickets, select the relevant source paths. When the task and provider are authorized for the **entire private 2nd Brain**, set `BRAIN_CONTEXT="$BRAIN_REPO"` instead of exporting. That choice exposes the whole local checkout, including Git history, ignored files, and uncommitted material. Both options use the same read-only mount. A read-only mount prevents edits but permits reading, copying, and inclusion in model requests. [Docker workspace mounts](https://docs.docker.com/ai/sandboxes/usage/#multiple-workspaces)

## Run Claude Code or Codex directly

After steps 1 and 2, choose one launch block below and run it on your Mac. Docker starts the CLI inside its own Linux VM. You interact with it in the terminal, and the agent edits and tests the private clone. Each block sets `LAB_NAME` for the review commands in step 6. For ThinkRail’s worktree UI, continue with step 3 instead. [Claude Code launcher](https://docs.docker.com/ai/sandboxes/agents/claude-code/) · [Codex launcher](https://docs.docker.com/ai/sandboxes/agents/codex/)

**Claude Code.** For a Claude subscription, use `/login` in the launched session if prompted. For an Anthropic API key, run `sbx secret set anthropic` on the Mac before launch. [Claude authentication](https://docs.docker.com/ai/sandboxes/agents/claude-code/#authentication)

```sh
LAB_NAME=claude-dev
sbx run --name "$LAB_NAME" --clone --skills=off --static-mcp none \
  claude "$PROJECT_REPO" "$BRAIN_CONTEXT:/context/second-brain:ro"
```

**Codex.** Docker prompts for host-side sign-in on first launch if it has no stored OpenAI credential. To authenticate ahead of time, run `sbx secret set openai --oauth` on the Mac, or use `sbx secret set openai` for an API key. [Codex authentication](https://docs.docker.com/ai/sandboxes/agents/codex/#authentication)

```sh
LAB_NAME=codex-dev
sbx run --name "$LAB_NAME" --clone --skills=off --static-mcp none \
  codex "$PROJECT_REPO" "$BRAIN_CONTEXT:/context/second-brain:ro"
```

**Permission defaults.** Docker’s built-in Claude launcher starts with `--dangerously-skip-permissions`. Its Codex launcher starts with `--dangerously-bypass-approvals-and-sandbox`. These defaults skip the agents’ own approval prompts and give Docker’s VM responsibility for isolation. The mounts, network policy, and credentials you grant determine what a command can affect. For example, Terraform can test module logic with mocked providers. A live apply can change real infrastructure when its identity has write access. Keep the first trial credential-free for cloud tooling. [Claude startup defaults](https://docs.docker.com/ai/sandboxes/agents/claude-code/#default-startup-command) · [Codex startup defaults](https://docs.docker.com/ai/sandboxes/agents/codex/#default-startup-command)

**First task.** Ask the agent to report its checkout and branch, confirm the context mount is read-only with `findmnt -T /context/second-brain`, and cite one dated note before editing. Ask it to create a task branch and commit the intended changes there. If you launch both agents with the names above, each gets a separate clone. Follow steps 5 and 6 for testing and review. The host remotes are `sandbox-claude-dev` and `sandbox-codex-dev` respectively. [Docker Git handoff](https://docs.docker.com/ai/sandboxes/workflows/git/#single-task)

## 3. Create the ThinkRail sandbox on your Mac

The **first path** is the project to clone. The **second path** is the reference mount. The UI port binds to loopback on the Mac. Disable the shared skills store and host MCP tools for this trial. Review effective network rules and available credentials, including any globally configured services, before putting a new skill in the sandbox. [Docker CLI options](https://docs.docker.com/reference/cli/sbx/create/) · [Docker security model](https://docs.docker.com/ai/sandboxes/security/)

```sh
sbx create --name "$LAB_NAME" --clone --skills=off --static-mcp none \
  --publish 127.0.0.1:24242:24242 \
  shell "$PROJECT_REPO" "$BRAIN_CONTEXT:/context/second-brain:ro"
sbx policy ls "$LAB_NAME"
sbx inspect "$LAB_NAME"
```

**Model access.** This example uses Anthropic as the model provider. On your Mac, register the API key for this sandbox through the interactive secret prompt. Give the installer access to the GitHub release hosts and the agent access to its model endpoint as needed under your network policy. Keep personal cloud logins, production SSH identities, and GitHub write tokens outside this trial. Docker can forward the host SSH agent, so verify the identity check in the next step. [Docker credentials](https://docs.docker.com/ai/sandboxes/configuration/credentials/) · [Network rules](https://docs.docker.com/reference/cli/sbx/policy/allow/network/)

```sh
sbx secret set anthropic --sandbox "$LAB_NAME"
sbx policy allow network --sandbox "$LAB_NAME" api.anthropic.com
sbx policy allow network --sandbox "$LAB_NAME" --method GET,HEAD \
  'raw.githubusercontent.com,github.com,api.github.com,release-assets.githubusercontent.com'
sbx run --name "$LAB_NAME"
```

## 4. Verify the mounts and launch ThinkRail inside the VM

Run the following **inside the sandbox shell**. The first check should print the editable project root. Both mount checks should include the standalone option `ro`. The example note should report readable. If you selected other files, substitute one of those paths. If the mounts differ, fix the setup before starting the agent. If `ssh-add -l` lists a production identity, resolve SSH forwarding before continuing with a skill trial. These checks avoid test writes to either source repo.

```sh
git rev-parse --show-toplevel
findmnt -T /run/sandbox/source -o TARGET,OPTIONS
findmnt -T /context/second-brain -o TARGET,OPTIONS
test -r /context/second-brain/trekai-questions/cross-system/2026-11-09-tl-terraform-change-deployment-process.md && echo "Context readable"
ssh-add -l
```

Install the Linux CLI **in the VM**. The official installer fetches the release for the VM architecture and checks its checksum. In this shell setup, a placeholder lets the client select the Anthropic provider while Docker’s proxy supplies the real key. [ThinkRail installer](https://github.com/JetBrains/thinkrail/blob/main/install.sh) · [Docker shell credentials](https://docs.docker.com/ai/sandboxes/configuration/credentials/#custom-templates-and-placeholder-values)

```sh
curl -fL https://raw.githubusercontent.com/JetBrains/thinkrail/main/install.sh -o /tmp/thinkrail-install.sh &&
  bash /tmp/thinkrail-install.sh --channel stable --no-modify-path
export PATH="$HOME/.local/bin:$PATH"
export ANTHROPIC_API_KEY=proxy-managed
thinkrail --version
thinkrail --host 0.0.0.0 --port 24242 --no-open .
```

On the Mac, open `http://127.0.0.1:24242`. Select the Anthropic model in ThinkRail and create a **side workspace** for the task. Select the sandbox clone as the project. For a connection failure, check the port ThinkRail printed and run `sbx port ls "$LAB_NAME"` in the Mac terminal where the variables are set. For authentication or download failures, check the sandbox’s scoped secret and the exact denied destination before changing network rules. [ThinkRail CLI flags](https://github.com/JetBrains/thinkrail/blob/main/apps/cli/SPEC.md) · [Docker port publishing](https://docs.docker.com/ai/sandboxes/usage/#publish-ports)

**First chat.** Start with a read-only request. This checks the UI, provider, active worktree, and context mount together.

> Print your working directory and current Git branch. Read the Terraform change-process note under `/context/second-brain/trekai-questions/cross-system/`. Give its relative path, evidence date, one supported claim, and one thing the note leaves unverified. Leave files unchanged.

The answer should identify the side workspace branch and cite the supplied note. It should distinguish the dated evidence from current runtime behavior. For implementation, give the agent the ticket, target repo, product and environment, intended file scope, and acceptance test. Ask it to flag any difference between the notes and the target repo. Keep Trek Learning (Hub/LMS) and TrekCAP/TrekFinder source-access boundaries intact.

## 5. Use it on a ticket

| Ticket | Work inside the sandbox | Evidence to review |
| --- | --- | --- |
| Application or script fix | Reproduce with a fixture, fix the issue in the task worktree, run the targeted test and affected suite. Give a cleanup script a disposable directory containing files to keep and files to remove. | Before-and-after test results, surviving fixture files, and the branch diff. |
| Terraform module or provider change | Check formatting, run `terraform init -backend=false` and `terraform validate`, then exercise module logic with mocked providers where appropriate. For a live plan, select test state and a test project with scoped credentials. | Module and lock-file diff, validation output, and a separate test-project plan when applicable. Keep any state and sensitive plan output private. [Terraform validation](https://developer.hashicorp.com/terraform/cli/commands/validate) · [Provider mocking](https://developer.hashicorp.com/terraform/language/tests/mocking) |
| Ansible role | Use a test inventory and disposable target. Run the role twice and inspect unexpected changes on the second run. Some tasks explicitly override check mode. | Target inventory, outcome of both runs, and a redacted diff. [Ansible check mode](https://docs.ansible.com/projects/ansible/latest/playbook_guide/playbooks_checkmode.html) |
| Google Cloud inventory script | Start with fixture JSON. For API coverage, use a dedicated test identity with the required read permissions in a test project and pass the project explicitly. | Expected resource selection and permission behavior. IAM, including inherited roles, determines effective access. [Google Cloud IAM](https://docs.cloud.google.com/iam/docs/resource-hierarchy-access-control) |
| GitHub Actions change | Check the workflow with `actionlint` and exercise its scripts in the VM. Inspect workflow triggers before pushing. Exercise runner events, token permissions, and cloud authentication in a test repo or environment. | Local lint and test output plus the test workflow run. Credentials available to the remote runner determine real effects. [actionlint](https://github.com/rhysd/actionlint) · [GitHub Actions security](https://docs.github.com/en/actions/reference/security/secure-use) |

For example, give a Terraform agent the two selected 2nd Brain notes and the infrastructure repo that owns the module. Ask for a provider upgrade on a side branch, validation against a fixture, and a summary of lock-file changes. Review the diff and test output before choosing whether to run a live plan. Keep production applies and deployments in the project’s established delivery process.

## 6. Bring back a branch without switching your Mac checkout

Have the agent commit the intended files on its task branch and report the branch name, commit ID, and checks run. On your Mac, while the sandbox is running, use its launch-time `LAB_NAME` and substitute the reported branch name below. Check that the fetched commit matches the handoff, then keep a local review branch before removing the sandbox. These commands leave unfinished files in your current checkout in place. [Docker Git handoff](https://docs.docker.com/ai/sandboxes/workflows/git/#single-task)

```sh
TASK_BRANCH=example-task  # replace with the reported branch
LAB_REMOTE="sandbox-$LAB_NAME"
git -C "$PROJECT_REPO" fetch "$LAB_REMOTE"
git -C "$PROJECT_REPO" log -1 --oneline "$LAB_REMOTE/$TASK_BRANCH"
git -C "$PROJECT_REPO" diff HEAD..."$LAB_REMOTE/$TASK_BRANCH"
git -C "$PROJECT_REPO" branch "review/$TASK_BRANCH" "$LAB_REMOTE/$TASK_BRANCH"
git -C "$PROJECT_REPO" status --short --branch
```

To resume later, stop with `sbx stop "$LAB_NAME"` and reconnect with `sbx run --name "$LAB_NAME"`. To discard the VM, first confirm all wanted commits have a local branch. Then use `sbx rm "$LAB_NAME"`. Removal discards the VM’s worktrees, tools, and uncommitted files. If you exported the two-note bundle, remove that temporary copy after retiring the sandbox. [Docker sandbox lifecycle](https://docs.docker.com/ai/sandboxes/usage/)
