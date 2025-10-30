import json
import numpy as np
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Any

class SimpleEncoder:
    """Vector encoder for mathematical content"""
    def __init__(self):
        self.vector_size = 384
    
    def encode(self, text: str) -> List[float]:
        """Encode text to vector using mathematical features"""
        vector = [0.0] * self.vector_size
        if not text:
            return vector
            
        text_lower = text.lower()
        
        # Mathematical symbol features
        math_symbols = ['+', '-', '*', '/', '=', '^', '√', 'π', 'θ', 'α', 'β']
        for i, symbol in enumerate(math_symbols):
            if i < len(vector):
                vector[i] = text.count(symbol) / len(text)
        
        # Mathematical topic features
        math_topics = {
            'algebra': ['solve', 'equation', 'variable', 'polynomial', 'quadratic'],
            'calculus': ['derivative', 'integral', 'limit', 'differentiate', 'integrate'],
            'geometry': ['area', 'volume', 'angle', 'triangle', 'circle', 'radius'],
            'trigonometry': ['sin', 'cos', 'tan', 'angle', 'triangle']
        }
        
        idx = 50
        for topic, keywords in math_topics.items():
            if idx < len(vector):
                vector[idx] = sum(1 for keyword in keywords if keyword in text_lower)
                idx += 1
        
        # Word frequency features
        words = text_lower.split()
        for i, word in enumerate(words[:100]):
            if 100 + i < len(vector):
                vector[100 + i] = 1.0
        
        # Normalize
        norm = np.linalg.norm(vector)
        if norm > 0:
            vector = [v / norm for v in vector]
        
        return vector

class MathKnowledgeBase:
    def __init__(self, collection_name="math_questions"):
        self.client = QdrantClient(":memory:")
        self.encoder = SimpleEncoder()
        self.collection_name = collection_name
        self.setup_collection()
        self.load_initial_data()
    
    def setup_collection(self):
        """Initialize Qdrant vector database"""
        self.client.recreate_collection(
            collection_name=self.collection_name,
            vectors_config=VectorParams(size=self.encoder.vector_size, distance=Distance.COSINE)
        )
    
    def load_initial_data(self):
        """Load comprehensive math dataset"""
        math_dataset = {
            "questions": [
                {
                    "question": "Solve the quadratic equation: x² - 5x + 6 = 0",
                    "solution": {
                        "steps": [
                            "Identify coefficients: a=1, b=-5, c=6",
                            "Calculate discriminant: D = b² - 4ac = (-5)² - 4(1)(6) = 25 - 24 = 1",
                            "Apply quadratic formula: x = [-b ± √D] / 2a",
                            "x = [5 ± √1] / 2 = [5 ± 1] / 2",
                            "x₁ = (5 + 1)/2 = 3, x₂ = (5 - 1)/2 = 2"
                        ],
                        "final_answer": "x = 2, 3"
                    },
                    "topic": "algebra"
                },
                {
                    "question": "Find the derivative of f(x) = 3x² + 2x - 1",
                    "solution": {
                        "steps": [
                            "Apply power rule: d/dx(xⁿ) = n*xⁿ⁻¹",
                            "d/dx(3x²) = 3*2x¹ = 6x",
                            "d/dx(2x) = 2",
                            "d/dx(-1) = 0",
                            "Combine results: f'(x) = 6x + 2"
                        ],
                        "final_answer": "f'(x) = 6x + 2"
                    },
                    "topic": "calculus"
                },
                {
                    "question": "Calculate the area of a circle with radius 7 cm",
                    "solution": {
                        "steps": [
                            "Formula: Area = πr²",
                            "Substitute r = 7",
                            "Area = π * (7)² = π * 49",
                            "Calculate: 49π ≈ 153.94 cm²"
                        ],
                        "final_answer": "153.94 cm²"
                    },
                    "topic": "geometry"
                }
            ]
        }
        
        points = []
        for i, item in enumerate(math_dataset['questions']):
            vector = self.encoder.encode(item['question'])
            point = PointStruct(
                id=i,
                vector=vector,
                payload=item
            )
            points.append(point)
        
        self.client.upsert(collection_name=self.collection_name, points=points)
        print(f"✅ Loaded {len(points)} math questions into vector database")
    
    def search_similar_questions(self, query: str, threshold: float = 0.6, top_k: int = 3):
        """Search for similar questions using vector similarity"""
        query_vector = self.encoder.encode(query)
        
        search_result = self.client.search(
            collection_name=self.collection_name,
            query_vector=query_vector,
            limit=top_k
        )
        
        results = []
        for result in search_result:
            if result.score >= threshold:
                results.append({
                    "question": result.payload["question"],
                    "solution": result.payload["solution"],
                    "similarity_score": float(result.score),
                    "topic": result.payload["topic"]
                })
        
        return results