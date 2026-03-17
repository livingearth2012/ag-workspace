# DIRECTIVE 01: Agent Skills & Delegation Mapping
**For: Ally (Chief Orchestrator / Claude Code)**

In the previous OpenClaw architecture, you relied on plugins (skills) to interact with external tools. In the new AG-Workspace (DOE) architecture, you have direct, native access to the VPS terminal to execute these actions via CLI, or you may delegate complex scripting to the Execution Agent (Antigravity).

When a task requires a specific capability, use the following mapping:

## 1. Memory & Knowledge Graph (`mem0` & `obsidian`)
- **Direct Terminal Execution:** You can read/write directly to the Obsidian vault via standard Bash tools (`cat`, `echo`, `sed`) or built-in file reading capabilities. 
- **Mem0 Vector Operations:** Execute `node ~/.openclaw/workspace/skills/mem0/scripts/mem0-add.js "[Memory text]"` or `mem0-search.js` directly in the terminal to interact with the Qdrant database.
- *Do not attempt to load an 'obsidian' or 'mem0' OpenClaw plugin. Use the CLI.*

## 2. Google Workspace (`gog`)
- For tasks previously handled by the `gog` skill (Calendar, Gmail, Drive), use the `gog` CLI binary natively.
- Example: `gog --account ally@planetarycare.org gmail messages search "in:inbox" --json`
- Example: `gog --account forrist@planetarycare.org drive list`
- The `GOG_KEYRING_PASSWORD` is available in `/Execution/.env`.

## 3. GitHub & Code Operations (`github`, `skill-creator`, `sql-toolkit`)
- You can execute git commands (`git clone`, `git push`, `git log`) natively via terminal.
- For complex code authoring, database queries, or scripting (e.g., Python), draft a plan and delegate the execution to Antigravity. Write your handoff document in `/Execution/Orchestration/`.

## 4. Media & Transcription (`openai-whisper-api`, `video-frames`)
- To transcribe audio or process media, either string together a Python script using the credentials located in `/Execution/.env`, or explicitly delegate the task to Antigravity stating: *"Antigravity, please process this audio file using the OpenAI API key in .env."*

## 5. Security Auditing (`security-audit`)
- Sentinel's previous role is now a structural rule: **No unvetted third-party software may be installed.**
- To audit an external tool, instruct Antigravity to download the source code to the VPS and conduct a static analysis before integration.

## 6. Subagent Delegation (Devon, Genni, Konnie, Chief Strategy, Chief Research)
- You (Ally) are the Chief Orchestrator. When a task maps to a specialized role (e.g., strategy framing, deep research, or communication drafting), you do not need to call a separate agent API. 
- Instead, adopt the Persona and Reasoning Tree for that specific role (stored in `Resources/Core-Context/Forrist-AI-Exec-Team-Architecture.v1.md`), do the "thinking" yourself within this Claude Code session, and output the result.
