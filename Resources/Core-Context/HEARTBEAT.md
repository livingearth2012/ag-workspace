# HEARTBEAT.md
# Ally's live heartbeat instruction file. Read and follow strictly every heartbeat cycle.
# Interval: 1440 minutes (set via agents.defaults.heartbeat.every in openclaw.json)

## Heartbeat Protocol

### 1. Session Health Check
Check JSONL sizes for all agents:
  ls -lh ~/.openclaw/agents/main/sessions/*.jsonl
  ls -lh ~/.openclaw/agents/devon/sessions/*.jsonl
  ls -lh ~/.openclaw/agents/genni/sessions/*.jsonl
  ls -lh ~/.openclaw/agents/claw/sessions/*.jsonl
  ls -lh ~/.openclaw/agents/sentinel/sessions/*.jsonl

| Condition | Action |
|-----------|--------|
| Any file >750K | Trigger SESSION HANDOFF protocol (see below) |
| Any file >500K | Run cleanup, post alert to #oc_ally-notifications |
| All files <500K | Note as clean, no action |

### 2. Post to #oc_heartbeats (C0AJXS4AMNE) ONLY
Post here and nowhere else. Do not post to webchat. Do not post to #oc_ally-notifications.

Format -- anomalies present:
  [Ally] #status: <YYYY-MM-DD HH:MM MT> -- WARN <agent>: <size> | <agent2>: <size2>

Format -- all clear:
  [Ally] #status: <YYYY-MM-DD HH:MM MT> -- all clear

Then include active tasks. For each agent that has tasks to complete before the next heartbeat, list them by name. Only list agents that have active or planned tasks -- skip agents with nothing pending.

Example:
  Ally: <task 1> | <task 2>
  Devon: <task 1>

If no agent -- including Ally -- has any active or planned tasks before the next heartbeat, display:
  Ally has no tasks she is doing or planning to do before the next heartbeat.

---

## SESSION HEALTH: Autonomous Maintenance

Monitor and maintain session health across all agents. Do not wait for Forrist to notice.

### Cleanup Authority -- No Approval Needed

  openclaw sessions cleanup --agent main --enforce --fix-missing
  openclaw sessions cleanup --agent devon --enforce --fix-missing
  openclaw sessions cleanup --agent genni --enforce --fix-missing
  openclaw sessions cleanup --agent claw --enforce --fix-missing
  openclaw sessions cleanup --agent sentinel --enforce --fix-missing

After cleanup, identify and delete orphaned JSONL files not listed in sessions.json.

### Gateway Restart -- Requires Forrist Confirmation

After cleanup, post to #oc_ally-notifications:
  [Ally] #system: Session cleanup complete. <agent>: <size before> -> <size after>. Orphans removed: <n>. Gateway restart needed -- is restart confirmed?

If Forrist replies 'restart confirmed' or 'yes' to that specific question, or if no response is received within 3 hours in #oc_ally-notifications, execute immediately:
  openclaw gateway restart && openclaw agents list

Then post: [Ally] #system: Gateway restarted. All agents online.

### Post-Cleanup Log

Write to 00_Staging-Forrist/ with: timestamp, trigger condition, agent, JSONL size before/after, orphans removed, restart status.

---

## SESSION HANDOFF -- 750K Threshold

When any active Ally session JSONL reaches 750K during a heartbeat check:

1. Generate summary: session ID, size, key decisions, files modified, open tasks, timestamp
2. Write HANDOFF block to: /home/openclaw/ObsidianVaults/OC_MM/09_Ally-Memory/Projects/current-status.md

   Block format:
   ## SESSION HANDOFF -- <timestamp>
   Session: <id> | Size: <size> | Trigger: 750K threshold
   ### Decisions Made
   <list>
   ### Files Modified
   <list>
   ### Open Tasks
   <list>

3. Run cleanup: openclaw sessions cleanup --agent main --enforce --fix-missing

4. Post to #oc_ally-notifications (C0AHNRLAZHR):
   [Ally] #system: Session handoff triggered. JSONL: <size>. Context written to current-status.md.
   New session auto-loads context on startup: https://oc.pccoop.org/chat
   Gateway restart needed -- reply 'restart confirmed' to proceed.

5. Stop -- do not continue processing in the bloated session after handoff.
