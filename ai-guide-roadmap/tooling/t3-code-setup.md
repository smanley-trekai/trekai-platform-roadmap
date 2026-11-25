# Set up T3 Code

Documentation checked **2026-11-25**. This is a setup guide, not a record of an installation performed here. The commands and UI labels below follow T3 Code's current documentation; recheck the linked sources if your version differs.

Return to the [tool comparison](README.md).

## What you are setting up

T3 Code is a free, MIT-licensed control interface around coding agents. The desktop app and web/mobile clients connect to the machine running the agents. Model access and billing remain with the provider you use.

For a first trial, use the desktop app on your Mac, one provider, and one small task. Add parallel worktrees after the first task works. The desktop download is available for both Apple Silicon and Intel Macs; the standalone `t3` executable currently has no Intel Mac build. See [installation requirements](https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md).

## 1. Check prerequisites

- A local Git repository you can work on, with a known starting branch/commit.
- Working Git on the machine that will run the agents.
- At least one supported provider, with an eligible subscription or API access. Provider installation/login belongs on that same machine, including when you connect from another device.
- For the Homebrew route, an existing working Homebrew installation. Use the direct download if you do not have Homebrew.

In Terminal, check Git:

```sh
git --version
```

On macOS, an `xcrun` error about `/Library/Developer/CommandLineTools` means the developer-tools installation needs repair before relying on Git/worktrees. On a machine without those tools, `xcode-select --install` starts Apple's installer; if an existing installation is broken, repair or reinstall it through your normal Mac support process. Rerun `git --version` afterwards. This error was observed in the documentation session; no repair was performed.

## 2. Install the desktop app

### macOS: Homebrew

```sh
brew install --cask t3-code
```

Launch **T3 Code** from Applications.

### macOS: direct download

1. Open the [official download page](https://t3.codes/download).
2. Select the Apple Silicon arm64 or Intel x64 macOS build that matches your Mac.
3. Open the downloaded disk image, copy the app to Applications, and launch it.

### Other platforms

| Platform | Supported installation route |
| --- | --- |
| Windows | `winget install T3Tools.T3Code`, or the official `.exe` download |
| Debian / Ubuntu | Download the `.deb` matching your architecture from the official releases |
| Other Linux | Use the matching AppImage from the official releases |

The [official installation guide](https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md) also covers Scoop, Arch, Nix, WSL, and nightly builds. A desktop release does not require building the T3 repository from source.

## 3. Connect an agent provider

1. Open **Settings → Providers**.
2. Select the environment/machine where this project will run.
3. Enable the provider you want and follow its setup flow.
4. Complete sign-in and check that the provider is ready before sending a task.

| Provider | First setup route |
| --- | --- |
| Codex | Use T3's **Connect with ChatGPT** flow, or an installed and authenticated Codex CLI. Follow [T3's Codex setup](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-codex.md). |
| Claude Code | Install Claude Code through its official installer, authenticate it on this machine, then enable Claude in T3. Follow [T3's Claude setup](https://github.com/pingdotgg/t3code/blob/main/docs/user/providers-claude.md). |
| Another agent | Follow the matching entry in [T3's provider setup table](https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md#providers). |

Existing provider access still has its own billing, quotas, and terms. Add a second provider after the first works. Do not put credentials in repository files or prompts; use the provider's sign-in flow or T3's sensitive-value settings where applicable.

If an installed CLI is not detected, check that it is available on the agent machine's `PATH`, or set **Binary path** in that provider's settings. A CLI installed only on your laptop will not satisfy a remote server's requirements. T3's managed Codex/Antigravity runtimes have their own setup path and need not be on `PATH`.

## 4. Choose permissions for the first task

The checked documentation says the initial default is **Full access**. For this first supervised trial, select **Supervised** explicitly in the composer or set **Settings → Threads → New threads → Permissions**. Projects can override environment defaults, so inspect the actual thread mode before sending.

| Mode | T3's documented behavior |
| --- | --- |
| Supervised | Requests approval for commands and file changes; some read-only actions can proceed |
| Auto-accept edits | Automatically approves file edits; other actions can still require approval |
| Auto | Uses provider automatic review where supported; behavior varies by provider |
| Full access | Allows commands and edits without the usual approval prompts; provider-specific restrictions can still apply |

This is a recommendation for learning the workflow, not a claim that the repository requires a particular T3 mode. See [permission modes and provider differences](https://github.com/pingdotgg/t3code/blob/main/docs/user/permission-modes.md).

## 5. Open your project

Use **Add project**, or drag a local folder onto the desktop sidebar. For this roadmap repository, select:

```text
/Users/ron/Documents/trekai/trekai-platform-roadmap
```

The web client uses **Add project** because browsers do not share local folder paths through folder dragging.

Optionally enable the bundled `t3` command in **Settings → About → t3 command → Install**. Open a new terminal after setup, then, with the desktop app running on the same machine:

```sh
cd /Users/ron/Documents/trekai/trekai-platform-roadmap
t3 app
```

This opens a thread for the current directory, adding the project if necessary. `t3 app` requires the running desktop app; it is not the command for connecting to a standalone remote server. If `t3` is missing, check **Settings → About** and the displayed **Add to PATH** option. Source: [install and first run](https://github.com/pingdotgg/t3code/blob/main/docs/user/install.md).

## 6. Run a small first task

Choose the project, provider/model, and **Supervised** permissions. Start with inspection before editing:

```text
Read AGENTS.md and README.md. Confirm the current working directory,
Git branch, and existing local changes. Summarize the purpose of
ai-guide-roadmap/tooling and suggest one small documentation improvement.
Do not edit files yet.
```

Check that the reported directory and branch are correct, that existing changes are recognized, and that the agent uses this repository's instructions. Then give it a specific small edit. Review the resulting diff and any command approval requests.

For a documentation change here, check local links and content consistency. A presentation or live diagram change has additional checks in the repository instructions; a Markdown setup guide does not require those operations.

## 7. Run parallel tasks in separate worktrees

T3 distinguishes a thread from a worktree. Threads in the same checkout share files and a branch. A new thread alone does not guarantee isolation.

1. Confirm your base branch includes the files both tasks need. Existing uncommitted edits are not a reliable shared baseline for new worktrees.
2. Create a thread and choose **New worktree** with the intended base branch.
3. Give it one bounded task, such as improving a setup subsection.
4. Create another thread with **New worktree** for an independent task, such as reviewing comparison sources.
5. Confirm each thread's working directory and branch before allowing edits.
6. Review each diff, run relevant checks, and integrate the reviewed work through the normal repository workflow.

Example task split:

| Thread | Task | Expected result |
| --- | --- | --- |
| Documentation | Clarify one setup step without changing the comparison | Small diff and link checks |
| Research | Review one tool's current license/free-plan claims | Dated findings with official sources; edits only within its assigned scope |

Start with two tasks. Separate worktrees prevent agents from editing the same working files, but changes can still conflict when merged. They do not create a security sandbox or separate shared services, credentials, network access, or databases. Use the [existing sandboxing guide](../sanboxing/README.md) when a private clone or runtime boundary is needed; do not assume opening a repository in T3 places it inside the previously described Docker setup.

Source: [working with threads](https://github.com/pingdotgg/t3code/blob/main/docs/user/thread-sidebar.md).

## 8. Review and hand off

Inspect the diff before committing. Check the changed files, any relevant test results, and the branch/worktree receiving the commit. T3 can generate commit messages and PR descriptions, but read them before publishing.

For GitHub PR workflows, connect the appropriate host account using [T3's source-control setup](https://github.com/pingdotgg/t3code/blob/main/docs/user/source-control.md). Provider/model sign-in and Git hosting sign-in are separate. A model connection does not establish Git push or PR permissions.

Save a brief handoff describing what changed, how it was checked, and what remains unresolved. Follow the project's instructions about progress records and reviews.

## Optional: web, remote, and phone access

Get the local workflow working first. T3's CLI can run a server and open the web client with `t3`; `t3 serve` starts it without opening a browser. Its docs describe `t3 up` and pairing for other devices. Follow the [remote-access guide](https://github.com/pingdotgg/t3code/blob/main/docs/user/remote-access.md) for the current connection and authentication flow rather than exposing a port by guesswork.

Mobile is a client of the agent machine; installing the phone app does not move the agents onto the phone. The host must remain available for work to continue. Provider installation, project files, and authentication belong to that host. Follow the [background-service guide](https://github.com/pingdotgg/t3code/blob/main/docs/user/background-service.md) if you later need an always-running server.

## Troubleshooting

| Symptom | Check |
| --- | --- |
| Git reports an `xcrun` / developer-tools error on Mac | Repair/install Apple's developer tools, then rerun `git --version` before creating worktrees |
| Provider missing | Select the correct environment; inspect the provider's installation and Binary path on that machine |
| Provider visible but not authenticated | Complete its documented sign-in flow on the agent machine, then recheck readiness |
| `t3` command not found | Install it from Settings → About, apply the displayed PATH setup, and open a new terminal |
| `t3 app` cannot reach the desktop app | Launch/update the desktop app on the same machine; use the remote guide for a standalone server |
| Two tasks affect the same files unexpectedly | Check whether their threads share a checkout; use New worktree for independent editing |
| Worktree lacks recent local files | Check the chosen base commit and whether those files were uncommitted in another checkout |
| PR creation fails | Check hosting-provider authentication, repository access, and Git remote credentials separately from model access |
| Remote client loses the agent | Check the host/server and connection; the mobile/web client does not keep an offline host running |
| Instructions differ from your installed version | Check the current upstream docs and provider compatibility notices in Settings → Providers |

## First-run checklist

- [ ] Git works on the agent machine.
- [ ] T3 Code opens and a provider reports ready.
- [ ] The selected project, directory, branch, model, and permission mode are correct.
- [ ] One inspection task completes with the expected context.
- [ ] One small edit produces a diff you can review and check.
- [ ] Two parallel editing tasks use distinct worktrees when needed.
- [ ] Git hosting authentication works if PR creation is part of the trial.

No live T3/provider installation, authentication, worktree launch, remote connection, or PR creation was tested while writing this guide. The setup steps were checked against upstream documentation; the checklist remains for the person performing installation.
