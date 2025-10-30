import requests
import pandas as pd
from typing import List, Dict
import json
from datetime import datetime

class JEEBenchmark:
    def __init__(self, math_agent_url: str = "http://localhost:8000"):
        self.agent_url = math_agent_url
    
    def load_jee_questions(self) -> List[Dict]:
        """Sample JEE-level math questions"""
        return [
            {
                "id": 1,
                "question": "Find the derivative of f(x) = x^3 * sin(x)",
                "category": "calculus",
                "difficulty": "medium"
            },
            {
                "id": 2,
                "question": "Solve the equation: 2x^2 - 5x + 2 = 0", 
                "category": "algebra",
                "difficulty": "easy"
            },
            {
                "id": 3,
                "question": "Calculate the integral of ∫(3x^2 + 2x + 1) dx from 0 to 2",
                "category": "calculus",
                "difficulty": "medium"
            }
        ]
    
    def run_benchmark(self):
        """Run benchmark against JEE questions"""
        questions = self.load_jee_questions()
        results = []
        
        print("🧮 JEE BENCHMARK TEST")
        print("=" * 60)
        
        for question in questions:
            print(f"\nTesting: {question['question']}")
            
            try:
                response = requests.post(
                    f"{self.agent_url}/solve-math",
                    json={"question": question["question"]},
                    timeout=30
                )
                
                if response.status_code == 200:
                    data = response.json()
                    results.append({
                        'question_id': question['id'],
                        'question': question['question'],
                        'category': question['category'],
                        'difficulty': question['difficulty'],
                        'success': True,
                        'source': data['solution']['source'],
                        'confidence': data['solution']['confidence'],
                        'response_time': response.elapsed.total_seconds()
                    })
                    print(f"✅ SUCCESS - Source: {data['solution']['source']}")
                else:
                    results.append({
                        'question_id': question['id'],
                        'success': False,
                        'error': f"HTTP {response.status_code}"
                    })
                    print(f"❌ FAILED")
                    
            except Exception as e:
                results.append({
                    'question_id': question['id'],
                    'success': False,
                    'error': str(e)
                })
                print(f"❌ ERROR: {e}")
        
        # Calculate metrics
        successful = [r for r in results if r['success']]
        success_rate = len(successful) / len(results) if results else 0
        
        print("\n" + "=" * 60)
        print("📊 BENCHMARK RESULTS")
        print(f"Total Questions: {len(results)}")
        print(f"Successful: {len(successful)}")
        print(f"Success Rate: {success_rate:.1%}")
        
        if successful:
            sources = pd.Series([r['source'] for r in successful]).value_counts()
            print(f"Sources Used: {sources.to_dict()}")
        
        return pd.DataFrame(results)

if __name__ == "__main__":
    benchmark = JEEBenchmark()
    results_df = benchmark.run_benchmark()
    print(f"\nDetailed results saved for {len(results_df)} questions")