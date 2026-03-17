# Protocol: Weekly Neo4j Knowledge Screening

## Overview
To keep our Neo4j Knowledge Graph focused and cost-effective, we only ingest high-value "anchor nodes" from the Obsidian Vault. This tool helps us decide which files qualify.

## Schedule
**Frequency:** Every Monday at 09:00 (or on-demand when significant new knowledge is added).

## Execution (Antigravity Role)
1. Run the screening script:
   `python3 /home/openclaw/ObsidianVaults/OC_MM/03_Projects-Active/AG-Workspace/Execution/neo4j_obsidian_screener.py`
2. Review the output report:
   `/home/openclaw/ObsidianVaults/OC_MM/03_Projects-Active/AG-Workspace/Execution/neo4j_screening_report.md`
3. Handoff to Ally:
   "Ally, I have screened the vault. Please review the high-priority recommendations in the screening report and orchestrate the Neo4j ingestion for top-tier files."

## Selection Criteria (The "Why")
- **Connectivity:** Notes with 5+ internal links are "hubs" that define the graph's structure.
- **Priority Folders:** Documents in `Projects-Active` and `Directives` take precedence.
- **Keywords:** Files containing `relationship`, `mapping`, or `protocol` keywords are essential for graph-based reasoning.
- **Structured Data:** Tables provide ready-to-ingest properties for Neo4j nodes.
