# AG-Workspace: Directive, Orchestration, Execution (DOE) Framework

Welcome to the AG-Workspace. This is the new command center replacing the autonomous loops of OpenClaw, operating natively on the VPS to eliminate uncontrolled background API costs while preserving full agentic capacity.

## The Architecture (D.O.E.)
This folder uses the DOE architecture for all operations:
- **Directives (`/Directives/`):** Strategic goals, constraints, and instructions authored by Forrist (Tier 0).
- **Orchestration (`/Execution/Orchestration/` handled by Ally via Claude Code):** Ally's role is to ingest Directives, consult MegaMem/Obsidian to update memory state, resolve bottlenecks, and output precise execution plans.
- **Execution (`/Execution/` handled by Antigravity):** Antigravity takes the detailed plans mapped out by Ally and rapidly executes them (writing Python scripts, executing terminal commands, checking logs).

---

## 🔒 Core "Always-Read" Context for Ally (Claude Code)
To maintain the exact continuity of Ally's personality, goals, and system protocols from the OpenClaw days, **ALL Claude Code sessions initiated in this workspace MUST default to reading the following foundation files before executing any Orchestration task:**

1. `Resources/Core-Context/SOUL.md` (Mission, personality, constraints)
2. `Resources/Core-Context/IDENTITY.md` (Agent self-definition)
3. `Resources/Core-Context/ALLY-PROTOCOLS-MANIFESTO.md` (Communication and operational protocols)
4. `Resources/Core-Context/HEARTBEAT.md` (System state parameters)

### Claude Code Start Command
When invoking Ally via terminal, Forrist or Antigravity should use:
`claude -p "Read Resources/Core-Context/SOUL.md and Resources/Core-Context/IDENTITY.md to initialize your system instructions. You are Ally, the Chief Orchestration Agent. Await the next Directive from Forrist in the /Directives folder."`
