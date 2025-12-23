import re
from typing import Dict, List

class ConceptExtractor:
    
    def dfs_extract_concepts(self, text: str):
        concepts = {}
        current_parent = None
        
        for line in text.split('\n'):
            stripped = line.strip()
            if not stripped:
                continue
            
            # Parse markdown headers (## or ###) as main concepts
            if stripped.startswith('##') or stripped.startswith('###'):
                concept = re.sub(r'^#+\s*', '', stripped).strip()
                if concept:
                    concepts[concept] = []
                    current_parent = concept
            
            # Parse bullet points and bold text as subconcepts
            elif current_parent:
                if stripped.startswith(('- ', '* ')):
                    subconcept = re.sub(r'^[-*]\s*', '', stripped).strip()
                elif stripped.startswith('**') and stripped.endswith('**'):
                    subconcept = stripped.replace('**', '').strip()
                else:
                    continue
                
                if subconcept and current_parent in concepts:
                    concepts[current_parent].append(subconcept)
        
        return concepts
    
    def build_quiz_topics(self, summary_text: str) -> List[Dict]:
        concepts = self.dfs_extract_concepts(summary_text)
        return [
            {
                "order": idx,
                "main": concept,
                "subtopics": subs,
                "depth": len(subs)
            }
            for idx, (concept, subs) in enumerate(concepts.items(), 1)
        ]
    
    def get_concept_difficulty(self, topic: Dict) -> str:
        depth = topic["depth"]
        return "Easy" if depth == 0 else "Medium" if depth <= 3 else "Hard"
    
    def get_dfs_order(self, summary_text: str) -> List[str]:
        concepts = self.dfs_extract_concepts(summary_text)
        return [concept for main in concepts for concept in [main] + concepts[main]]
    
    def analyze_concept_relationships(self, summary_text: str) -> Dict:
        concepts = self.dfs_extract_concepts(summary_text)
        
        return {
            "total_main_concepts": len(concepts),
            "total_subconcepts": sum(len(subs) for subs in concepts.values()),
            "concepts_by_complexity": {
                "simple": sum(1 for subs in concepts.values() if len(subs) == 0),
                "moderate": sum(1 for subs in concepts.values() if 1 <= len(subs) <= 3),
                "complex": sum(1 for subs in concepts.values() if len(subs) > 3)
            },
            "all_topics": list(concepts.keys()),
            "subtopic_map": concepts
        }
