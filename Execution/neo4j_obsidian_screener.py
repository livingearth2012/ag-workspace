import os
import re
import json
from datetime import datetime

# CONFIGURATION
VAULT_ROOT = "/home/openclaw/ObsidianVaults/OC_MM"
SCREENER_LOG = "/home/openclaw/ObsidianVaults/OC_MM/03_Projects-Active/AG-Workspace/Execution/neo4j_screening_report.json"
RELEVANCE_KEYWORDS = ["#knowledge", "#concept", "#entity", "#protocol", "#architecture", "relationship", "mapping"]

class KnowledgeScreener:
    def __init__(self, vault_path):
        self.vault_path = vault_path
        self.results = []

    def screen_file(self, file_path):
        """Analyze a markdown file for Neo4j inclusion potential."""
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()
        
        rel_path = os.path.relpath(file_path, self.vault_path)
        score = 0
        reasons = []

        # Criterion 1: Frontmatter Tags
        if "tags:" in content or "#" in content:
            found_tags = [kw for kw in RELEVANCE_KEYWORDS if kw in content.lower()]
            if found_tags:
                score += (20 * len(found_tags))
                reasons.append(f"Contains relevant tags/keywords: {', '.join(found_tags)}")

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
        for root, dirs, files in os.walk(self.vault_path):
            if ".git" in root or ".obsidian" in root:
                continue
            for file in files:
                if file.endswith(".md"):
                    analysis = self.screen_file(os.path.join(root, file))
                    if analysis:
                        self.results.append(analysis)
        
        # Sort by score
        self.results.sort(key=lambda x: x['score'], reverse=True)
        
        with open(SCREENER_LOG, 'w') as f:
            json.dump(self.results, f, indent=4)
        
        self.generate_human_report()

    def generate_human_report(self):
        report_path = SCREENER_LOG.replace(".json", ".md")
        with open(report_path, 'w') as f:
            f.write(f"# Neo4j Weekly Screening Report: {datetime.now().strftime('%Y-%m-%d')}\n\n")
            f.write("This report identifies high-value Obsidian notes that should be synced to Neo4j to build our Knowledge Graph.\n\n")
            f.write("## Selection Logic (Teaching Agents & Users)\n")
            f.write("- **Rank 100+ (APPROVED):** Core nodes with heavy linking and key tags.\n")
            f.write("- **Rank 30-60 (RECOMMENDED):** Contextual notes that provide supporting relationships.\n\n")
            
            f.write("## Screened Recommendations\n")
            for res in self.results[:20]: # Show top 20
                status_emoji = "✅" if res['status'] == "APPROVED" else "💡"
                f.write(f"### {status_emoji} {res['file']} (Score: {res['score']})\n")
                for reason in res['reasons']:
                    f.write(f"- {reason}\n")
                f.write("\n")

if __name__ == "__main__":
    screener = KnowledgeScreener(VAULT_ROOT)
    screener.run()
