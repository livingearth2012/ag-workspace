import os
import re
import json
from datetime import datetime

# CONFIGURATION
VAULT_ROOT = "/home/openclaw/ObsidianVaults/OC_MM"
SCREENER_LOG = "/home/openclaw/ObsidianVaults/OC_MM/03_Projects-Active/AG-Workspace/Execution/neo4j_screening_report.json"
MASTER_SYNC_LOG = "/home/openclaw/ObsidianVaults/OC_MM/03_Projects-Active/AG-Workspace/Execution/neo4j_master_sync_list.json"
RELEVANCE_KEYWORDS = ["#knowledge", "#concept", "#entity", "#protocol", "#architecture", "relationship", "mapping", "system", "integration", "workflow", "ontology", "graph"]

class KnowledgeScreener:
    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.results = []
        self.ghost_notes = []
        self.master_list = self.load_master_list()

    def load_master_list(self):
        """Loads the list of files that were previously approved or synced."""
        if os.path.exists(MASTER_SYNC_LOG):
            with open(MASTER_SYNC_LOG, 'r') as f:
                return json.load(f)
        return {}

    def save_master_list(self):
        """Updates the master list with current findings."""
        with open(MASTER_SYNC_LOG, 'w') as f:
            json.dump(self.master_list, f, indent=4)

    def check_ghost_notes(self):
        """Identifies files that are in the master list but missing from the vault."""
        for rel_path, data in list(self.master_list.items()):
            full_path = os.path.join(self.vault_path, rel_path)
            if not os.path.exists(full_path):
                self.ghost_notes.append({
                    "file": rel_path,
                    "last_score": data.get("score", 0),
                    "status": "GHOST"
                })

    def screen_file(self, file_path):
        """Analyze a markdown file for Neo4j inclusion potential."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        rel_path = os.path.relpath(file_path, self.vault_path)
        
        # SKIP archives and noisy research imports
        if "99_Archives" in rel_path or "05_Research/Evernote" in rel_path:
            return None

        score = 0
        reasons = []

        # Criterion 1: Frontmatter Tags & Keywords
        found_tags = [kw for kw in RELEVANCE_KEYWORDS if kw in content.lower()]
        if found_tags:
            score += (10 * len(found_tags))
            reasons.append(f"Contains relevant keywords: {', '.join(found_tags)}")

        # Criterion 2: Connectivity (Internal Links)
        links = re.findall(r'\[\[(.*?)\]\]', content)
        if len(links) > 5:
            score += 30
            reasons.append(f"High connectivity: {len(links)} internal links (Potential Graph Hub)")
        elif len(links) > 0:
            score += 10
            reasons.append(f"Has links: {len(links)} connections")

        # Criterion 3: Folder Importance
        if "Projects-Active" in rel_path or "Directives" in rel_path:
            score += 25
            reasons.append("Located in high-priority directory (Active Projects/Directives)")

        # Criterion 4: Structural Indicators (Tables/Lists)
        if "|" in content and "---" in content: # Simple table check
            score += 15
            reasons.append("Contains structured data (Table)")

        if score > 30:
            return {
                "file": rel_path,
                "score": score,
                "reasons": reasons,
                "status": "APPROVED" if score > 60 else "RECOMMENDED"
            }
        return None

    def run(self):
        print(f"--- Starting Weekly Knowledge Screening: {datetime.now().strftime('%Y-%m-%d')} ---")
        
        # 1. Check for Ghost Notes (Deleted from Vault but in Master List)
        self.check_ghost_notes()

        # 2. Screen current files
        for root, dirs, files in os.walk(self.vault_path):
            if ".git" in root or ".obsidian" in root:
                continue
            for file in files:
                if file.endswith(".md"):
                    analysis = self.screen_file(os.path.join(root, file))
                    if analysis:
                        self.results.append(analysis)
                        # Update master list with latest score
                        self.master_list[analysis['file']] = {"score": analysis['score'], "timestamp": datetime.now().isoformat()}
        
        # Sort by score
        self.results.sort(key=lambda x: x['score'], reverse=True)
        
        self.save_master_list()
        
        with open(SCREENER_LOG, 'w') as f:
            json.dump({"recommendations": self.results, "ghost_notes": self.ghost_notes}, f, indent=4)
        
        self.generate_human_report()

    def generate_human_report(self):
        report_path = SCREENER_LOG.replace(".json", ".md")
        with open(report_path, 'w') as f:
            f.write(f"# Neo4j Weekly Screening & Pruning Report: {datetime.now().strftime('%Y-%m-%d')}\n\n")
            
            if self.ghost_notes:
                f.write("## ⚠️ Pruning Action Required (Ghost Notes Found)\n")
                f.write("The following files were deleted from Obsidian but exist in our Neo4j Knowledge Map. Please review for pruning:\n\n")
                f.write("| File Path | Last Score | Action (Ally/Forrist) |\n")
                f.write("| :--- | :--- | :--- |\n")
                for ghost in self.ghost_notes:
                    f.write(f"| {ghost['file']} | {ghost['last_score']} | [ ] PRUNE / [ ] KEEP |\n")
                f.write("\n---\n\n")

            f.write("## Selection Logic (Teaching Agents & Users)\n")
            f.write("- **Rank 100+ (APPROVED):** Core nodes with heavy linking and key tags.\n")
            f.write(" - **Rank 65+ (HIGH PRIORITY):** Essential context and integration maps.\n")
            f.write("- **Rank 30-60 (RECOMMENDED):** Supporting relationships.\n\n")
            
            f.write("## New Screened Recommendations\n")
            for res in self.results[:50]: # Show top 50 for broader pool
                status_emoji = "✅" if res['score'] >= 65 else "💡"
                f.write(f"### {status_emoji} {res['file']} (Score: {res['score']})\n")
                for reason in res['reasons']:
                    f.write(f"- {reason}\n")
                f.write("\n")

if __name__ == "__main__":
    screener = KnowledgeScreener(VAULT_ROOT)
    screener.run()
