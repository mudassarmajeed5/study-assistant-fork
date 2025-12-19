import heapq
from typing import List, Dict, Tuple, Set
from collections import defaultdict
import json

class QuizRecommender:
    """
    Uses A* algorithm to recommend the next optimal quiz question
    based on student performance, question difficulty, and learning value
    """
    
    def __init__(self, quiz_data: List[Dict]):
        """
        Initialize recommender with quiz data
        
        Args:
            quiz_data: List of quiz questions with metadata
        """
        self.quiz_data = quiz_data
        self.concept_graph = self._build_concept_graph()
    
    def _build_concept_graph(self) -> Dict:
        """
        Build concept dependency graph from quiz questions
        Returns: {concept: {related_concepts}}
        """
        graph = defaultdict(set)
        
        # Basic AI/ML course concept relationships
        relationships = {
            "variables": ["data_types"],
            "data_types": ["variables", "operators"],
            "operators": ["data_types", "conditionals"],
            "conditionals": ["operators", "loops"],
            "loops": ["conditionals", "arrays"],
            "functions": ["loops", "arrays"],
            "arrays": ["data_types", "loops"],
            "oop": ["functions", "arrays"],
        }
        
        for concept, related in relationships.items():
            for rel in related:
                graph[concept].add(rel)
        
        return graph
    
    def get_weak_topics(self, performance_history: Dict[int, float]) -> Set[str]:
        """
        Extract topics where student performed poorly
        
        Args:
            performance_history: {question_idx: score (0.0 or 1.0)}
        
        Returns:
            Set of weak topics
        """
        weak_topics = set()
        topic_scores = defaultdict(list)
        
        # Group performance by topic
        for q_idx, score in performance_history.items():
            if q_idx < len(self.quiz_data):
                question = self.quiz_data[q_idx]
                # Extract topic from question (heuristic: first few words)
                topic = question.get('topic', 'general')
                topic_scores[topic].append(score)
        
        # Find topics with < 70% accuracy
        for topic, scores in topic_scores.items():
            avg_score = sum(scores) / len(scores) if scores else 1.0
            if avg_score < 0.7:
                weak_topics.add(topic)
        
        return weak_topics
    
    def calculate_heuristic(self, question_idx: int, 
                           student_data: Dict) -> float:
        """
        Calculate heuristic value h(n) for A* algorithm
        Lower value = higher priority to ask
        
        Args:
            question_idx: Index of candidate question
            student_data: {
                'performance_history': dict,
                'total_score': float,
                'weak_topics': set,
                'questions_answered': int
            }
        
        Returns:
            Heuristic score (lower is better/higher priority)
        """
        if question_idx >= len(self.quiz_data):
            return float('inf')
        
        question = self.quiz_data[question_idx]
        
        # Start with neutral value
        h_value = 0.0
        
        # Factor 1: Learning Value based on weak topics
        weak_topics = student_data.get('weak_topics', set())
        question_topic = question.get('topic', 'general')
        
        if question_topic in weak_topics:
            h_value -= 10  # HIGH PRIORITY: Student needs this
        elif student_data.get('total_score', 0.5) > 0.8:
            # Student doing well, make it challenging
            difficulty = question.get('difficulty', 2)
            if difficulty >= 4:
                h_value -= 5  # Encourage harder questions
            else:
                h_value += 3  # Discourage easy questions
        
        # Factor 2: Difficulty relative to performance
        avg_score = student_data.get('total_score', 0.5)
        difficulty = question.get('difficulty', 2)  # 1-5 scale
        
        if avg_score < 0.5:  # Struggling
            if difficulty <= 2:
                h_value -= 5  # Easier questions help build confidence
            elif difficulty >= 4:
                h_value += 8  # Too hard, avoid
        elif avg_score < 0.7:  # Moderate performance
            if difficulty == 2 or difficulty == 3:
                h_value -= 7  # Optimal challenge zone
        else:  # Doing well
            if difficulty >= 4:
                h_value -= 6  # Push with harder questions
            else:
                h_value += 5  # Avoid wasting time on easy ones
        
        # Factor 3: Concept progression (prerequisites)
        answered_questions = student_data.get('questions_answered', set())
        prerequisites_met = self._check_prerequisites(question, answered_questions)
        
        if not prerequisites_met:
            h_value += 15  # Penalty: not ready for this question
        else:
            h_value -= 3  # Bonus: prerequisites met
        
        # Factor 4: Variety (avoid asking same topic repeatedly)
        recent_questions = list(answered_questions)[-5:] if answered_questions else []
        recent_topics = [self.quiz_data[q].get('topic', 'general') for q in recent_questions if q < len(self.quiz_data)]
        
        if question_topic in recent_topics:
            h_value += 2  # Small penalty for repetition
        else:
            h_value -= 1  # Small bonus for variety
        
        return h_value
    
    def _check_prerequisites(self, question: Dict, answered_questions: Set[int]) -> bool:
        """
        Check if student has answered prerequisites for this question
        
        Args:
            question: Question dict with potential 'prerequisites' key
            answered_questions: Set of question indices already answered
        
        Returns:
            True if prerequisites met (or no prerequisites)
        """
        prerequisites = question.get('prerequisites', [])
        
        if not prerequisites:
            return True  # No prerequisites = can answer
        
        # Check if any prerequisite questions were answered correctly
        for prereq_idx in prerequisites:
            if prereq_idx in answered_questions:
                # Check if they got it right (assuming 1.0 = correct, stored elsewhere)
                # For now, just check if attempted
                return True
        
        # No prerequisites met
        return len(answered_questions) == 0  # First question always ok
    
    def a_star_next_question(self, current_idx: int,
                            performance_history: Dict[int, float],
                            answered_questions: Set[int]) -> int:
        """
        Use A* algorithm to find the next optimal question to ask
        
        Args:
            current_idx: Current question index
            performance_history: {question_idx: score}
            answered_questions: Set of answered question indices
        
        Returns:
            Index of recommended next question
        """
        if current_idx >= len(self.quiz_data) - 1:
            return current_idx + 1  # End of quiz
        
        # Calculate student data for heuristics
        scores = list(performance_history.values())
        total_score = sum(scores) / len(scores) if scores else 0.5
        weak_topics = self.get_weak_topics(performance_history)
        
        student_data = {
            'performance_history': performance_history,
            'total_score': total_score,
            'weak_topics': weak_topics,
            'questions_answered': answered_questions
        }
        
        # Priority queue: (f_score, counter, question_index)
        open_set = []
        counter = 0
        
        # Examine all remaining questions
        for q_idx in range(current_idx + 1, len(self.quiz_data)):
            if q_idx in answered_questions:
                continue  # Skip already answered
            
            # g(n) = actual cost (distance from current)
            g_score = q_idx - current_idx
            
            # h(n) = heuristic (estimated learning value)
            h_score = self.calculate_heuristic(q_idx, student_data)
            
            # f(n) = g(n) + h(n)
            f_score = g_score + h_score
            
            heapq.heappush(open_set, (f_score, counter, q_idx))
            counter += 1
        
        # Return the question with lowest f-score (highest priority)
        if open_set:
            _, _, best_idx = heapq.heappop(open_set)
            return best_idx
        else:
            # Fallback: next unanswered question
            for q_idx in range(current_idx + 1, len(self.quiz_data)):
                if q_idx not in answered_questions:
                    return q_idx
            return current_idx + 1
    
    def get_performance_summary(self, performance_history: Dict[int, float]) -> Dict:
        """
        Generate summary of student performance
        
        Args:
            performance_history: {question_idx: score}
        
        Returns:
            Performance metrics by topic
        """
        topic_performance = defaultdict(lambda: {'correct': 0, 'total': 0})
        
        for q_idx, score in performance_history.items():
            if q_idx < len(self.quiz_data):
                question = self.quiz_data[q_idx]
                topic = question.get('topic', 'general')
                
                topic_performance[topic]['total'] += 1
                if score == 1.0:
                    topic_performance[topic]['correct'] += 1
        
        # Calculate percentages
        summary = {}
        for topic, stats in topic_performance.items():
            pct = (stats['correct'] / stats['total'] * 100) if stats['total'] > 0 else 0
            summary[topic] = {
                'score': f"{pct:.0f}%",
                'correct': stats['correct'],
                'total': stats['total']
            }
        
        return summary
    
    def recommend_review_topics(self, performance_history: Dict[int, float]) -> List[str]:
        """
        Recommend which topics to review based on performance
        
        Args:
            performance_history: {question_idx: score}
        
        Returns:
            Ranked list of topics to review (worst first)
        """
        topic_scores = defaultdict(list)
        
        for q_idx, score in performance_history.items():
            if q_idx < len(self.quiz_data):
                question = self.quiz_data[q_idx]
                topic = question.get('topic', 'general')
                topic_scores[topic].append(score)
        
        # Calculate average per topic and rank
        topic_avgs = []
        for topic, scores in topic_scores.items():
            avg = sum(scores) / len(scores)
            topic_avgs.append((topic, avg))
        
        # Sort by score (worst first)
        topic_avgs.sort(key=lambda x: x[1])
        
        return [topic for topic, _ in topic_avgs]
