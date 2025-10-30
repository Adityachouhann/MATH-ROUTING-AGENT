try:
    import dspy
    from app.config import Config
    
    # Configure DSPy
    lm = dspy.OpenAI(model='gpt-3.5-turbo', api_key=Config.OPENAI_API_KEY)
    dspy.configure(lm=lm)
    DSPY_AVAILABLE = True
except ImportError:
    DSPY_AVAILABLE = False

class RouteQuerySignature(dspy.Signature if DSPY_AVAILABLE else object):
    """DSPy signature for intelligent routing"""
    question: str = dspy.InputField(desc="Mathematical question from student")
    knowledge_base_results: str = dspy.InputField(desc="Results from knowledge base search")
    use_knowledge_base: str = dspy.OutputField(desc="Whether to use knowledge base or web search")

class MathRoutingAgent:
    def __init__(self):
        self.dspy_available = DSPY_AVAILABLE
        if DSPY_AVAILABLE:
            self.route_classifier = dspy.Predict(RouteQuerySignature)
        else:
            self.route_classifier = None
    
    def route_question(self, question: str, kb_results: list):
        """Intelligent routing using DSPy"""
        if self.dspy_available and self.route_classifier:
            try:
                kb_info = f"Found {len(kb_results)} similar questions" if kb_results else "No similar questions found"
                
                prediction = self.route_classifier(
                    question=question,
                    knowledge_base_results=kb_info
                )
                
                use_kb = "knowledge base" in prediction.use_knowledge_base.lower()
                
                return {
                    "use_knowledge_base": use_kb,
                    "reasoning": prediction.use_knowledge_base,
                    "kb_match_count": len(kb_results),
                    "confidence": "high",
                    "dspy_used": True
                }
            except:
                # Fallback if DSPy fails
                return self._fallback_routing(kb_results)
        else:
            return self._fallback_routing(kb_results)
    
    def _fallback_routing(self, kb_results: list):
        """Fallback routing logic"""
        use_kb = len(kb_results) > 0
        
        return {
            "use_knowledge_base": use_kb,
            "reasoning": f"Found {len(kb_results)} similar questions in knowledge base",
            "kb_match_count": len(kb_results),
            "confidence": "medium",
            "dspy_used": False
        }