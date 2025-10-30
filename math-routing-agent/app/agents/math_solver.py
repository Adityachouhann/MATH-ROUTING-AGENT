import openai
import re
from typing import List, Dict, Any
from app.config import Config

client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)

class MathSolverAgent:
    def generate_solution_from_kb(self, question: str, kb_solution: Dict) -> Dict[str, Any]:
        """Generate solution from knowledge base"""
        return {
            "source": "knowledge_base",
            "steps": kb_solution.get('steps', []),
            "final_answer": kb_solution.get('final_answer', ''),
            "confidence": "high",
            "similar_question": kb_solution.get('question', '')
        }
    
    def generate_solution_from_web(self, question: str, web_context: Dict) -> Dict[str, Any]:
        """Generate solution using web context"""
        try:
            context = self._prepare_web_context(web_context)
            
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": """You are a mathematics professor. Provide clear, educational step-by-step solutions.
                        Always explain each step and simplify complex concepts for students."""
                    },
                    {
                        "role": "user", 
                        "content": f"Solve this math problem: {question}\n\nContext from research: {context}"
                    }
                ],
                temperature=0.3,
                max_tokens=800
            )
            
            solution_text = response.choices[0].message.content
            steps = self._parse_solution_steps(solution_text)
            
            return {
                "source": "web_search",
                "steps": steps,
                "final_answer": self._extract_final_answer(steps),
                "confidence": "medium",
                "sources": web_context.get('sources', [])
            }
            
        except Exception as e:
            return self._generate_fallback_solution(question)
    
    def _prepare_web_context(self, web_context: Dict) -> str:
        """Prepare context from web search results"""
        context_parts = []
        
        if web_context.get('answer'):
            context_parts.append(f"Research findings: {web_context['answer']}")
        
        for i, source in enumerate(web_context.get('sources', [])[:2]):
            context_parts.append(f"Source {i+1}: {source.get('content', '')}")
        
        return "\n".join(context_parts) if context_parts else "No additional context"
    
    def _parse_solution_steps(self, solution_text: str) -> List[str]:
        """Parse solution into educational steps"""
        steps = []
        lines = solution_text.split('\n')
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith('```'):
                # Clean step markers
                clean_line = re.sub(r'^(?:\d+[\.\)]|\*|\-)\s*', '', line)
                if clean_line and len(clean_line) > 10:  # Meaningful content
                    steps.append(clean_line)
        
        return steps if steps else [solution_text]
    
    def _extract_final_answer(self, steps: List[str]) -> str:
        """Extract final answer from steps"""
        if not steps:
            return "Solution not available"
        
        # Look for final answer in last steps
        for step in reversed(steps[-3:]):
            if any(keyword in step.lower() for keyword in ['answer', 'therefore', 'thus', '=']):
                return step
        
        return steps[-1]
    
    def _generate_fallback_solution(self, question: str) -> Dict[str, Any]:
        """Generate fallback solution"""
        return {
            "source": "fallback",
            "steps": [f"Working on solution for: {question}", "Please try rephrasing your question."],
            "final_answer": "Solution generation in progress",
            "confidence": "low"
        }