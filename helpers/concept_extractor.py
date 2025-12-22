import re
from collections import defaultdict
from typing import Dict, List, Tuple

class ConceptExtractor:
    
    def __init__(self):
        self.concept_tree = defaultdict(list)
        self.visited_concepts = set()
    
    def dfs_extract_concepts(self, text: str) -> Dict[str, List[str]]:

        lines = text.split('\n')
        concepts = {}
        current_parent = None
        
        for line in lines:
            stripped = line.strip()
            
            if not stripped:
                continue
            
            # Parse markdown headers as concept levels
            if stripped.startswith('###'):
                # Main concept (h3 level)
                concept = re.sub(r'^#+\s*', '', stripped).strip()
                if concept:
                    concepts[concept] = []
                    current_parent = concept
                    
            elif stripped.startswith('##'):
                # Section header (h2 level) - could be parent
                concept = re.sub(r'^#+\s*', '', stripped).strip()
                if concept:
                    concepts[concept] = []
                    current_parent = concept
                    
            elif current_parent and (stripped.startswith('- ') or stripped.startswith('* ')):
                # Bullet points are subconcepts
                subconcept = re.sub(r'^[-*]\s*', '', stripped).strip()
                if subconcept and current_parent in concepts:
                    concepts[current_parent].append(subconcept)
                    
            elif current_parent and stripped.startswith('**') and stripped.endswith('**'):
                # Bold text = subconcepts
                subconcept = stripped.replace('**', '').strip()
                if subconcept and current_parent in concepts:
                    concepts[current_parent].append(subconcept)
        
        return concepts
    
    def dfs_traverse_concepts(self, concepts: Dict[str, List[str]], 
                             parent: str = '', depth: int = 0) -> List[Tuple[str, int]]:

        result = []
        visited = set()
        
        def dfs(current, d):
            if current in visited:
                return
            visited.add(current)
            result.append((current, d))
            
            # Visit subconcepts
            if current in concepts:
                for subconcept in concepts[current]:
                    dfs(subconcept, d + 1)
        
        # Start DFS from each main concept
        for concept in concepts.keys():
            if concept not in visited:
                dfs(concept, depth)
        
        return result
    
    def build_quiz_topics(self, summary_text: str) -> List[Dict]:
        """
        Extract topics in hierarchical order using DFS
        Returns list of topics to create questions about
        """
        concepts = self.dfs_extract_concepts(summary_text)
        topics = []
        
        for idx, (main_concept, sub_concepts) in enumerate(concepts.items(), 1):
            topics.append({
                "order": idx,
                "main": main_concept,
                "subtopics": sub_concepts,
                "depth": len(sub_concepts)
            })
        
        return topics
    
    def get_concept_difficulty(self, topic: Dict) -> str:
        """
        Estimate difficulty based on number of subtopics
        More subtopics = more complex concept
        """
        depth = topic["depth"]
        if depth == 0:
            return "Easy"
        elif depth <= 3:
            return "Medium"
        else:
            return "Hard"
    
    def get_dfs_order(self, summary_text: str) -> List[str]:
        """
        Get concepts in DFS order (main concept first, then all subconcepts)
        Useful for generating questions in logical progression
        """
        concepts = self.dfs_extract_concepts(summary_text)
        ordered = []
        
        for main_concept, sub_concepts in concepts.items():
            ordered.append(main_concept)
            ordered.extend(sub_concepts)
        
        return ordered
    
    def analyze_concept_relationships(self, summary_text: str) -> Dict:
        """
        Analyze relationships between concepts
        Returns statistics about concept structure
        """
        concepts = self.dfs_extract_concepts(summary_text)
        
        analysis = {
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
        
        return analysis
