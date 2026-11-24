# Codex and Claude Code Folder Structure

**Official documentation checked on November 24, 2026.** This guide covers local Codex clients and Claude Code, including their personal configuration and repository files. Hosted sessions can load different settings. Here, “Claude” means Claude Code, rather than the general Claude chat interface.

Use the folders to give an agent consistent project knowledge, repeatable procedures, and appropriate configuration. Start with a short project instruction file. Add skills, specialized agents, and hooks when you have a concrete use for them. The trees below show useful documented locations, not a list of folders you must create.

## Understand personal and project scope

`~` means your home directory. A path such as `~/.codex/config.toml` contains personal defaults. A path such as `my-project/.codex/config.toml` belongs to one project. The leading dot makes a folder hidden by default on macOS and Linux; it does not make its contents secret.

| Scope | What belongs there | How it helps |
| --- | --- | --- |
| Personal | Preferences and reusable tools you use across projects | Avoid repeating your own setup in every repository |
| Project | Team conventions, project settings, and project-specific workflows | Give everyone working in the repository a consistent starting point |
| Local project override | Your private adjustments for one project, where supported | Customize your environment without changing teammates' settings |
| Managed | Organization-enforced configuration | Apply centrally administered limits and defaults |
| Generated state | History, memory, credentials, caches, and execution records | Support continuity and troubleshooting; generally let the application manage these |

An instruction file supplies model context. Configuration, permissions, and sandbox controls govern capabilities. Writing “do not deploy” in an instruction file is useful guidance, but it does not replace access controls. [Codex configuration](https://learn.chatgpt.com/docs/config-file/config-basic), [Claude settings](https://code.claude.com/docs/en/settings), [Claude instructions](https://code.claude.com/docs/en/memory).

## Codex personal folders

Codex uses `CODEX_HOME`, which defaults to `~/.codex`, for its configuration and local state. The current skills guide documents a separate personal authoring location at `~/.agents/skills/`. These are two different directories. [Config and state](https://learn.chatgpt.com/docs/config-file/config-advanced#config-and-state-locations), [skill locations](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

```text
~/
├── .codex/                              # Default CODEX_HOME
│   ├── config.toml                      # Personal settings and MCP configuration
│   ├── AGENTS.md                        # Personal standing instructions
│   ├── AGENTS.override.md               # Optional alternative to AGENTS.md here
│   ├── deep-review.config.toml          # Example named CLI profile
│   ├── agents/
│   │   └── reviewer.toml                # Optional custom subagent definition
│   ├── rules/
│   │   └── default.rules                # Command execution policy rules
│   ├── hooks.json                       # Optional lifecycle hook registrations
│   ├── auth.json                        # Only when using file-based credentials
│   ├── history.jsonl                    # When history persistence is enabled
│   ├── memories/                        # Generated memory store, when used
│   ├── memories_v2/                     # Newer generated memory store, when used
│   └── ...                             # Other application-managed state
└── .agents/
    └── skills/
        └── review-change/               # Example personal skill
            ├── SKILL.md
            ├── references/              # Optional supporting documentation
            ├── scripts/                 # Optional executable helpers
            ├── assets/                  # Optional templates or other resources
            └── agents/
                └── openai.yaml          # Optional Codex skill metadata
```

### What to maintain yourself

| Path | Purpose | Useful example |
| --- | --- | --- |
| `~/.codex/config.toml` | Personal client defaults, permissions configuration, and MCP server entries | Configure the integrations you use across repositories |
| `~/.codex/AGENTS.md` | Instructions that should apply across projects | Your preferred response style and general working conventions |
| `~/.codex/<name>.config.toml` | A named configuration layer selected with `codex --profile <name>` | Separate your normal work settings from a review-oriented profile |
| `~/.agents/skills/<name>/SKILL.md` | A reusable workflow with a name, description, and instructions | A procedure for investigating a failing CI job |
| `~/.codex/agents/<name>.toml` | A custom subagent with a defined role and supported model or capability settings | A focused reviewer that reports findings with file references |
| `~/.codex/hooks.json` | Register actions for lifecycle events; inline hooks in `config.toml` are another supported representation | Run a configured check at the appropriate event |

A skill's `agents/openai.yaml` contains optional interface, invocation-policy, and dependency metadata. It is **not** a custom subagent definition; those belong in `.codex/agents/*.toml`. [Skills](https://learn.chatgpt.com/docs/build-skills), [custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents#custom-agents), [hooks](https://learn.chatgpt.com/docs/hooks).

Current Codex profiles use separate `<name>.config.toml` files. Since Codex 0.134.0, `--profile` no longer reads the older `[profiles.<name>]` tables from `config.toml`. This matters when following an older setup tutorial. [Profile format and migration](https://learn.chatgpt.com/docs/config-file/config-advanced#profiles).

### What Codex manages

Let Codex manage authentication, history, and generated memory. Credentials may use the OS credential store instead of `auth.json`. Memories are optional, and current clients can use `memories/`, `memories_v2/`, or both during migration. Required project rules should stay in `AGENTS.md` or checked-in documentation, rather than depending on generated recall. Additional bundled-skill, plugin, cache, and state directories can vary by installation. [Local state](https://learn.chatgpt.com/docs/config-file/config-advanced#config-and-state-locations), [memory storage](https://learn.chatgpt.com/docs/customization/memories#local-memory-storage).

## Codex project folders

```text
my-project/
├── AGENTS.md                            # Shared project instructions
├── AGENTS.override.md                   # Optional replacement at this directory
├── .codex/
│   ├── config.toml                      # Trusted project configuration
│   ├── agents/
│   │   └── reviewer.toml                # Project-specific custom subagent
│   ├── rules/
│   │   └── review.rules                 # Optional command execution policy
│   └── hooks.json                       # Optional project hook registrations
├── .agents/
│   └── skills/
│       └── investigate-ci/
│           ├── SKILL.md
│           ├── references/
│           └── scripts/
├── services/
│   └── api/
│       └── AGENTS.md                    # More specific module instructions
└── docs/
    └── ...                              # Specifications, decisions, and runbooks
```

The project instruction file is normally `my-project/AGENTS.md`, **outside** `.codex/`. Do not confuse it with the personal `~/.codex/AGENTS.md`. Codex discovers guidance from the project root toward the launch directory. At each level it chooses `AGENTS.override.md` before `AGENTS.md`; it does not append both files from that same directory. More specific guidance appears later in the instruction chain. [Instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance).

Project `.codex/config.toml`, hooks, and rules load only from trusted project layers. Codex finds repository skills under `.agents/skills/` along the path between the current directory and repository root. This lets a large repository keep general procedures at the root and specialized procedures near a service. [Project configuration](https://learn.chatgpt.com/docs/config-file/config-advanced#project-config-files-codexconfigtoml), [skill discovery](https://learn.chatgpt.com/docs/build-skills#where-codex-loads-local-skills).

Codex `.rules` files are an experimental execution-policy mechanism for commands outside the sandbox. They are not Markdown coding guidelines. Put architectural guidance in `AGENTS.md`; use execution rules for the command-policy behavior they support. [Codex rules](https://learn.chatgpt.com/docs/agent-configuration/rules).

Custom Codex subagents inherit the parent's permissions, provider, and MCP servers. A role description that says “read only” does not create a separate read-only sandbox. [Subagent permissions](https://learn.chatgpt.com/docs/agent-configuration/subagents#approvals-and-sandbox-controls).

## Claude Code personal folders

Claude Code normally uses `~/.claude/` and a separate `~/.claude.json` file. `CLAUDE_CONFIG_DIR` can relocate this configuration and state. The personal folder contains both files you author and data the application generates. [Claude directory reference](https://code.claude.com/docs/en/claude-directory).

```text
~/
├── .claude.json                         # App state and personal/local MCP entries
└── .claude/
    ├── CLAUDE.md                        # Personal standing instructions
    ├── settings.json                    # Personal settings, permissions, hooks
    ├── rules/
    │   └── testing.md                   # Optional personal instruction rules
    ├── skills/
    │   └── investigate-ci/
    │       ├── SKILL.md
    │       ├── references/
    │       └── scripts/
    ├── agents/
    │   └── reviewer.md                  # Optional custom subagent
    ├── commands/
    │   └── review.md                    # Older single-file skill/command format
    ├── workflows/
    │   └── review.js                    # Optional saved dynamic workflow
    ├── output-styles/
    │   └── explain.md                   # Optional response style
    ├── projects/
    │   └── <project>/
    │       ├── <session>.jsonl           # Generated conversation transcript
    │       └── memory/
    │           ├── MEMORY.md            # Auto-memory index
    │           └── <topic>.md           # Individual memories
    ├── agent-memory/
    │   └── <agent-name>/                # Optional subagent memory
    ├── plugins/                         # Installed plugin data
    ├── plans/                           # Generated plan files
    ├── file-history/                    # Generated file checkpoints
    ├── debug/                           # Debug logs, when enabled
    ├── history.jsonl                    # Prompt recall history
    └── ...                              # Other application-managed data
```

### What each part gives you

| Path | Purpose | How it helps |
| --- | --- | --- |
| `~/.claude/CLAUDE.md` | Personal instructions across projects | Keep preferences consistent without adding them to each repository |
| `~/.claude/settings.json` | Personal settings, permissions, and hook configuration | Control the client separately from prose instructions |
| `~/.claude/rules/*.md` | Modular instruction files | Organize guidance by topic; supported path filters can narrow when it loads |
| `~/.claude/skills/<name>/SKILL.md` | Reusable workflows, invoked with `/name` or selected when relevant | Reuse a proven procedure with supporting files |
| `~/.claude/agents/*.md` | Subagent definitions with frontmatter and a prompt | Define a specialized reviewer or investigator |
| `~/.claude/commands/*.md` | The older single-file format, still supported | Retain existing commands; prefer skill folders for new procedures |
| `~/.claude/projects/<project>/memory/` | Auto memory retained across sessions | Recall useful preferences and corrections without treating them as enforced policy |
| `~/.claude.json` | Application state and MCP entries at user or private project scope | Let the CLI manage personal integrations and project state |

The official directory reference also documents optional `workflows/*.js`, `output-styles/*.md`, and subagent memory. Add these only when their purpose is useful to your workflow. Sessions, checkpoints, logs, and installed-plugin records are application data rather than a project template. [Directory and application data](https://code.claude.com/docs/en/claude-directory), [skills and commands](https://code.claude.com/docs/en/skills), [auto memory](https://code.claude.com/docs/en/memory#auto-memory).

## Claude Code project folders

```text
my-project/
├── CLAUDE.md                            # Shared instructions; alternative below
├── CLAUDE.local.md                      # Personal project instructions, gitignore
├── .mcp.json                            # Shared project MCP server definitions
├── .claude/
│   ├── CLAUDE.md                        # Alternative location for project guidance
│   ├── settings.json                    # Shared project settings
│   ├── settings.local.json              # Personal project settings, gitignore
│   ├── rules/
│   │   ├── testing.md
│   │   └── infrastructure.md
│   ├── skills/
│   │   └── investigate-ci/
│   │       ├── SKILL.md
│   │       ├── references/
│   │       └── scripts/
│   ├── agents/
│   │   └── reviewer.md
│   ├── commands/                        # Optional older command format
│   ├── workflows/                       # Optional dynamic workflows
│   └── worktrees/                       # Generated isolated checkouts, when used
├── services/
│   └── api/
│       └── CLAUDE.md                    # Module guidance, loaded when applicable
└── docs/
    └── ...
```

Choose one main project guidance location, normally root `CLAUDE.md` or `.claude/CLAUDE.md`, rather than duplicating the same content. Claude concatenates applicable instructions; it does not provide a general guarantee that contradictory prose in a closer file wins. Keep personal and project guidance consistent. [Instruction locations and loading](https://code.claude.com/docs/en/memory#claude-md-files).

`.claude/rules/*.md` can split guidance into topics. A rule with supported `paths` frontmatter can load for matching files, which is useful for infrastructure-specific conventions without putting them into every task. [Path-specific rules](https://code.claude.com/docs/en/memory#path-specific-rules).

Hook registrations belong in a settings file's `hooks` configuration. A directory named `.claude/hooks/` is a useful place to store scripts **if you choose that convention**, but putting a script there does not register it automatically. Likewise, a chosen script directory for Codex must be referenced by its hook configuration. [Claude hook configuration](https://code.claude.com/docs/en/claude-directory#choose-the-right-file), [Codex hook configuration](https://learn.chatgpt.com/docs/hooks).

### Understand the MCP location difference

For Claude Code, shared project servers belong in root `.mcp.json`. Personal servers and private project-scoped servers are stored in `~/.claude.json`; the latter do **not** belong in `.claude/settings.local.json`. Prefer `claude mcp` commands to maintain these records. Codex documents MCP entries under `[mcp_servers.<name>]` in its TOML configuration. These formats are not interchangeable. [Claude MCP scopes](https://code.claude.com/docs/en/mcp#mcp-installation-scopes), [Codex MCP configuration](https://learn.chatgpt.com/docs/extend/mcp).

## Compare the two tools

| Need | Codex | Claude Code |
| --- | --- | --- |
| Personal configuration | `~/.codex/config.toml` | `~/.claude/settings.json` |
| Shared project configuration | `.codex/config.toml` in trusted projects | `.claude/settings.json` |
| Personal project settings file | No equivalent filename documented here; use supported configuration layers | `.claude/settings.local.json` |
| Main project guidance | `AGENTS.md` | `CLAUDE.md`, or supported `AGENTS.md` loading |
| Personal guidance | `~/.codex/AGENTS.md` | `~/.claude/CLAUDE.md` |
| Project skills | `.agents/skills/<name>/SKILL.md` | `.claude/skills/<name>/SKILL.md` |
| Personal skills | `~/.agents/skills/<name>/SKILL.md` | `~/.claude/skills/<name>/SKILL.md` |
| Custom project subagents | `.codex/agents/*.toml` | `.claude/agents/*.md` |
| Modular prose guidance | Nested `AGENTS.md` and referenced project documentation | `.claude/rules/*.md` and nested instruction files |
| Execution policy | Sandbox and approval settings; `.rules` where supported | Permission settings, sandbox controls, and supported hooks |
| Hook registration | `hooks.json` or inline TOML hooks | `hooks` in settings JSON |
| Shared project MCP | `[mcp_servers.<name>]` in TOML configuration | Root `.mcp.json` |

The source sections above establish these paths. Two particularly easy mistakes are treating Codex `.rules` as equivalent to Claude Markdown rules, and assuming either product automatically reads the other's skill directory.

### Configuration precedence differs from instruction loading

For ordinary Codex configuration values, CLI overrides take priority over trusted project layers, selected profile files, and user defaults. Claude's ordinary settings precedence is managed policy, command-line settings, project-local settings, shared project settings, then user settings. Some fields have merge or special handling rules, and administrator constraints remain applicable. Do not apply either settings precedence list to conflicting Markdown prose as if it were a deterministic settings merge. [Codex precedence](https://learn.chatgpt.com/docs/config-file/config-basic#configuration-precedence), [Claude precedence](https://code.claude.com/docs/en/settings#settings-precedence).

## Use both tools without maintaining duplicate instructions

My recommended shared setup is to keep general project guidance in `AGENTS.md` and let Claude Code consume it through its supported mechanism.

Current Claude Code documentation says direct `AGENTS.md` loading requires **v2.1.277 or later**. By default, it loads these files when no project `CLAUDE.md` or `CLAUDE.local.md` exists in the working directory or above it. Personal `~/.claude/CLAUDE.md` does not disable that fallback. Settings and session availability can change the behavior. [Claude AGENTS.md support](https://code.claude.com/docs/en/memory#agents-md).

For a repository that also needs Claude-specific guidance, or sessions without direct support, a small root `CLAUDE.md` can import the shared file:

```markdown
@AGENTS.md

## Claude Code specific guidance

Keep tool-specific instructions here only when the shared guidance cannot cover them.
```

The `@AGENTS.md` line must be actual file content, outside a code fence in the real `CLAUDE.md`. This is a documented Claude import mechanism, not a general Markdown feature that every agent expands. Keep shared instruction content in one place. [Sharing instructions](https://code.claude.com/docs/en/memory#share-one-file-with-other-coding-tools).

For skills, keep the standard `SKILL.md` procedure as portable as possible, while using the discovery path each tool documents. You can maintain a common source and synchronize it into both locations, or use links where your clients and operating system support them. Test discovery in both clients, and keep vendor-specific frontmatter or metadata separate where needed. Sharing a standard file format does not imply identical tool permissions or invocation behavior. [Codex skills](https://learn.chatgpt.com/docs/build-skills), [Claude skills](https://code.claude.com/docs/en/skills).

## Connect the folders to your development and DevOps work

This is a suggested organization for the practices in the [AI workflow guide](ai-workflow-guide.md):

| Information or behavior | Where to put it | Benefit |
| --- | --- | --- |
| Repository commands and architectural boundaries | Shared project instruction file | The agent starts with the conventions that prevent recurring mistakes |
| A feature's intended behavior and acceptance criteria | A versioned specification under `docs/` or the project's established location | Keep the goal reviewable as implementation changes |
| A proven CI investigation procedure | A task-specific skill with references and scripts | Reuse expertise only when the task calls for it |
| A specialized review role | A custom agent definition | Give the role a clear scope and expected output |
| Access to CI, source control, or telemetry | The tool's MCP configuration and authorization controls | Retrieve current evidence instead of relying on stale copied output |
| A check that must run mechanically | A supported hook and its registered script | Reduce dependence on the model remembering a prose instruction |
| Current progress, evidence, and open questions | An explicit task handoff document | Resume work without loading an entire conversation history |
| A recalled preference or correction | Generated memory, reviewed when important | Improve continuity while keeping authoritative rules in maintained files |

Ordinary files under `docs/` do not become standing instructions merely because they exist. Point the agent to the relevant file, reference it from guidance, or load it through the workflow. Keep the main guidance short so it helps the agent find detailed material when needed.

## Scale instructions for a large project

Keep the root instruction file as a small entry point. Put rules that only apply to one service or directory close to that code, and keep detailed explanations in referenced documents. Moving text into folders is useful when it narrows what is relevant; importing every document back into the root defeats that purpose.

### Recommended length versus technical limits

- **Suggested team guideline for `AGENTS.md`:** aim for fewer than about **200 concise lines per file**, often much less at the root. This is a maintainability target proposed here, not an official Codex line limit. Remove duplication and split by responsibility rather than padding to a number.
- **Codex loading cap:** the documented default `project_doc_max_bytes` is **32 KiB for the combined instruction chain**, not 32 KiB per nested file. Nesting does not reset this budget. [Codex instruction discovery](https://learn.chatgpt.com/docs/agent-configuration/agents-md#how-codex-discovers-guidance).
- **Claude Code recommendation:** its documentation recommends **under 200 lines per `CLAUDE.md`**. Imported files still add to context; splitting via imports alone does not reduce what is loaded. [Writing effective instructions](https://code.claude.com/docs/en/memory#write-effective-instructions).

These are different measures: a line target helps readability; bytes measure a client loading budget; neither is a universal token allowance or a guarantee that every instruction will be followed.

### Example: shared guidance plus local detail

```text
my-project/
├── AGENTS.md                      # Shared commands, boundaries, project map
├── CLAUDE.md                      # Optional Claude wrapper importing @AGENTS.md
├── services/
│   ├── api/
│   │   ├── AGENTS.md              # API test command, contracts, local constraints
│   │   └── CLAUDE.md              # Optional wrapper importing this AGENTS.md
│   └── web/
│       ├── AGENTS.md              # UI conventions and web checks
│       └── CLAUDE.md              # Optional wrapper importing this AGENTS.md
├── infrastructure/
│   ├── AGENTS.md                  # Terraform validation and environment boundaries
│   └── CLAUDE.md                  # Optional wrapper importing this AGENTS.md
├── .agents/skills/
│   └── review-change/SKILL.md     # Reusable procedure selected when relevant
├── .claude/rules/
│   └── api.md                    # Alternative: a path-scoped Claude rule
└── docs/
    ├── architecture.md           # Detailed reference, read when relevant
    ├── api-contracts.md
    └── deployment.md
```

This is an illustrative layout, not a requirement to create every file. Choose one maintained source for each rule. Claude wrappers or path-scoped rules are options; do not copy the same guidance into all of them. A child wrapper should import its own local `AGENTS.md`, not repeatedly import the root.

### How the scoped guidance is selected

**Codex:** startup discovery follows the project-root-to-working-directory path. For work launched in `services/api`, that includes root and API guidance, not sibling web instructions. A nearer instruction can refine broader guidance; `AGENTS.override.md` replaces `AGENTS.md` at the same directory level. When working across modules, explicitly inspect each module's applicable instructions. [Layered instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md#layer-project-instructions).

**Claude Code:** ancestor `CLAUDE.md` guidance loads at launch; child guidance loads when files in that subtree are accessed. Path-scoped `.claude/rules/` can target matching files. Applicable prose is combined, so avoid contradictions rather than assuming a closer file always resolves them. Check the earlier shared-guidance section before relying on `AGENTS.md` fallback. [Loading behavior](https://code.claude.com/docs/en/memory#how-claude-md-files-load), [path-specific rules](https://code.claude.com/docs/en/memory#path-specific-rules).

### What to put where

- **Root guidance:** repository navigation, shared build/test commands, boundaries that apply everywhere, and pointers to local guidance.
- **Nested guidance:** only the differences for that service, package or infrastructure area: its commands, contracts, constraints and validation.
- **Referenced docs:** architecture explanations, specifications, runbooks and examples needed for particular tasks. Link them and read them when relevant; a link is not the same as an automatic import.
- **Skills:** repeatable multi-step procedures, with their own references and scripts.
- **Handoffs:** temporary task state, evidence and open questions; keep these out of permanent instructions unless they become durable lessons.

Before a task, identify the target subtree, load its applicable guidance, and check for conflicting or stale rules. After a change, update only the guidance whose scope changed. Verify discovery from the intended working directory, rather than assuming every file was loaded. Instruction files remain context, not substitutes for permissions or sandbox controls.

Documentation for the loading and size details above was checked on November 24, 2026. The example layout and `AGENTS.md` line target are proposed team practices.

## Decide what to commit

Commit the shared instruction files, reviewed project skills and agent definitions, useful non-secret project configuration, and the scripts those configurations reference. Shared MCP definitions should refer to appropriate authentication mechanisms instead of embedding credentials.

Keep personal overrides, authentication material, generated session records, logs, and caches out of the repository. Review generated memory before choosing to share it. For Claude, explicitly ignore local files you create yourself; current Claude Code also excludes `settings.local.json` when it writes the file. [Claude local settings](https://code.claude.com/docs/en/settings#keep-personal-settings-out-of-a-repository).

An example project `.gitignore` addition, to adapt to your repository:

```gitignore
# Personal Claude project files
CLAUDE.local.md
.claude/settings.local.json

# Local isolated checkouts, when used
.claude/worktrees/
```

Avoid ignoring the entire project `.claude/`, `.codex/`, or `.agents/` directory if it contains the shared setup your team needs. Home-directory configuration should not be copied wholesale into a repository.

## Start with the smallest useful setup

1. Write a short shared project instruction file with the commands, boundaries, and conventions you repeatedly explain.
2. If using both tools, verify Claude's `AGENTS.md` support or add the documented import.
3. Add project settings only for behavior the project actually needs; keep personal preferences in user configuration.
4. Turn one proven repeated procedure into a skill in the appropriate discovery location.
5. Add custom agents, MCP connections, or hooks when they solve a specific recurring problem.

Check `codex --version` and `claude --version` when a documented feature is missing. In Claude Code, `/context all` shows loaded instruction files and `/status` helps identify setting sources. In Codex, verify which guidance and skills the session reports, and restart after changes where the relevant documentation requires it. [Claude inspection](https://code.claude.com/docs/en/memory#set-up-a-project-claude-md), [settings inspection](https://code.claude.com/docs/en/settings), [Codex guidance](https://learn.chatgpt.com/docs/agent-configuration/agents-md), [Codex skills](https://learn.chatgpt.com/docs/build-skills).
